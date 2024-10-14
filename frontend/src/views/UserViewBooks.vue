<template>
  <div class="body">
    <h2>{{ section_title }}</h2>
    <p class="pwhite">View and request books of {{section_title}} here. If already requested, go to the "My Requests" page to view the status of your request.</p>
    <div v-if="books.length > 0" class="book-grid">
      <div v-for="book in books" :key="book.id" class="book-item" @click="viewDetails(book.id)">
        <img :src="`http://127.0.0.1:5000/${book.image_path}`" alt="Book Image" v-if="book.image_path" style="max-width: 200px; max-height: 300px;" />        
        <h5>{{ book.book_title }}</h5>
        <button class="button" @click="viewDetails(book.id)">View Details</button>
      </div>
    </div>
    <p v-else class="pwhite">No book is found in this section.</p>
  </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default {
  props: ['id'],
  setup() {
    const toast = useToast();

    return {
      toast
    };
  },
  data() {
    return {
      books: [],
      section_title: '',
    };
  },

  mounted() {
    this.fetchBooks();
  },

  methods: {
    fetchBooks() {
      const accesstoken = localStorage.getItem("access_token");
      axios.get(`http://127.0.0.1:5000/section/${this.id}/books`, {
        params: { user_id: this.user_id },headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        this.books = response.data.books;
        this.section_title = response.data.section_title;
        console.log(this.books)
      })
      .catch(error => {
        console.error('Error fetching books:', error);
      });
    },
    viewDetails(id) {
        this.$router.push({ path: `/viewdetails/${id}/` });
    }
  }
};
</script>

<style scoped>
.body {
  padding: 3%;
  min-height: 100vh;

}

.book-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.book-item {
  background-color: #ffffff;
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

.book-item h5 {
  font-size: 18px;
  margin: 16px 0;
}

.book-item .btn {
  margin-top: 8px;
}

h2 {
  color:white;
  font-size: 30px;
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
}
.button{
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
.pwhite{
  color:white;
}
</style>