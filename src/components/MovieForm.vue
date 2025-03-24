<template>
    <div class="container mt-4">
      <form id="movieForm" @submit.prevent="saveMovie">
        <div v-if="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>
        
        <div v-if="errorMessages.length > 0" class="alert alert-danger">
          <ul>
            <li v-for="error in errorMessages" :key="error.field">
              {{ error.message }}
            </li>
          </ul>
        </div>
  
        <div class="form-group mb-3">
          <label for="title" class="form-label">Movie Title</label>
          <input 
            type="text" 
            name="title" 
            class="form-control" 
            placeholder="Enter movie title"
          />
        </div>
  
        <div class="form-group mb-3">
          <label for="description" class="form-label">Movie Description</label>
          <textarea 
            name="description" 
            class="form-control" 
            placeholder="Enter movie description"
            rows="4"
          ></textarea>
        </div>
  
        <div class="form-group mb-3">
          <label for="poster" class="form-label">Movie Poster</label>
          <input 
            type="file" 
            name="poster" 
            class="form-control" 
            accept="image/*"
          />
        </div>
  
        <button type="submit" class="btn btn-primary">Submit Movie</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  let csrf_token = ref("");
  let successMessage = ref("");
  let errorMessages = ref([]);
  
  function getCsrfToken() {
    fetch('/api/v1/csrf-token')
      .then((response) => response.json())
      .then((data) => {
        csrf_token.value = data.csrf_token;
      });
  }
  
  function saveMovie() {
    // Reset previous messages
    successMessage.value = "";
    errorMessages.value = [];
  
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);
  
    fetch("/api/v1/movies", {
      method: 'POST',
      body: form_data,
      headers: {
        'X-CSRFToken': csrf_token.value
      }
    })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.message) {
        successMessage.value = data.message;
        // Reset form after successful submission
        movieForm.reset();
      } else if (data.errors) {
        errorMessages.value = data.errors;
      }
    })
    .catch(function (error) {
      console.error("Error:", error);
      errorMessages.value = [{ message: "An unexpected error occurred" }];
    });
  }
  
  onMounted(() => {
    getCsrfToken();
  });
  </script>