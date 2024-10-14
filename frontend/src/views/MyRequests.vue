<template>
  <div>
    <section class="vh-100">
      <div class="container py-5 h-200">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col col-lg-14 col-xl-12">
            <div class="card rounded-3">
              <div class="card-body p-4">
                <h4 class="text-center my-3 pb-3">My Requests</h4>
                <p>Here are the books you requested for..</p>
                <table class="table mb-4">
                  <thead>
                    <tr>
                      <th scope="col">Request ID</th>
                      <th scope="col">Book ID</th>
                      <th scope="col">Book Title</th>
                      <th scope="col">Days</th>
                      <th scope="col">Status</th>
                      <th scope="col">Requested on</th>
                      <th scope="col">Granted on</th>
                      <th scope="col">Rejected on</th>
                      <th scope="col">Returned on</th>
                      <th scope="col">Book</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="myrequest in myrequests" :key="myrequest.id">
                      <td>{{ myrequest.id }}</td>
                      <td>{{ myrequest.book_id }}</td>
                      <td>{{ myrequest.book_title }}</td>
                      <td>{{ myrequest.days }}</td>
                      <td>{{ myrequest.status }}</td>
                      <td>{{ myrequest.requested_on }}</td>
                      <td>{{ myrequest.granted_on }}</td>
                      <td>{{ myrequest.rejected_on }}</td>
                      <td>{{ myrequest.returned_on }}</td>
                      <td>
                        <div v-if="myrequest.status === 'granted'" class="d-flex">
                            <button class="btn btn-success me-3" @click='readBook(myrequest.book_id)'>Read</button>
                            <button class="btn btn-danger" @click="returnbook(myrequest.id)">Return</button>
                          </div>
                          <div v-else-if="myrequest.status === 'Access Revoked'">
                            <button class="btn btn-outline-secondary disabled">Access Revoked</button>
                          </div>
                          <div v-else-if="myrequest.status === 'pending'">
                            <button class="btn btn-danger" @click="withdrawrequest(myrequest.id)">Withdraw Request</button>
                          </div>
                          <div v-else-if="myrequest.status === 'rejected'">
                            <button class="btn btn-danger disabled">Rejected</button>
                          </div>
                          <div v-else-if="myrequest.status === 'returned'">
                            <button class="btn btn-outline-danger disabled">Returned</button>
                          </div>
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
      myrequests: [],
      user_id: JSON.parse(localStorage.getItem('user_info')).user_id,
    };
  },
  mounted() {
    this.getmyRequests();
  },
  methods: {
    getmyRequests(){
      const accesstoken = localStorage.getItem("access_token");
      axios.get('http://127.0.0.1:5000/myrequests/', {
        params: {
          user_id: this.user_id,
        },
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.myrequests = response.data.myrequests;
        })
        .catch(error => {
          console.error('Error found', error);
        });
    },
    withdrawrequest(id) {
      const accesstoken = localStorage.getItem("access_token");
      axios.delete(`http://127.0.0.1:5000/withdrawrequest/${id}/`, { params: { user_id: this.user_id },headers: {
          Authorization: `Bearer ${accesstoken}`
        } })
        .then(response => {
          const user = response.data.user  
          localStorage.setItem('user_info',JSON.stringify(user));
          console.log('Book withdrawn successfully');
          this.toast.success("Book withdrawn successfully!!");

        setTimeout(() => {
          this.$router.go(0);
        }, 1000);
        })
        .catch(error => {
          console.error('Error withdrawing request:', error);
          alert(error.response.data.message);
        });
    },
    readBook(book_id) {
      axios.get(`http://127.0.0.1:5000/book/${book_id}`)
      .then(response => {
        const filePath = response.data.file_path;
        this.toast.warning("Opening book");
        window.open(`http://127.0.0.1:5000/${filePath}`, '_blank');
      })
      .catch(error => {
        console.error('Error fetching book file:', error);
      });
    },
    returnbook(id) {
      const accesstoken = localStorage.getItem("access_token");
      axios.put(`http://127.0.0.1:5000/returnbook/${id}`,{},
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        this.$router.go(0);
        this.toast.success("Book returned successfully!!");

      })
      .catch(error => {
        console.error('Error found', error);
        this.toast.error("Error returning book");
      });
    },
  },
};
</script>

<style scoped>
</style>