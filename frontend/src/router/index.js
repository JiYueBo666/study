import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Login from "../views/Login.vue";
import CreateArticle from "../views/CreateArticle.vue";

const routes = [
	{
		path: "/",
		name: "Home",
		component: Home,
	},
	{
		path: "/login",
		name: "Login",
		component: Login,
	},
	{
		path: "/create",
		name: "CreateArticle",
		component: CreateArticle,
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

export default router;
