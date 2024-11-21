<template>
	<div class="home-container">
		<el-container>
			<el-header>
				<div class="header-content">
					<h1>个人博客</h1>
					<div class="header-buttons">
						<el-button v-if="!token" @click="$router.push('/login')">登录</el-button>
						<template v-else>
							<el-button @click="$router.push('/create')">写文章</el-button>
							<el-button @click="handleLogout">退出</el-button>
						</template>
					</div>
				</div>
			</el-header>
			<el-main>
				<div class="article-list">
					<el-card v-for="article in articles" :key="article.id" class="article-card">
						<h2>{{ article.title }}</h2>
						<markdown-viewer :content="article.content" />
						<div class="article-meta">
							<span>
								发布时间: {{ new Date(article.created_at).toLocaleString() }}
							</span>
						</div>
					</el-card>
				</div>
			</el-main>
		</el-container>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api";
import MarkdownViewer from "../components/MarkdownViewer.vue";

const router = useRouter();
const articles = ref([]);
const token = ref(localStorage.getItem("token"));

const fetchArticles = async () => {
	try {
		const response = await api.get("/api/v1/articles");
		articles.value = response.data;
	} catch (error) {
		console.error("获取文章失败:", error);
	}
};

const handleLogout = () => {
	localStorage.removeItem("token");
	token.value = null;
	router.push("/login");
};

onMounted(() => {
	fetchArticles();
});
</script>

<style scoped>
.home-container {
	min-height: 100vh;
	background-color: #f5f5f5;
}
.header-content {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0 20px;
}
.article-list {
	max-width: 800px;
	margin: 0 auto;
}
.article-card {
	margin-bottom: 20px;
}
.article-meta {
	margin-top: 10px;
	color: #666;
	font-size: 0.9em;
}
</style>
