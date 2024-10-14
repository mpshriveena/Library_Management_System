<template>
    <div class="section-container">
      <div class="recent-books">
      <h3>Recent Books</h3>
      <div v-if="recent_books.length > 0" class="books-row">
      <div v-for="book in recent_books" :key="book.id" class="book-item" @click="viewDetails(book.id)">
        <img :src="`http://127.0.0.1:5000/${book.image_path}`" alt="Book Image" v-if="book.image_path" style="max-width: 200px; max-height: 300px;" />        
        <p><strong>{{ book.book_title }}</strong></p>
      </div>
    </div>
    <p v-else class="pwhite">No book added recently.</p>
  </div>
  <div class="sections">
        <h1>Sections</h1>
        <div v-if="sections.length > 0">
        <div v-for="section in sections" v-bind:key="section.id" class="section-item" @click='UserviewBooks(section.id)'>
            <h2>{{section.sec_title}}</h2>
            <p>{{section.sec_description}}</p>
            <button class="button" @click='UserviewBooks(section.id)'>View Books</button>
        </div>
      </div>
      <p v-else class="pwhite">Not section added yet</p>
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
        recent_books:[],
        sections:[],
        access_token: localStorage.getItem('access_token'),
      };
    },
    mounted() {
      this.getSections();
    },
    methods: {
      getSections(){
        const accesstoken = localStorage.getItem("access_token");
      axios.get('http://127.0.0.1:5000/home',
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.sections = response.data.sections;
          this.recent_books = response.data.recent_books;
        })
        .catch(error => {
          console.error('Error found', error);
        });
    },

    UserviewBooks(id) {
        this.$router.push({ path: `/section/${id}/books` });
      },
      viewDetails(id) {
        this.$router.push({ path: `/viewdetails/${id}/` });
    }
  }
  }
  </script>
  
    
<style scoped>
*{
  font-family: 'Poppins', 'sans-serif'; 
}
.section-container {
  padding: 20px;
}

.recent-books {
  margin-bottom: 30px;
}

.books-row {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
}

.book-item {
  background: rgba(255, 255, 255, 1);
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  text-align: center;
  transition: box-shadow 0.3s, transform 0.3s;
  width: 18%;
  margin: 10px;
}

.book-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-4px);
}

.book-item img {
  width: 100%;
  height: auto;
  max-height: 150px;
  margin-bottom: 10px;
}

.book-item p {
  margin: 10px 0;
}

.sections {
  margin-top: 30px;
  padding:10px
}

.section-item {
  background: rgb(255, 255, 255);
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
h1,h3{
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
color:#ffffff;
padding:10px;
}
.pwhite{
  color:white;
}
</style>