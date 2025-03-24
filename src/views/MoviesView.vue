<template>
    <div class="movies-container">
      <h1 class="text-2xl font-bold mb-4">Movies</h1>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div v-for="movie in movies" :key="movie.id" class="movie-card border rounded-lg p-4 shadow-md">
          <img 
            :src="movie.poster" 
            :alt="movie.title" 
            class="w-full h-64 object-cover rounded-t-lg"
          >
          <div class="mt-4">
            <h2 class="text-xl font-semibold">{{ movie.title }}</h2>
            <p class="text-gray-600 mt-2">{{ movie.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  
  let movies = ref([]);
  
  const fetchMovies = async () => {
    try {
      const response = await fetch('/api/v1/movies');
      const data = await response.json();
      movies.value = data.movies;
    } catch (error) {
      console.error('Error fetching movies:', error);
    }
  };
  
  onMounted(fetchMovies);
  </script>