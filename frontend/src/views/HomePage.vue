<template>
    <div>
      <UserHome v-if="user_info && user_info.role.name === 'user'"/>
      <LibrarianHome v-if="user_info && user_info.role.name === 'librarian'"/>
    </div>
  </template>
  
  <script>
  import UserHome from "./UserHome.vue";
  import LibrarianHome from "./LibrarianHome.vue";
  
  export default {
    data() {
      return {
        user_info: JSON.parse(localStorage.getItem('user_info')),
        access_token: localStorage.getItem('access_token'),
      };
    },
    components: {
      UserHome,
      LibrarianHome,
    },
  };
  </script>
  

<style>

</style>