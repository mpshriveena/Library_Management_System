<template>
  <div class="body">
  <div class="section-container">
    <h1>Search results</h1>
  <div v-if="field==='section'" class="sections">
      <div v-if="results.length > 0">
      <p class="pwhite">Your search results for "{{ search }}" under "{{ field }}" are given below..</p>
      <div v-for="section in results" v-bind:key="section.id" class="section-item" @click='UserviewBooks(section.id)'>
          <h2>{{section.sec_title}}</h2>
          <p>{{section.sec_description}}</p>
          <button class="button" @click='UserviewBooks(section.id)'>View Books</button>
      </div>
    </div>
    <p v-else  class="pwhite">No results for search "{{ search }}"</p>
   </div>
   <div v-if="field === 'book' || field === 'author'">
    <p class="pwhite">Your search results for "{{ search }}" under "{{ field }}" are given below..</p>
    <div v-if="results.length > 0" class="book-grid">
      <div v-for="book in results" :key="book.id" class="book-item" @click="viewDetails(book.id)">
        <img :src="`http://127.0.0.1:5000/${book.image_path}`" alt="Book Image" v-if="book.image_path" style="max-width: 200px; max-height: 300px;" />        
        <p><strong>{{ book.book_title }}</strong></p>
        <button class="button1" @click="viewDetails(book.id)">View Details</button>
      </div>
    </div>
    <p v-else class="pwhite">No results for search "{{ search }}"</p>
  </div>
</div>
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
      field:'',
      search:'',
      results:[],
    };
  },
  mounted() {
    this.getSearchResults();
  },
  methods: {
  getSearchResults(){
    const searchResults = JSON.parse(sessionStorage.getItem('searchResults'));
    const accesstoken = localStorage.getItem("access_token");
    if (searchResults) {
      this.field = searchResults.field;
      this.search = searchResults.search;
      this.results = searchResults.results;
    } else {
      axios.get('http://127.0.0.1:5000/search',
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.field = response.data.field;
          this.search = response.data.search;
          this.results = response.data.results;
        })
        .catch(error => {
          console.error('Error found', error);
        });
    }
  },
  UserviewBooks(id) {
    this.$router.push({ path: `/section/${id}/books` });
  },
  viewDetails(id) {
        this.$router.push({ path: `/viewdetails/${id}/` });
    },
}
}
</script>

  
<style scoped>
*{
  font-family: 'Poppins', 'sans-serif'; 
}
.body {
  padding: 3%;
  min-height: 100vh;

}
.section-container {
  padding: 20px;
}  
.sections {
  margin-top: 30px;
  padding:10px
}

.section-item {
  background: rgba(255, 255, 255);
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
.section-item:hover{
  transform: scale(1.01);
}
.section-item h2 {
  margin-bottom: 10px;
}

.section-item p {
  margin-bottom: 20px;
}
.book-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.book-item {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.336);
  padding: 16px;
  transition: box-shadow 0.3s, transform 0.3s;
  text-align: center;
}

.book-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-4px);
}

.book-item img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin-bottom: 16px;
}
.button{
  width:8%;
  height:45px;
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
.button1{
  width:100%;
  height:45px;
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
h1,h3{
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
color:#ffffff;
padding:10px;
}
.pwhite{
  color:white;
}
</style>