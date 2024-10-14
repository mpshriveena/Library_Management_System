<template>
    <div class="body">
      <div class="statsu-container">
      <h1>Statistics</h1>
      <br>
      <div class="div1">
      <div class="remaining">
        <div class="login">
        <div class="last-login">
      <h5>Last Login at: {{ data.last_login_at }}</h5>
    </div>
    <div class="current-login">
      <h5>Current Login at: {{ data.current_login_at }}</h5>
    </div>
  </div>
  <div class="div2">
          <div class="total-requests">
            <h4>Total Requests</h4><br>
            <h5>{{ data.requests }}</h5>
          </div>
          <div class="remaining-requests">
            <h4>Remaining Requests</h4><br>
          <div v-if="data.requests_remaining==='unlimited'">
            <h5>Unlimited</h5>
          </div>
          <div v-else-if="data.requests_remaining===0">
            <h5>0</h5>
          </div>
          <div v-else><h5>{{ data.requests_remaining }}</h5>
          </div>
        </div>
      </div>
      <div class="div3">
          <div class="pending-requests">
            <h4>Books Bought</h4><br>
            <h5>{{ data.buys }}</h5>
          </div>
          <div class="books-read">
            <h4>Books Read</h4><br>
            <h5>{{ data.total_read }}</h5>
          </div>
        </div>
      </div>
            <div class="current-books">
      <h2>My Current Requested Books</h2><br>
      <div v-for="request in data.request_details" v-bind:key="request.id" class="book-items">
            <h3>{{request.book_title}}</h3>
            <p>Requested for : {{request.days}} days</p>
            <p>Days remaining : {{request.days_remaining}}</p>
          </div>
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
        data:{},
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
      };
    },
  
    created() {
      this.getUserstats(this.user_id);
      this.user_id= JSON.parse(localStorage.getItem('user_info')).user_id;

    },
  
    methods: {
      getUserstats(user_id) {
        const accesstoken = localStorage.getItem("access_token");
        axios.get(`http://127.0.0.1:5000/getuserstats/${user_id}`,
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
          .then(response => {
            this.data = response.data;
            console.log(this.data);
          })
          .catch(error => {
            console.error('Error fetching userstats:', error);
          });
      },
  }}
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
      text-align:center;
  }

.div1{
  display:flex;
  column-gap: 5%;
}
.remaining {

  text-align: left;
  padding:3%;
  width:66%;
  height: 70vh;
  border-radius: 10px;
  background: transparent;
  border: 2px solid rgb(255, 255, 255);
}
.current-books{
  text-align: center;
  padding:20px;
  width:33%;
  height: auto;
  background: transparent;
  border: 2px solid rgb(255, 255, 255);
  border-radius: 10px;
}
.login{
  display:flex;
  justify-content: space-between;
}
.last-login, .current-login {
  border-radius: 10px;
  background: transparent;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 25px 10px rgb(0, 0, 0);
  height:5vh;
  padding:10px;
  transition: transform 0.3s ease;
}
.div2{
  display:flex;
  justify-content: space-between;
}
.div3{
  display:flex;
  justify-content: space-between;
}
.total-requests, .pending-requests, .books-read, .remaining-requests {
  background: transparent;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 25px 10px rgb(0, 0, 0);  border-radius: 10px;
  margin-top:50px;
  padding:7%;
  text-align: center;
  transition: transform 0.3s ease;
}
.last-login:hover, .current-login:hover, .total-requests:hover, .pending-requests:hover, .books-read:hover, .remaining-requests:hover{
  transform: scale(1.1);
}
.total-requests, .pending-requests{
  width:45%;
}
.books-read, .remaining-requests{
  width:50%;
}
.book-items{
  background: transparent;
  border-radius: 10px;
  margin-top:7px;
  padding:3%;
  backdrop-filter: blur(20px);
  box-shadow: 0 0 25px 10px rgb(0, 0, 0);
}
h4,h5{
  text-shadow: 3px 3px 8px rgb(68, 0, 255);
}
h3,p{
  text-shadow: 3px 3px 8px rgb(0, 255, 21);
}
h2{
  text-shadow: 3px 3px 8px rgb(255, 0, 212);
}
h1{
  color:black;
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
}
</style>