<template>
    <div class="sections">
      <div class="section-container">
    <button @click="exportCSV" class="button1">
      Export Books and Request Details to CSV
    </button><br><br>
      <h1>Sections</h1><br>
      <button class="button" @click='createSection'>Create Section</button>
      <br><br>
      <div v-if="sections.length > 0">
      <div v-for="section in sections" v-bind:key="section.id" class="section-item">
          <h2>ID:{{section.id}} {{section.sec_title}}</h2>
          <p>Date Created: {{section.date_created}}</p>          
          <p>{{section.sec_description}}</p>
          <button class="btn btn-success me-3" @click='editSection(section.id,section.sec_title,section.sec_description)'>Edit Section</button>
          <button class="btn btn-success me-3" @click='viewBooks(section.id)'>View Books</button>
          <button class="btn btn-danger" @click='deleteSection(section.id)'>Delete</button>
      </div>
    </div>
    <p v-else class="pwhite">No sections added yet..</p>
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
      sections:[],
      access_token: localStorage.getItem('access_token'),
    };
  },
  mounted() {
    this.getSections();
  },
  methods: {
    exportCSV() {
      this.triggerexportCSV();
    },
    async triggerexportCSV() {
      try {
        const response = await axios.post(`http://127.0.0.1:5000/export_csv`);
        if (response.data.success) {
          this.toast.success("Export job has been triggered. You will receive an email once it is complete.");
        } else {
          this.toast.error("Failed to trigger export job. Please try again.");
        }
      } catch (error) {
        this.toast.error("An error occurred. Please try again.");
      }
    },
    createSection(){
      this.$router.push({ path: `/createsection` });
    },
    getSections(){
      const accesstoken = localStorage.getItem("access_token");
    axios.get('http://127.0.0.1:5000/home',
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        this.sections = response.data.sections;
      })
      .catch(error => {
        console.error('Error found', error);
      });
  },

  deleteSection(id){
    const accesstoken = localStorage.getItem("access_token");
    axios.delete(`http://127.0.0.1:5000/deletesection/${id}`,
        {
        headers: {
          Authorization: `Bearer ${accesstoken}`
        }
      })
      .then(response => {
        console.log('Section deleted successfully',response);
        this.toast.success("Section deleted successfully");
        window.location.reload();
      })
      .catch(error => {
        console.error('Error found', error);
      });
  },
  viewBooks(id) {
  
      this.$router.push({ path: `/section/${id}/book` });
    },
    editSection(id, sec_title, sec_description) {
  
      this.$router.push({
        name: 'EditSection',
        params: { id: id, sec_title: sec_title, sec_description:sec_description }
      });
    },
}
}
</script>

  
<style scoped>

.section-container {
  padding: 20px;
}
.sections {
  
  padding:10px
}

.section-item {
  background: rgba(255, 255, 255);
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
.section-item:hover{
  transform: scale(1.01);
}

.section-item h2 {
  margin-bottom: 10px;
}

.section-item p {
  margin-bottom: 20px;
}
.button{
  width:10%;
  height:50px;
  background: rgba(168, 29, 29, 1);
  border:none;
  outline:none;
  color:white;
  border-radius: 4px;
  cursor:pointer;
  font-weight:500;
  font-size:20px;
  text-shadow: 3px 3px 8px rgb(238, 255, 0); 
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}
.button1{
  width:25%;
  height:50px;
  background: rgb(3, 97, 8);
  border:none;
  outline:none;
  color:white;
  border-radius: 10px;
  cursor:pointer;
  font-weight:500;
  font-size:20px;
  text-shadow: 3px 3px 8px rgb(238, 255, 0); 
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}
h1{
  text-shadow: 3px 3px 8px rgb(238, 255, 0);
  color:white;
}
.pwhite{
  color:white;
}
.button:hover{
  background: rgb(109, 2, 2);
}
.button1:hover{
  background: rgb(2, 58, 4);
}
</style>