import { createRouter, createWebHistory } from "vue-router";
import UserChats from "./components/UserChats.vue";
import LoginPage from "./components/LoginPage.vue";

const routes = [
    {
        path: "/",
        name: "home",
        component: LoginPage
    },
    {
        path: "/user_chats/:id",
        name: "user-chats",
        component: UserChats
    },
];

const router = createRouter(
    {
        history: createWebHistory(),
        routes,
    }
)

export default router;