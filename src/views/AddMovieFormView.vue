<template>
  <div>
    <h1 class="text-center my-4">Add a New Movie</h1>
    <MovieForm @flashMessage="flashMessage" />
    <transition name="fade">
      <div v-if="message" class="text-green-600 mt-4 text-center">
        {{ message }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MovieForm from '@/components/MovieForm.vue'

// Holds the flash message text
const message = ref('')

/**
 * Displays a temporary flash message for 5 seconds.
 * @param {string} msg - The message to display.
 */
const flashMessage = (msg) => {
  message.value = msg
  setTimeout(() => {
    message.value = ''
  }, 5000)
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
