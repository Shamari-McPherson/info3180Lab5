<template>
  <div class="movie-list">
    <h1 class="movie-heading">Movies</h1>

    <!-- Display a simple loading message while fetching movies -->
    <div v-if="movies.length === 0" class="movie-load">
      <p class="loading-message">Movies are loading...</p>
    </div>

    <!-- Display the list of movies -->
    <div v-else class="movies-listed">
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <img 
          v-if="movie.poster" 
          :src="`http://localhost:5173${movie.poster}`" 
          alt="Movie Poster" 
          class="movie-img"
        />
        <div class="text-content">
          <h2 class="movie-title">{{ movie.title }}</h2>
          <p class="movie-description">{{ movie.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);
const errors = ref([]);

const fetchMovies = () => {
  fetch('/api/v1/movies', { method: 'GET' })
    .then((response) => response.json())
    .then((data) => {
      if (data.errors) {
        errors.value = data.errors;
      } else {
        movies.value = data.movies;
      }
    })
    .catch((error) => {
      errors.value = ["An unexpected error occurred."];
      console.error("Fetch error: ", error);
    });
};

onMounted(fetchMovies);
</script>

<style scoped>
.movie-heading {
  text-align: left;
  font-family: 'Montserrat', sans-serif;
  font-weight: bold;
  color: #6f4f9f; /* Lilac color */
  margin-left: 20px;
  font-size: 32px;
}

.movie-list {
  padding: 20px;
}

.movies-listed {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px 40px;
}

.movie-card {
  display: grid;
  grid-template-columns: 180px 1fr;
  align-items: flex-start;
  background-color: #f3e8ff; /* Light lilac background */
  border: 1px solid #e0d7f1; /* Cream border */
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 15px;
}

.movie-card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.movie-img {
  width: 170px;
  height: 250px;
  object-fit: cover;
  border-radius: 8px;
}

.text-content {
  padding-left: 20px;
  color: #333;
}

.movie-title {
  font-size: 20px;
  font-weight: bold;
  color: #6f4f9f;
}

.movie-description {
  font-size: 14px;
  color: #555;
  margin-top: 10px;
}

.movie-load {
  text-align: center;
  padding: 50px;
  background-color: #f3e8ff; /* Light lilac background */
  color: #6f4f9f;
  font-size: 18px;
}

.loading-message {
  color: #6f4f9f;
  font-weight: bold;
}
</style>
