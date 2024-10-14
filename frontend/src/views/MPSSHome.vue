<template>
<div class="home">
 
    <div class="hello">
      <div class="content">
        <h2 class="logo"><strong><i class='bx bxl-firebase'></i> M.P.S.S Knowledge Junction</strong></h2>
      </div>
        <div class="text-sci">
          <h1> Welcome ! !<br><strong> To our Virtual Library</strong></h1>
          <p>Library is the storehouse of knowledge.
           We aim to provide quality books to be read by the user anywhere, anytime!!
          You can request for books to read. These books are very useful
        for book lovers and knowledge seekers. Please use the "About" page 
      to know how to use this website. Happy Learning!!</p>
        </div>
    </div>
    <div class="login">
        <div class="form-box">
        <form @submit.prevent="LogIn">
          <h2><strong>Login</strong></h2>
          <div class="input-box">
            <input type="email" id="email" placeholder="name@example.com" v-model='email' required>
            <label>Email</label>
          </div>
          <div class="input-box">
            <input type="password" id="password" v-model='password' required>
            <label>Password</label>
          </div>
          
            <button type="submit" class="button" @click='LogIn'> Login </button>
          
          <div class="register-link">
            <p>Don't have an account? <router-link to="/register"><a>Register</a></router-link> </p>
          </div>
          <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
          </div>
        </form>
        
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
  data(){
    return{
      email:'',
      password:'',
      errorMessage:'',
    };
  },
  mounted(){
    const backgroundImageURL = `../public/background2.jpg`;
    document.body.style.backgroundImage = `url(${backgroundImageURL})`;
    localStorage.setItem('backgroundImage', backgroundImageURL);
  },
  methods:{
      LogIn(){
        this.$axios.post('http://127.0.0.1:5000/', {
          email: this.email,
          password: this.password
        }).then(response => {
  const user = response.data.user
  
  const access_token = response.data.access_token
  const backgroundImageURL = `../public/background2.jpg`;
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('user_info',JSON.stringify(user));
  localStorage.setItem('backgroundImage', backgroundImageURL);
  document.body.style.backgroundImage = `url(${backgroundImageURL})`;
  window.location.reload();
  this.toast.success("Login successful!!");
  this.$router.push('/home');
}).catch(error => {
  this.errorMessage = error.response.data.message
});
       
    }
  }
}
</script>

<style scoped>
.home {
  margin:0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', 'sans-serif';
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url('../public/background2.jpg') no-repeat center center;
  background-size: cover;
  border-radius: 10px;
}

.hello .content{
  font-size:30px;

}
.home .hello{
  width:100%;
  height: 100%;
  background:transparent;
  padding: 12%;
  color:aliceblue;
}

.home .login{
  width:100%;
  height: 100%;
}

.hello .content h2 {
  font-size: 30px;
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
}

.text-sci h1 {
  font-size: 40px;
  text-shadow: 3px 3px 6px rgb(238, 255, 0); 
}

.text-sci p {
  font-size: 22px;
  margin: 20px 0;
  color: white;
  text-shadow: 5px 5px 15px rgba(0, 0, 0, 1);
  background-color: rgba(0, 0, 0, 0.137);
  padding: 10px;
  border-radius: 5px; 
}
.login .form-box{
  display:flex;
  justify-content:center;
  align-items:center;
  width:100%;
  height: 80%;
  background: transparent;
  backdrop-filter: blur(20px);
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  color:white;
}
.form-box h2{
  font-size:32px;
  text-align:center;
  text-shadow: 3px 3px 8px rgb(238, 255, 0); 

}
.form-box .input-box{
  position:relative;
  width:340px;
  height: 50px;
  border-bottom:2px solid white;
  margin: 30px 0;
}

.input-box input{
  width:100%;
  height: 100%;
  background:transparent;
  border:none;
  outline: none;
  color: white;
}

.input-box label{
  position:absolute;
  top:50%;
  left:0;
  transform: translateY(-50%);
  font-size: 16px;
  font-weight: 500;
  pointer-events: 500;
  transition: .5s ease;
}
.input-box input:focus~label,
.input-box input:valid~label{
  top:-5px;
}
.button{
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
.form-box .register-link, .error-message{
  font-size: 14.5px;
  font-weight: 500;
  text-align: center;
  margin-top: 25px;
  color: white;
}
.register-link a {
  color: white; 
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline; 
}

</style>
