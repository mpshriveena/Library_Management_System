<template>
  <div class='body'>
        <div class="signup-box">
        <form @submit.prevent="SignUp">
          <h1><strong>Register</strong></h1>
          <div class = "inputbox">
            <input type="text" id="username" placeholder="name" v-model="username" required>
            <label>Username</label>

          </div>
            <div class = "inputbox">
              <input type="email" id="email" placeholder="name@example.com" v-model="email" required>
              <label>Email</label>

            </div>
            <div class = "inputbox">
              <input type="password" id="password" v-model="password" required>
              <label>Password</label>
            </div>
            <button class="button" @click='SignUp'> Register </button>
            <div class="login-link">
            <p>Already have an account? <router-link to="/"><a>Login</a></router-link> </p>
          </div>
          </form>
          <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
          </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToast } from 'vue-toastification';

export default{
  data(){
    return{
      username:'',
      email:'',
      password:'',
      role:'user',
      errorMessage:'',
    };
  },
  methods:{
    async SignUp(){
      try{
        await axios.post('http://127.0.0.1:5000/register',{
          username: this.username,
          email: this.email,
          password: this.password,
          role:this.role
        });
        this.$router.push('/');
        
      } catch(error){
        this.errorMessage = error.response.data.message
      }
    }
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

.signup-box {
    width: 420px;
    background: transparent;
    border: 0;
    backdrop-filter: blur(20px);
    color: white;
    border-radius: 10px;
    padding: 30px 40px;
    box-shadow: 0 0 50px 25px rgb(0, 0, 0);
}

.signup-box h1 {
    font-size: 36px;
    text-align: center;
    text-shadow: 3px 3px 8px rgb(238, 255, 0); 

}

.signup-box .inputbox{
  position:relative;
  width:340px;
  height: 50px;
  border-bottom:2px solid white;
  margin: 30px 0;
}

.inputbox input{
  width:100%;
  height: 100%;
  background:transparent;
  border:none;
  outline: none;
  color: white;
}
.inputbox input::placeholder {
    color: rgba(2, 2, 2, 0.233);
}
.inputbox label{
  position:absolute;
  top:50%;
  left:0;
  transform: translateY(-50%);
  font-size: 16px;
  font-weight: 500;
  pointer-events: 500;
  transition: .5s ease;
}
.inputbox input:focus~label,
.inputbox input:valid~label{
  top:-5px;
}

.signup-box .button{
  width:100%;
  height:45px;
  background: rgba(168, 29, 29, 0.521);
  border:none;
  outline:none;
  color:white;
  border-radius: 4px;
  cursor:pointer;
  font-weight:500;
  text-shadow: 3px 3px 8px rgb(238, 255, 0); 
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}
.login-link{
  font-size: 14.5px;
  font-weight: 500;
  text-align: center;
  margin-top: 25px;
  color: white;
}
.login-link a {
  color: white;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline; 
}
.error-message{
  text-align:center;
}


</style>
