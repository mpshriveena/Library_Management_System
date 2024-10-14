<template>
  <div class="details-container">
    <div class="book-details">
      <div class="book-info">
        <img :src="`http://127.0.0.1:5000/${details.image_path}`" alt="Book Image" v-if="details.image_path" />
        <div class="book-meta">
          <h1>{{ details.book_title }}</h1>
          <p>{{ details.author }}</p>
          <h2>Rs : {{ details.price }}</h2>
          <p> {{ details.book_description }}</p>
          <div v-if="details.request_status === 'granted'" class="d-flex">
            <button class="btn btn-success me-3" @click='readBook(details.id)'>Read</button>
            <button class="btn btn-danger" @click="returnbook(details.id)">Return</button>
          </div>
          <div v-else-if="details.request_status === 'bought'">
            <button class="btn btn-success me-3" @click='readBook(details.id)'>Read</button>
          </div>
          <div v-else-if="details.request_status === 'Access Revoked'">
            <button class="btn btn-outline-secondary disabled">Access Revoked</button>
          </div>
          <div v-else-if="details.request_status === 'pending'">
            <button class="btn btn-secondary disabled">Requested</button>
          </div>
          <div v-else-if="details.request_status === 'rejected'">
            <button class="btn btn-danger disabled">Rejected</button>
          </div>
          <div v-else-if="details.request_status === 'returned'">
            <button class="btn btn-outline-danger disabled">Returned</button>
          </div>
          <div v-if="details.request_status === 'not_requested'" class="d-flex">
            <button class="btn btn-success me-3" @click="requestBook(details.id)">Request</button>
            <button class="btn btn-success" @click="buyBook(details.id)">Buy Now</button>
          </div>
        </div>
      </div>
      <h5>Feedbacks({{ feedbacks.length }})</h5>
      <div class="feedback-section">
        <div class="mb-3">
          <label for="exampleFormControlInput1" class="form-label">Your feedback</label>
          <div v-if="details.request_status === 'granted' || details.request_status === 'Access Revoked' || details.request_status === 'returned' || details.request_status === 'bought'" class="d-flex">
            <div class="d-flex w-100">
              <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Your feedback here..." v-model='feedback'>
              <button @click='sendFeedback()' class="btn btn-outline-secondary ms-2">Submit</button>
            </div>
          </div>
          <div v-else>
            <div class="d-flex w-100">
              <input type="text" class="form-control" id="exampleFormControlInput1" placeholder="Read the book to write your feedback here..." v-model='feedback' disabled>
              <button @click='sendFeedback()' class="btn btn-outline-secondary disabled ms-2">Submit</button>
            </div>
          </div>
        </div>
        <div v-if="feedbacks.length > 0">
          <div v-for="feedback in feedbacks" :key="feedback.id">
            <label><strong>{{ feedback.username }}</strong></label>
            <p>{{ feedback.feedback }}</p>
          </div>
        </div>
        <p v-else>No feedbacks yet. Be the one to give the first feedback</p>
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
      user_info: null,
      user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
    };
  },
  created() {
    this.getDetails(this.id);
    this.user_info = localStorage.getItem('user_info');
  },
  
  methods: {
    getDetails(id) {
      const accesstoken = localStorage.getItem("access_token");
      axios.get(`http://127.0.0.1:5000/viewdetails/${id}`, {
        params: { user_id: this.user_id },headers: {
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
    requestBook(id) {
      const accesstoken = localStorage.getItem("access_token");
      axios.get(`http://127.0.0.1:5000/requestbook/${id}/`, { params: { user_id: this.user_id },headers: {
          Authorization: `Bearer ${accesstoken}`
        } })
        .then(response => {
          this.$router.push({ path: `/requestbook/${id}/` });
        })
        .catch(error => {
          console.error('Error requesting book:', error);
          this.toast.error("You cannot request more than 5 books!! Subscribe for more requests.");
        });
    },
    buyBook(id) {
      const accesstoken = localStorage.getItem("access_token");
      axios.get(`http://127.0.0.1:5000/buybook/${id}/`, { params: { user_id: this.user_id },headers: {
          Authorization: `Bearer ${accesstoken}`
        } })
        .then(response => {
          this.$router.push({ path: `/buybook/${id}/` });
        })
        .catch(error => {
          console.error('Error buying book:', error);
          alert(error.response.data.message);
        });
    },
    readBook(id) {
      axios.get(`http://127.0.0.1:5000/book/${id}`)
        .then(response => {
          const filePath = response.data.file_path;
          this.toast.warning("Opening book");
          window.open(`http://127.0.0.1:5000/${filePath}`, '_blank');
        })
        .catch(error => {
          console.error('Error fetching book file:', error);
        });
    },
    returnbook(id) {
      const accesstoken = localStorage.getItem("access_token");
      axios.put(`http://127.0.0.1:5000/returnbook/${id}`,{},
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.$router.go(0);
          this.toast.success("Book returned successfully!!");
        })
        .catch(error => {
          console.error('Error found', error);
        });
    },
    sendFeedback() {
      const accesstoken = localStorage.getItem("access_token");
      axios.post(`http://127.0.0.1:5000/sendfeedback/`,
        {
          feedback: this.feedback,
          user_id: this.user_id,
          book_id: this.id,
        },
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.toast.success("Thanks for you feedback!!");
          this.$router.go(0);
        })
        .catch(error => {
          console.error('Error found', error);
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
