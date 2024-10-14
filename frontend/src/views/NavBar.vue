<template>
  <div class="colour" style="background-color: rgb(236, 213, 255);">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">M.P.S.S</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item" v-if="userRole">
              <router-link class="nav-link active" aria-current="page" to="/home">Home</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'librarian'">
              <router-link class="nav-link" to="/createsection">Create Section</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'librarian'">
              <router-link class="nav-link" to="/requests">Requests</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'librarian'">
              <router-link class="nav-link" to="/buybooks">Books Bought</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'user'" @click="getMyrequests">
              <router-link class="nav-link" to="/myrequests">My Requests</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'user'" @click="getMybooks">
              <router-link class="nav-link" to="/mybooks">My Books</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'librarian'">
              <router-link class="nav-link" to="/allbooks">All Books</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'user'">
              <router-link class="nav-link" to="/subscription">Subscription</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'user'">
              <router-link class="nav-link" to="/statsuser">Stats</router-link>
            </li>
            <li class="nav-item" v-if="userRole === 'librarian'">
              <router-link class="nav-link" to="/statslib">Stats</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/about">About</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/contact">Contact</router-link>
            </li>
            <li class="nav-item" v-if="userRole">
              <button class="nav-link" @click="logout">Logout</button>
            </li>
          </ul>
          <form id="searchform" class="d-flex ms-auto" method="post" @submit.prevent="searchFunction" v-if="userRole === 'user'">
            <select class="form-select me-2" id="field" name="field" aria-label="Default select example" v-model="field">
              <option value="section" selected>Section</option>
              <option value="book">Book</option>
              <option value="author">Author</option>
            </select>
            <input type="text" id="search" name="search" class="form-control me-2" placeholder="Search" v-model="search" />
            <button type="submit" class="button" @click="searchFunction">Search</button>
          </form>
          <form id="searchform" class="d-flex ms-auto" method="post" @submit.prevent="searchFunction" v-if="userRole === 'librarian'">
            <select class="form-select me-2" id="field" name="field" aria-label="Default select example" v-model="field">
              <option value="section" selected>Section</option>
              <option value="book">Book</option>
              <option value="author">Author</option>
            </select>
            <input type="text" id="search" name="search" class="form-control me-2" placeholder="Search" v-model="search" />
            <button type="submit" class="button" @click="searchFunctionLib">Search</button>
          </form>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  setup() {
    const toast = useToast();

    return {
      toast
    };
  },
  data() {
    return {
      field: '',
      search: '',
      results: [],
    };
  },
  computed: {
    userRole() {
      const userInfo = localStorage.getItem('user_info');
      if (userInfo) {
        const user = JSON.parse(userInfo);
        console.log('User role:', user.role.name);
        return user.role.name;
      }
      return null;
    }
  },
  methods: {
    logout() {
      const accesstoken = localStorage.getItem("access_token");
      this.$axios.post('http://127.0.0.1:5000/logout', null, {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user_info');
        this.$router.push('/').then(() => {
        window.location.reload();
        this.toast.success("Logged out successfully!!");
      });
      })
      .catch(error => {
        console.log('logout failed', error);
      });
    },
    searchFunction() {
      const user_id = JSON.parse(localStorage.getItem('user_info')).user_id;
      const accesstoken = localStorage.getItem("access_token");
      axios.post('http://127.0.0.1:5000/search', {
        field: this.field,
        search: this.search,
        user_id: user_id
      },
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        sessionStorage.setItem('searchResults', JSON.stringify(response.data));
        this.$router.go(0);
        this.$router.push({ path: `/searchresults` });
      })
      .catch(error => {
        console.error('Error found', error);
      });
    },
    searchFunctionLib() {
      const accesstoken = localStorage.getItem("access_token");
      axios.post('http://127.0.0.1:5000/searchl', {
        field: this.field,
        search: this.search,
      },
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        sessionStorage.setItem('searchResults', JSON.stringify(response.data));

        this.$router.push({ path: `/searchresultsl` });
      })
      .catch(error => {
        console.error('Error found', error);
      });
    },
    getMyrequests() {
      const formData = {
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
      };
      const accesstoken = localStorage.getItem("access_token");
      axios.get(`http://127.0.0.1:5000/myrequests`, { params: formData },
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        this.$router.push({ path: `/myrequests` });
      });
    },
    getMybooks() {
      const formData = {
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
      };
      const accesstoken = localStorage.getItem("access_token");
      axios.get(`http://127.0.0.1:5000/mybooks`, { params: formData },
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        this.$router.push({ path: `/mybooks` });
      });
    },
  }
};
</script>

<style scoped>
#searchform {
  display: flex;
  align-items: center;
}
.button{
    width:200px;
    height:38px;
    background: rgba(168, 29, 29, 1);
    border:none;
    outline:none;
    color:white;
    border-radius: 4px;
    cursor:pointer;
    font-weight:500;
    text-shadow: 3px 3px 8px rgb(238, 255, 0); 
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  }
</style>
