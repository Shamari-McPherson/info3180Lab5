<template>
  <div class="movie-form-container">
    <transition name="fade-in-down">
      <h2>Add a New Movie</h2>
    </transition>

    <!-- Flash message UI -->
    <transition name="fade">
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </transition>

    <transition name="fade">
      <div v-if="errors.length" class="error-message">
        <ul>
          <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
        </ul>
      </div>
    </transition>

    <form id="movieForm" @submit.prevent="saveMovie" class="form-box" enctype="multipart/form-data">
      <transition name="slide-up" appear>
        <div class="form-group">
          <label for="title">Title</label>
          <input v-model="title" type="text" name="title" class="form-control" />
        </div>
      </transition>

      <transition name="slide-up" appear>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea v-model="description" name="description" class="form-control"></textarea>
        </div>
      </transition>

      <transition name="slide-up" appear>
        <div class="form-group">
          <label for="poster">Poster Image</label>
          <input @change="handleFileChange" ref="fileInput" type="file" name="poster" class="form-control" />
        </div>
      </transition>

      <transition name="fade-in">
        <button type="submit" class="submit-btn">Submit</button>
      </transition>
    </form>
  </div>
</template>

<script setup>
// In MovieForm.vue script section
import { ref, onMounted, nextTick, defineEmits } from "vue";

const emit = defineEmits(["flashMessage"]);
const title = ref("");
const description = ref("");
const poster = ref(null);
const fileInput = ref(null);
const csrf_token = ref("");
const successMessage = ref("");
const errors = ref([]);

// Fetch CSRF token more reliably
function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then(res => {
      if (!res.ok) {
        throw new Error(`Failed to fetch CSRF token: ${res.status}`);
      }
      return res.json();
    })
    .then(data => {
      console.log("CSRF token received");
      csrf_token.value = data.csrf_token;
    })
    .catch(error => {
      console.error("Error fetching CSRF token:", error);
      errors.value = ["Failed to fetch CSRF token. Please refresh the page."];
    });
}

onMounted(() => {
  getCsrfToken();
});

function handleFileChange(event) {
  poster.value = event.target.files[0];
}

function saveMovie() {
  errors.value = [];
  successMessage.value = "";
  
  // Validate form data
  if (!title.value) {
    errors.value.push("Title is required");
    return;
  }
  
  if (!description.value) {
    errors.value.push("Description is required");
    return;
  }
  
  if (!poster.value) {
    errors.value.push("Poster image is required");
    return;
  }
  
  if (!csrf_token.value) {
    console.error("No CSRF token available");
    errors.value.push("Security token missing. Please refresh the page.");
    return;
  }
  
  console.log("Creating FormData...");
  const form_data = new FormData();
  form_data.append("csrf_token", csrf_token.value);
  form_data.append("title", title.value);
  form_data.append("description", description.value);
  form_data.append("poster", poster.value);
  
  console.log("Submitting form with data:", {
    title: title.value,
    description: description.value,
    poster: poster.value.name,
    csrf_token: csrf_token.value.substring(0, 10) + "..." // Only log part of the token for security
  });
  
  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    credentials: 'same-origin'
  })
  .then(response => {
    console.log("Response status:", response.status);
    // Get response text for any status code
    return response.text().then(text => {
      // Try to parse as JSON if possible
      try {
        const data = JSON.parse(text);
        return { ok: response.ok, data };
      } catch (e) {
        // If not JSON, return the raw text
        return { ok: response.ok, text };
      }
    });
  })
  .then(result => {
    if (!result.ok) {
      console.error("Error response:", result.text || result.data);
      throw new Error(`Server returned ${result.ok ? "success" : "error"}`);
    }
    
    console.log("Success:", result.data);
    if (result.data.errors) {
      errors.value = result.data.errors;
      emit("flashMessage", errors.value);
    } else {
      successMessage.value = "Movie added successfully!";
      emit("flashMessage", successMessage.value);
      resetForm();
    }
  })
  .catch(error => {
    console.error("Error:", error);
    errors.value = [`Failed to submit form: ${error.message}`];
  });
}

function resetForm() {
  title.value = "";
  description.value = "";
  poster.value = null;
  nextTick(() => {
    if (fileInput.value) {
      fileInput.value.value = null;
    }
  });
}
</script>

<style scoped>
.success-message {
  color: green;
  background-color: #d4edda;
  padding: 10px;
  border-radius: 5px;
  width: fit-content;
  margin: 1rem auto;
  text-align: center;
}

.error-message {
  color: red;
  background-color: #f8d7da;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  width: fit-content;
  margin: 1rem auto;
  text-align: center;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
