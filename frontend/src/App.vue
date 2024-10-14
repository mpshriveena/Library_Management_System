<script setup>
import NavBar from './views/NavBar.vue'
import UserHome from "./views/UserHome.vue"
import LibrarianHome from "./views/LibrarianHome.vue"

</script>

<template>
  <div id="app">
    <NavBar/>
    <router-view/>
  </div>
</template>

<script>



export default {
  name: 'App',
  components: {
    NavBar,
    UserHome,
    LibrarianHome,
  },
  created() {
    const backgroundImage = localStorage.getItem('backgroundImage');
    console.log('Background Image URL:', backgroundImage); // Debugging line
    if (backgroundImage) {
      document.body.style.backgroundImage = `url(${backgroundImage})`;
    }
  }
}
</script>

<style>
body {
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  font-family: 'Poppins', 'sans-serif';
}
</style>
