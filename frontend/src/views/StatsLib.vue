<template>
  <div class="body">
    <div class="statsu-container">
      <h1>Statistics</h1>
      <br>
      <div class="div1">
        <div class="remaining">
          <div class="total-users">
            <h4>Total Users</h4><br>
            <h5>{{ data.total_users }}</h5>
          </div>
          <div class="active_users">
            <h4>Active Users</h4><br>
            <h5>{{ data.active_users }}</h5>
          </div>
          <div class="revenue_by_books">
            <h4>Revenue from books</h4><br>
            <h5>{{ data.revenue_by_books }}</h5>
          </div>
          <div class="total_requests">
            <h4>Total Requests</h4><br>
            <h5>{{ data.total_requests }}</h5>
          </div>
          <div class="pending_requests">
            <h4>Pending Requests</h4><br>
            <h5>{{ data.pending_requests }}</h5>
          </div>
          <div class="subscribes-revenue">
            <h4>Revenue from Subscribes</h4><br>
            <h5>{{ data.subscribes * 2000 }}</h5>
          </div>
          <div class="total_buys">
            <h4>Total Books Bought</h4><br>
            <h5>{{ data.total_buys }}</h5>
          </div>
          <div class="total_subscribes">
            <h4>Total Subscribers</h4><br>
            <h5>{{ data.subscribes }}</h5>
          </div>
          <div class="total_revenue">
            <h4>Total Revenue Generated</h4><br>
            <h1>{{ data.total_revenue }}</h1>
          </div>
        </div>
        <div class="current-books">
          <h2>Popular Requested Books</h2><br>
          <div v-if="data.popular_requested_books.length > 0">
          <div v-for="book in data.popular_requested_books" :key="book.id" class="book-items">
            <h3>{{ book.book_title }}</h3>
            <p>Total Requests: {{ book.request_count }}</p>
          </div>
        </div>
        <h6 v-else>No requests yet</h6>
        <br><br>
          <h2>Popular Bought Books</h2><br>
          <div v-if="data.popular_bought_books.length > 0">
          <div v-for="book in data.popular_bought_books" :key="book.id" class="book-items">
            <h3>{{ book.book_title }}</h3>
            <p>Total Buys: {{ book.buy_count }}</p>
          </div>
          </div>
          <h6 v-else>No books bought yet yet</h6>
        </div>
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
      data: {},
    };
  },
  created() {
    this.getLibstats();
  },
  methods: {
    getLibstats() {
      const accesstoken = localStorage.getItem("access_token");
      axios.get('http://127.0.0.1:5000/getlibstats/', {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.data = response.data;
          console.log(this.data);
        })
        .catch(error => {
          console.error('Error fetching Librarian stats:', error);
          this.toast.error("Error fetching statistics page");
        });
    },
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', 'sans-serif';
}

.body {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.statsu-container {
  width: 95%;
  height: 85vh;
  background: transparent;
  border: 0;
  color: white;
  border-radius: 10px;
  padding: 50px;
  box-shadow: 0 0 25px 10px rgb(0, 0, 0);
  text-align: center;
}

.div1 {
  display: flex;
  column-gap: 5%;
  height: 100%;
}

.remaining {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 10px;
  width: 66%;
  height: 90%;
  padding:10px;
  border-radius: 10px;
  background: transparent;
  border: 2px solid rgb(255, 255, 255);
}

.current-books {
  text-align: center;
  padding: 20px;
  width: 33%;
  height: 90%;
  background: transparent;
  border: 2px solid rgb(255, 255, 255);
  border-radius: 10px;
}

.total-users, .active_users, .revenue_by_books,
.total_requests, .pending_requests, .subscribes-revenue,
.total_buys, .total_subscribes, .total_revenue {
  background: transparent;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 25px 10px rgb(0, 0, 0);
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 10px;
  text-align: center;
  transition: transform 0.3s ease;
}

.total-users:hover, .active_users:hover, .revenue_by_books:hover,
.total_requests:hover, .pending_requests:hover, .subscribes-revenue:hover,
.total_buys:hover, .total_subscribes:hover, .total_revenue:hover {
  transform: scale(1.1);
}

.book-items {
  background: transparent;
  border-radius: 10px;
  margin-top: 16px;
  padding: 4%;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 25px 10px rgb(0, 0, 0);
}

h4, h5 {
  text-shadow: 3px 3px 8px rgb(68, 0, 255);
}

h3, p {
  text-shadow: 3px 3px 8px rgb(0, 255, 21);
}

h2 {
  text-shadow: 3px 3px 8px rgb(255, 0, 212);
}

h1 {
  color: black;
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
}
.pwhite{
  color:white;
}
</style>
