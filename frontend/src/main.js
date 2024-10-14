import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

import axios from 'axios'

axios.defaults.baseURL = 'http//127.0.0.1.5000'

const axiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000', 
  });

axiosInstance.interceptors.request.use(
    (config) => {
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        config.headers['Authorization'] = `Bearer ${accessToken}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
const app = createApp(App)
app.use(Toast, {
  // You can customize the options here
  position: "top-right",   // Position of the toast
  timeout: 5000,           // Duration of the toast
  closeOnClick: true,      // Close the toast when clicked
  pauseOnFocusLoss: true,  // Pause the toast when window loses focus
  pauseOnHover: true,      // Pause the toast when hovered
  draggable: true,         // Enable drag-to-close functionality
  draggablePercent: 0.6,   // Percentage of toast's width required to drag
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false
});

app.config.globalProperties.$axios = axiosInstance;



app.use(router)

app.mount('#app')
