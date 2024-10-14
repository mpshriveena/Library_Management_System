<template>
    <div>
      <section class="vh-100">
        <div class="container py-5 h-200">
          <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col col-lg-12 col-xl-10">
              <div class="card rounded-3">
                <div class="card-body p-4">
                  <h4 class="text-center my-3 pb-3">My Books</h4>
                  <p>Here are the books which you bought from our website..</p>
                  <table class="table mb-4">
                    <thead>
                      <tr>
                        <th scope="col">Buy ID</th>
                        <th scope="col">Book ID</th>
                        <th scope="col">Book Title</th>
                        <th scope="col">Price</th>
                        <th scope="col">Bought on</th>
                        <th scope="col">Book</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="mybook in mybooks" :key="mybook.id">
                        <td>{{ mybook.id }}</td>
                        <td>{{ mybook.book_id }}</td>
                        <td>{{ mybook.book_title }}</td>
                        <td>{{ mybook.price }}</td>
                        <td>{{ mybook.bought_on }}</td>
                        <td>
                              <button class="btn btn-success me-3" @click='readBook(mybook.book_id)'>Read</button>
                        </td>
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
        mybooks: [],
        user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
      };
    },
    mounted() {
      this.getmyBooks();
    },
    methods: {
      getmyBooks(){
        const accesstoken = localStorage.getItem("access_token");
        axios.get('http://127.0.0.1:5000/mybooks/', {
          params: {
            user_id: this.user_id,
          },
          headers: {
            Authorization: `Bearer ${accesstoken}`
          }
        })
          .then(response => {
            this.mybooks = response.data.mybooks;
          })
          .catch(error => {
            console.error('Error found', error);
          });
      },
      readBook(book_id) {
        axios.get(`http://127.0.0.1:5000/book/${book_id}`)
        .then(response => {
          const filePath = response.data.file_path;
          window.open(`http://127.0.0.1:5000/${filePath}`, '_blank');
          this.toast.warning("Opening Book");
        })
        .catch(error => {
          console.error('Error fetching book file:', error);
          this.toast.error("Error opening book!!");
        });
      },
    },
  };
  </script>
  
  <style scoped>
  </style>