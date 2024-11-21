import axios from "axios";

const api = axios.create({
	baseURL: "http://localhost:8000",
	timeout: 5000,
	headers: {
		"Content-Type": "application/json",
	},
});

// 添加请求拦截器用于调试
api.interceptors.request.use(
	config => {
		console.log("发送请求:", config);
		return config;
	},
	error => {
		console.error("请求错误:", error);
		return Promise.reject(error);
	}
);

// 添加响应拦截器用于调试
api.interceptors.response.use(
	response => {
		console.log("收到响应:", response);
		return response;
	},
	error => {
		console.error("响应错误:", error);
		return Promise.reject(error);
	}
);

export default api;
