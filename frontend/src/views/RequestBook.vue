<template>
    <div class="body">
      <div class="request-container">
          <h3>Are you sure you wanna request the book "{{ requestedbook.book_title }}"?</h3>
         <br> <p><strong>By: </strong> {{ requestedbook.author }}</p>
          <br><p><strong>Description:</strong> {{ requestedbook.book_description }}</p>
         <br> 
         <div class="inputbox">
         <input type="number" id="days" placeholder="Days" v-model='days'/>
         <label>Days</label>
          <br><br><br><button class="button" @click='requestedBookandDay(requestedbook.id, requestedbook.book_title)'>Request</button>
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
        requestedbook: {},
        days:0,
        user_info: null,
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
        message: '',
      };
    },
    created() {
      this.getRequestedbook(this.id);
      this.user_info = localStorage.getItem('user_info');
      this.user_id= JSON.parse(localStorage.getItem('user_info')).user_id;

    },
  
    methods: {
      getRequestedbook(id) {
        const accesstoken = localStorage.getItem("access_token");
        axios.get(`http://127.0.0.1:5000/requestbook/${id}`, {params:{ user_id: this.user_id },headers: {
          Authorization: `Bearer ${accesstoken}`
        }})
          .then(response => {
            this.requestedbook = response.data.requestedbook;
            console.log(JSON.parse(this.user_info).user_id);
          })
          .catch(error => {
            console.error('Error fetching books:', error);
          });
      },
      
      requestedBookandDay(id, book_title) {
        const formData = {
        book_id: id,
        book_title: book_title,
        days: this.days,
        user_id:JSON.parse(this.user_info).user_id,
        username:JSON.parse(this.user_info).username,
      };
      const accesstoken = localStorage.getItem("access_token");
      console.log('Form Data:', formData);
      axios.post('http://127.0.0.1:5000/requestbook/',formData,
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        const user = response.data.user  
        localStorage.setItem('user_info',JSON.stringify(user));
        console.log('Book requested successfully');
        this.$router.go(-1);
        this.toast.success("Book requested successfully!!");
      })
      .catch(error => {
        console.error('Error requesting book:', error);
      });
    },
  }
};
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

.request-container {
    width: 1500px;
    height: auto;
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
  width:80%;
  height:40px;
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

h4,p{
  text-shadow: 3px 3px 8px rgb(0, 0, 0)
}
.inputbox{
  position:relative;
  left:430px;
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

</style>