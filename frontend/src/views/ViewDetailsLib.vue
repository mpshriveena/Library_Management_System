<template>
    <div class="details-container">
      <div class="book-details">
        <div class="book-info">
          <img :src="`http://127.0.0.1:5000/${details.image_path}`" alt="Book Image" v-if="details.image_path" />
          <div class="book-meta">
            <h1>ID:{{details.id}} {{ details.book_title }}</h1>
            <p>{{ details.author }}</p>
            <h2>Rs. {{ details.price }}</h2>
            <p> {{ details.book_description }}</p>
            <button class="btn btn-success me-3" @click='readBook(details.id)'>Read Book</button>
          <button class="btn btn-success me-3" @click='editBook(details.id,details.book_title,details.price,details.book_description,details.author)'>Edit Book</button>
          <button class="btn btn-danger" @click='deleteBook(details.id)'>Delete</button>
          </div>
        </div>
        <h5>Feedbacks({{ feedbacks.length }})</h5>
        <div class="feedback-section">
          <div v-if="feedbacks.length > 0">
            <div v-for="feedback in feedbacks" :key="feedback.id">
              <label><strong>{{ feedback.username }}</strong></label>
              <p>{{ feedback.feedback }}</p>
            </div>
          </div>
          <p v-else>No feedbacks yet.</p>
        </div>
      </div>
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
        details: {},
        feedback: '',
      };
    },
    created() {
      this.getDetailsLib(this.id);
    },
    
    methods: {
      getDetailsLib(id) {
        const accesstoken = localStorage.getItem("access_token");
        axios.get(`http://127.0.0.1:5000/viewdetailslib/${id}`,
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
          .then(response => {
            this.details = response.data.details;
            this.feedbacks = response.data.feedbacks;
          })
          .catch(error => {
            console.error('Error fetching books:', error);
          });
      },
      deleteBook(id) {
  const accesstoken = localStorage.getItem("access_token");
  axios.delete(`http://127.0.0.1:5000/deletebook/${id}/`, {
    headers: {
      Authorization: `Bearer ${accesstoken}`
    }
  })
  .then(response => {
    console.log('Book deleted successfully', response);
    this.toast.success("Book deleted successfully!!");
    this.$router.go(-1);
  })
  .catch(error => {
    console.error('Error found', error);
  });
}
,
  editBook(id, book_title,price, book_description, author) {
      this.$router.push({
        name: 'EditBook',
        params: { id: id, book_title: book_title,price: price.toString(), book_description:book_description, author:author }
      });
    },
    readBook(book_id) {
      axios.get(`http://127.0.0.1:5000/book/${book_id}`)
        .then(response => {
          const filePath = response.data.file_path;
          this.toast.warning("Opening book");
          window.open(`http://127.0.0.1:5000/${filePath}`, '_blank');
        })
        .catch(error => {
          console.error('Error fetching book file:', error);
        });
    },
    }
  };
  </script>
  
  <style scoped>
  .details-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding: 20px;
  }
  
  .book-details {
    background: rgba(255, 255, 255, 1);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
    width: 90%;
    max-width: 1800px;
    height: 90vh; /* Adjust the height */
    max-height: 85vh;
    overflow: auto;
  }
  
  .book-info {
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
  }
  
  .book-info img {
    max-width: 320px;
    max-height: 480px;
    margin-right: 20px;
  }
  
  .book-meta {
    flex: 1;
  }
  
  .feedback-section {
    margin-top: 20px;
  }
  </style>
  