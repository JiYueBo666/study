<template>
	<div class="create-container">
		<el-card class="create-card">
			<h2>写文章</h2>
			<el-form :model="articleForm" @submit.prevent="handleSubmit">
				<el-form-item>
					<el-input v-model="articleForm.title" placeholder="文章标题" />
				</el-form-item>
				<el-form-item>
					<div class="editor-container">
						<div class="editor">
							<el-input
								v-model="articleForm.content"
								type="textarea"
								:rows="15"
								placeholder="支持 Markdown 格式"
							/>
						</div>
						<div class="preview">
							<h3>预览</h3>
							<markdown-viewer :content="articleForm.content || ''" />
						</div>
					</div>
				</el-form-item>
				<el-form-item>
					<el-button type="primary" @click="handleSubmit">发布文章</el-button>
					<el-button @click="$router.push('/')">返回</el-button>
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
import MarkdownViewer from "../components/MarkdownViewer.vue";

const router = useRouter();
const articleForm = ref({
	title: "",
	content: "",
});

const handleSubmit = async () => {
	try {
		const token = localStorage.getItem("token");
		if (!token) {
			ElMessage.error("请先登录");
			router.push("/login");
			return;
		}

		console.log("发送文章数据:", {
			title: articleForm.value.title,
			content: articleForm.value.content,
		});

		const response = await api.post(
			"/api/v1/articles",
			{
				title: articleForm.value.title,
				content: articleForm.value.content,
			},
			{
				headers: {
					Authorization: `Bearer ${token}`,
					"Content-Type": "application/json",
				},
			}
		);

		console.log("发布成功:", response.data);
		ElMessage.success("发布成功");
		router.push("/");
	} catch (error) {
		console.error("发布失败:", {
			status: error.response?.status,
			data: error.response?.data,
			message: error.message,
			config: {
				url: error.config?.url,
				method: error.config?.method,
				headers: error.config?.headers,
				data: error.config?.data,
			},
		});
		ElMessage.error(error.response?.data?.detail || "发布失败");
	}
};
</script>

<style scoped>
.create-container {
	padding: 20px;
	max-width: 1200px;
	margin: 0 auto;
}

.editor-container {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 20px;
	margin-bottom: 20px;
}

.preview {
	border: 1px solid #dcdfe6;
	border-radius: 4px;
	padding: 20px;
	background-color: #fff;
	overflow-y: auto;
	max-height: 500px;
}

.editor {
	min-height: 300px;
}
</style>
