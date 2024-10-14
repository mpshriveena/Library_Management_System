<template>
    <div class="body">
        <div class="inputbox">
            <h2>Edit Section</h2>
      <br>
      <p>Title</p>
          <input type="text" id="sec_title" placeholder="title" v-model='sec_title' required/>
          <br>   <br> 
    <p>Description</p>
          <textarea type="text" id="sec_description" placeholder="Description" v-model='sec_description' required></textarea>
          <br>  <br>  
          <button type="submit" @click="updateSection" class="button">Update Section</button>
      </div>
    </div>
  </template>

  <script>
import axios from 'axios'
import { useToast } from 'vue-toastification';

export default {
    props: ['section'],
    setup() {
    const toast = useToast();

    return {
      toast
    };
  },
    data() {
        return {
            id: this.$route.params.id,
            sec_title: this.$route.params.sec_title,
            sec_description: this.$route.params.sec_description,
        };
        },

    
    methods: {
        updateSection() {
            const formData = new FormData();
            const accesstoken = localStorage.getItem("access_token");
            formData.append("sec_title", this.sec_title);
            formData.append("sec_description", this.sec_description);
            formData.append("id", this.id);
           
            
            axios.put(`http://127.0.0.1:5000/section/edit/${this.id}`, formData,
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
                .then(() => {
                  this.toast.success("Section edited successfully!!");
                    this.$router.push(`/home`);
                })
                .catch(error => {
        console.error('Error found', error);
        this.toast.error("Error in editing section");
      });

    },
        
    },
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

.inputbox {
    width: 900px;
    height:auto;
    background: transparent;
    border: 0;
    backdrop-filter: blur(20px);
    color: white;
    border-radius: 10px;
    padding: 30px 40px;
    box-shadow: 0 0 50px 25px rgb(0, 0, 0);
}
h2{
  text-align: center;
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
}
.inputbox input{
  width:100%;
  height: 50px;
  border-radius: 10px;
  border-color: rgb(255, 255, 255);
  background: transparent;
  border-width:2px;
  color: white;
  padding:20px;
}
.inputbox textarea{
  width:100%;
  height: 300px;
  background: transparent;
  color: white;
  border-radius: 10px;
  border-color: rgb(255, 255, 255);
  border-width:2px;
  padding:10px;
}
.button{
  width:100%;
  height:60px;
  background: rgba(168, 29, 29, 1);
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
</style>