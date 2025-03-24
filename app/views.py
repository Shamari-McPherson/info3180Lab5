"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from .models import Movie
from .forms import MovieForm

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

def form_errors(form):
    """
    Collects form errors and returns them as a list of dictionaries.
    Each dictionary represents a field with its corresponding error messages.
    """
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            error_messages.append({
                'field': field,
                'message': error
            })
    return error_messages

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    # Create form instance
    form = MovieForm()
    
    # Check if form validates
    if form.validate_on_submit():
        # Secure filename to prevent directory traversal attacks
        poster_file = form.poster.data
        filename = secure_filename(poster_file.filename)
        
        # Generate unique filename to prevent overwriting
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        
        # Save the file to uploads folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        poster_file.save(file_path)
        
        # Create new movie record
        new_movie = Movie(
            title=form.title.data,
            description=form.description.data,
            poster=unique_filename
        )
        
        # Add and commit to database
        db.session.add(new_movie)
        db.session.commit()
        
        # Return success response
        return jsonify({
            'message': 'Movie Successfully added',
            'title': new_movie.title,
            'poster': unique_filename,
            'description': new_movie.description
        }), 201
    
    # If validation fails, return errors
    return jsonify({
        'errors': form_errors(form)
    }), 400
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