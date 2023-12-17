import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.css';
import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/LoginPage.vue';
import Chats from './components/ChatWindow.vue';

const app = createApp(App);

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/ChatWindow', component: Chats },
  ],
});

app.use(router);

app.mount("#app");
