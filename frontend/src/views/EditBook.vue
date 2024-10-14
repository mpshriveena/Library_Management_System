<template>
    <div class="body">
    <div class="inputbox">
      <h2>Edit Book</h2>
      <br>
      <p>Title</p>
          <input type="text" id="book_title" placeholder="Title" v-model='book_title' required/>
          <br>   <br>
          <p>Author</p>    
          <input type="text" id="author" placeholder="Author" v-model='author'/>
          <br>   <br> 
          <p>Description</p>  
          <textarea type="text" id="book_description" placeholder="Description" v-model='book_description' required></textarea>
          <br>   <br>
          <p>Price (Enter price if you wnat to change it)</p>    
          <input type="number" id="price" placeholder="Price" v-model='price'/>
          <br>   <br>  
          <p>Upload Book Image (if you want to change existing image)</p>
    <input type="file" name="bookimage" id="bookimage" @change="onFileChange($event, 'bookimage')" class="upload-box"/>
    <br>   <br> 
    <p>Upload Book PDF (if you want to change existing pdf)</p>
    <input type="file" name="bookpdf" id="bookpdf" @change="onFileChange($event, 'bookpdf')" class="upload-box"/>
    <br>   <br> 
          <button type="submit" @click="updateBook" class="button">Update Book</button>
      </div>
      </div>
  </template>

  <script>
import axios from 'axios'
import { useToast } from 'vue-toastification';

export default {
    props: ['book'],
    setup() {
    const toast = useToast();

    return {
      toast
    };
  },
    data() {
        return {
            id: this.$route.params.id,
            book_title: this.$route.params.book_title,
            book_description: this.$route.params.book_description,
            author: this.$route.params.author,
            price: '',
            bookimage:null,
            bookpdf:null,
        };
        },

    
    methods: {
        onFileChange(event, type) {
      if (type === 'bookpdf') {
        this.bookpdf = event.target.files[0];
      } else if (type === 'bookimage') {
        this.bookimage = event.target.files[0];
      }
    },
        updateBook() {
            const formData = new FormData();
            const accesstoken = localStorage.getItem("access_token");
            formData.append("book_title", this.book_title);
            formData.append("book_description", this.book_description);
            formData.append("author", this.author);
            formData.append("price", this.price);
            formData.append("id", this.id);
            formData.append('bookimage', this.bookimage);
            formData.append('bookpdf', this.bookpdf);
           console.log(formData);
            
            axios.put(`http://127.0.0.1:5000/book/edit/${this.id}`, formData,
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
                .then(() => {
                  this.toast.success("Book edited successfully!!");
                    this.$router.go(-1);
                })
                .catch(error => {
        console.error('Error found', error);
        this.toast.error("Error in editing book");
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
  text-shadow: 3px 3px 8px rgb(0, 0, 1);
}
p{
  text-shadow: 3px 3px 8px rgb(0, 0, 1);

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
  height: 150px;
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
.button:hover{
  background:#861a1a;
}
upload-box{
  font-size:16px;
  background:white;
  border-radius: 50px;
  box-shadow: 5px 5px 10px black;
  width:500px;
  outline:none;
}
::-webkit-file-upload-button{
  color:white;
  background: #b60202a1;
  padding:3px;
  width:130px;
  border:none;
  box-shadow:1px 0 1px 1px #6b4559;
  border-radius: 50px;
  outline:none;
}
::-webkit-file-upload-button:hover{
  background:#861a1a;
}
</style>
