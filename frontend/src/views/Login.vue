<template>
	<div class="login-container">
		<el-card class="login-card">
			<h2>登录</h2>
			<el-form :model="loginForm" @submit.prevent="handleLogin">
				<el-form-item>
					<el-input v-model="loginForm.username" placeholder="用户名" />
				</el-form-item>
				<el-form-item>
					<el-input v-model="loginForm.password" type="password" placeholder="密码" />
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="handleLogin" style="width: 100%">
						登录
					</el-button>
				</el-form-item>
			</el-form>
		</el-card>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api";
import { ElMessage } from "element-plus";

const router = useRouter();
const loginForm = ref({
	username: "",
	password: "",
});

const handleLogin = async () => {
	try {
		console.log("开始登录请求");
		console.log("登录表单数据:", loginForm.value);

		// 测试API连接
		try {
			await api.get("/");
			console.log("API 连接测试成功");
		} catch (error) {
			console.error("API 连接测试失败:", error);
			ElMessage.error("无法连接到服务器，请检查后端服务是否运行");
			return;
		}

		const response = await api.post("/api/v1/auth/login", loginForm.value);
		console.log("登录响应:", response.data);

		localStorage.setItem("token", response.data.access_token);
		ElMessage.success("登录成功");
		router.push("/");
	} catch (error) {
		console.error("登录错误详情:", {
			status: error.response?.status,
			statusText: error.response?.statusText,
			data: error.response?.data,
			message: error.message,
			config: {
				url: error.config?.url,
				method: error.config?.method,
				baseURL: error.config?.baseURL,
				headers: error.config?.headers,
			},
		});

		if (!error.response) {
			ElMessage.error("网络错误，请检查后端服务是否运行");
		} else {
			ElMessage.error(error.response.data?.detail || "登录失败");
		}
	}
};
</script>

<style scoped>
.login-container {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
	background-color: #f5f5f5;
}
.login-card {
	width: 400px;
}
</style>
