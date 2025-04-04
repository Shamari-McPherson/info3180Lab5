"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import Movie
from .forms import MovieForm
from flask_wtf.csrf import generate_csrf

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/api/v1/movies', methods=['POST', 'GET'])
def movies():
    if request.method == 'GET':
        # Retrieve all movies from the database
        movies = Movie.query.all()
        
        # Convert movies to a list of dictionaries
        movie_list = []
        for movie in movies:
            movie_list.append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'poster': f'/api/v1/posters/{movie.poster}'
            })
        
        # Return the list of movies as JSON
        return jsonify({'movies': movie_list})
    
    elif request.method == 'POST':
        try:
            # Print raw request data for debugging
            print("==== REQUEST DATA ====")
            print("Form data:", dict(request.form))
            print("Files:", request.files)
            print("Headers:", dict(request.headers))
            
            # Create form instance
            form = MovieForm()
            
            print("==== FORM VALIDATION ====")
            valid = form.validate_on_submit()
            print(f"Form valid: {valid}")
            
            if not valid:
                print("Validation errors:", form.errors)
                # Check for CSRF errors specifically
                if 'csrf_token' in form.errors:
                    print("CSRF error:", form.errors['csrf_token'])
                    
                return jsonify({
                    'errors': form_errors(form)
                }), 400
            
            print("==== PROCESSING FORM ====")
            print(f"Title: {form.title.data}")
            print(f"Description: {form.description.data}")
            
            # Handle poster file
            poster_file = form.poster.data
            filename = secure_filename(poster_file.filename)
            print(f"Original filename: {filename}")
            
            # Generate unique filename
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            print(f"Generated filename: {unique_filename}")
            
            # Save the file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            poster_file.save(file_path)
            print(f"File saved to: {file_path}")
            
            try:
                print("==== DATABASE OPERATION ====")
                # Create new movie with debugging info
                print("Creating movie object...")
                new_movie = Movie(
                    title=form.title.data,
                    description=form.description.data,
                    poster=unique_filename
                )
                
                print(f"Movie object created: {new_movie.title}")
                
                # Add and commit to database
                print("Adding to session...")
                db.session.add(new_movie)
                print("Committing...")
                db.session.commit()
                print("Database commit successful")
                
                return jsonify({
                    'message': 'Movie Successfully added',
                    'title': new_movie.title,
                    'poster': new_movie.poster,
                    'description': new_movie.description
                }), 201
                
            except Exception as db_error:
                print("==== DATABASE ERROR ====")
                print(f"Error: {str(db_error)}")
                print("Stack trace:")
                import traceback
                traceback.print_exc()
                db.session.rollback()
                return jsonify({'errors': [f"Database error: {str(db_error)}"]}), 500
                
        except Exception as e:
            print("==== SERVER ERROR ====")
            print(f"Error: {str(e)}")
            print("Stack trace:")
            import traceback
            traceback.print_exc()
            return jsonify({'errors': [f"Server error: {str(e)}"]}), 500

# Add a route to serve poster images
@app.route("/api/v1/posters/<filename>")
def get_posters(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename), 200
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()}), 200


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404