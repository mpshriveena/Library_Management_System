<template>
    <div>
      <section class="vh-100">
  <div class="container py-5 h-200">
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col col-lg-14 col-xl-12">
        <div class="card rounded-3">
          <div class="card-body p-4">
  
            <h4 class="text-center my-3 pb-3">Requests</h4>
            <p>Hello Librarian!! You can view the requests of users and grant them or reject them here.</p>

            <table class="table mb-4">
                <thead>
                    <tr>
                      
                      <th scope="col">Request ID</th>
                      <th scope="col">User ID</th>
                      <th scope="col">User Name</th>
                      <th scope="col">Book ID</th>
                      <th scope="col">Book Title</th>
                      <th scope="col">Days</th>
                      <th scope="col">Status</th>
                      <th scope="col">requested_on</th>
                      <th scope="col">granted_on</th>
                      <th scope="col">rejected_on</th>
                      <th scope="col">returned_on</th>
                      <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in requests" v-bind:key="request.id">
                      
                      <td>{{ request.id}}</td>
                      <td>{{ request.user_id}}</td>
                      <td>{{ request.username}}</td>
                      <td>{{request.book_id}}</td>
                      <td>{{request.book_title}}</td>
                      <td>{{ request.days }}</td>
                      <td>{{request.status}}</td>
                      <td>{{ request.requested_on}}</td>
                      <td>{{request.granted_on}}</td>
                      <td>{{request.rejected_on}}</td>
                      <td>{{request.returned_on}}</td>

                      <td>
                        <div v-if="request.status === 'pending'" class="d-flex">
                          <button class="btn btn-success me-3" @click="grantRequest(request.id)">Grant</button>
                          <button class="btn btn-danger" @click="rejectRequest(request.id)">Reject</button>
                        </div>
                        <div v-else-if="request.status === 'granted'">
                          <button class="btn btn-danger" @click="revokeRequest(request.id)">Revoke</button>
                          </div>
                          <div v-else-if="request.status === 'rejected'">
                            <button class="btn btn-danger disabled">Rejected</button>
                          </div>
                          <div v-else-if="request.status === 'Access Revoked'">
                            <button class="btn btn-outline-secondary disabled">Access Revoked</button>
                          </div>
                          <div v-else-if="request.status === 'returned'">
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
        requests:[],
      };
    },
    mounted() {
      this.getRequests();
    },
    methods: {
      getRequests(){
        const accesstoken = localStorage.getItem("access_token");
      axios.get('http://127.0.0.1:5000/requests',
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.requests = response.data.requests;
        })
        .catch(error => {
          console.error('Error found', error);
        });
    }, 

    grantRequest(id){
      const accesstoken = localStorage.getItem("access_token");
      axios.put(`http://127.0.0.1:5000/grantrequest/${id}`,{},
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.toast.success("Request granted successfully!!");
          this.$router.go(0);
        })
        .catch(error => {
          console.error('Error found', error);
        });
    },

    rejectRequest(id){
      const accesstoken = localStorage.getItem("access_token");
      axios.put(`http://127.0.0.1:5000/rejectrequest/${id}`,{},
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.toast.success("Request rejected successfully!!");
          this.$router.go(0);
        })
        .catch(error => {
          console.error('Error found', error);
        });
    }, 

    revokeRequest(id){
      const accesstoken = localStorage.getItem("access_token");
      axios.put(`http://127.0.0.1:5000/revokerequest/${id}`,{},
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
        .then(response => {
          this.toast.success("Access revoked successfully!!");
          this.$router.go(0);
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