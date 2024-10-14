<template>
  <div class="body">
  <div class="subscription-container">
    <div v-if="user_info.subscription" class="subscribed-section">
     <br> <h1 class="title">Subscription</h1>
      <br><br>
      <h4>Thank You for subscribing. You can now request for unlimited number of books.</h4>
    <br>
      <h3>Happy Learning!!</h3>
    </div>
    <div v-else class="subscribed-section">
      <h1>Subscription</h1>
      <br><br>
      <h4>Tired of requesting only 5 books?</h4>
      <br>
      <p>Subscribe for requesting unlimited books.</p>
      <br>
      <p>Happy Note: This is a one-time subscription.</p>
      <br>
      <h3>Subscription Amount: Rs. 2000 only</h3>
      <br>
      <button class="button" @click="subscribe(user_info.user_id)">Subscribe</button>
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
      user_info: JSON.parse(localStorage.getItem('user_info')),
    };
  },
  methods: {
    subscribe(id){
      const accesstoken = localStorage.getItem("access_token");
      axios.put(`http://127.0.0.1:5000/subscribe/${id}`,{},
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
        const user = response.data.user  
        localStorage.setItem('user_info',JSON.stringify(user));
        console.log('Subscribed successfully');
        this.toast.success("Subscribed successfully!!");
        this.$router.go(0);
        })
        .catch(error => {
          console.error('Error found', error);
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

.subscription-container {
    width: 800px;
    height: 660px;
    background: transparent;
    border: 0;
    backdrop-filter: blur(20px);
    color: white;
    border-radius: 10px;
    padding: 150px;
    box-shadow: 0 0 50px 25px rgb(0, 0, 0);
    text-align:center;
}
h1{
    font-size: 36px;
    text-align: center;
    text-shadow: 3px 3px 8px rgb(238, 255, 0);
}
.button{
  width:100%;
  height:60px;
  background: rgba(168, 29, 29, 0.521);
  border:none;
  outline:none;
  color:white;
  border-radius: 4px;
  cursor:pointer;
  font-weight:1000;
  font-size:larger;
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}
h3{
  text-shadow: 3px 3px 8px rgb(255, 0, 0);
}
h4,p{
  text-shadow: 3px 3px 8px rgb(0, 0, 0)
}
</style>