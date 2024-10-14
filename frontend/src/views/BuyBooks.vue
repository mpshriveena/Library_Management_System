<template>
    <div>
      <section class="vh-100">
  <div class="container py-5 h-200">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-lg-14 col-xl-12">
        <div class="card rounded-3">
          <div class="card-body p-4">
  
            <h4 class="text-center my-3 pb-3">Bought Books</h4>
            <p>Hello Librarian!! You can view the books bought by the users.</p>

            <table class="table mb-4">
                <thead>
                    <tr>
                      
                      <th scope="col">Request ID</th>
                      <th scope="col">User ID</th>
                      <th scope="col">User Name</th>
                      <th scope="col">Book ID</th>
                      <th scope="col">Book Title</th>
                      <th scope="col">Price</th>
                      <th scope="col">Bought on</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="buybook in buybooks" v-bind:key="buybook.id">
                      
                      <td>{{ buybook.id}}</td>
                      <td>{{ buybook.user_id}}</td>
                      <td>{{ buybook.username}}</td>
                      <td>{{buybook.book_id}}</td>
                      <td>{{buybook.book_title}}</td>
                      <td>{{buybook.price}}</td>
                      <td>{{buybook.bought_on}}</td>
                    </tr>
                </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
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
        buybooks:[],
      };
    },
    mounted() {
      this.getBuybooks();
    },
    methods: {
      getBuybooks(){
        const accesstoken = localStorage.getItem("access_token");
      axios.get('http://127.0.0.1:5000/buybooks',
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.buybooks = response.data.buybooks;
        })
        .catch(error => {
          console.error('Error found', error);
        });
    }, 
  }
  }
  </script>
  
    
  <style>
    
  </style>