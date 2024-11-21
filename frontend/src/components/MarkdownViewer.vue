<template>
	<div class="markdown-body" v-html="renderedContent"></div>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import { marked } from "marked";
import hljs from "highlight.js";
import katex from "katex";
import "highlight.js/styles/github.css";
import "katex/dist/katex.min.css";
import "./markdown.css"; // 我们将创建这个样式文件

const props = defineProps({
	content: {
		type: String,
		required: true,
		default: "",
	},
});

// 处理数学公式
function processMath(text) {
	if (typeof text !== "string") {
		console.warn("非字符串输入:", text);
		return String(text || "");
	}

	// 处理块级数学公式
	text = text
		.split("$$")
		.map((part, index) => {
			if (index % 2 === 1) {
				try {
					return katex.renderToString(part, {
						displayMode: true,
						throwOnError: false,
					});
				} catch (e) {
					console.error("块级公式渲染失败:", e);
					return part;
				}
			}
			return part;
		})
		.join("");

	// 处理行内数学公式
	text = text
		.split("$")
		.map((part, index) => {
			if (index % 2 === 1) {
				try {
					return katex.renderToString(part, {
						displayMode: false,
						throwOnError: false,
					});
				} catch (e) {
					console.error("行内公式渲染失败:", e);
					return part;
				}
			}
			return part;
		})
		.join("");

	return text;
}

// 配置 marked
const renderer = {
	text(text) {
		try {
			return processMath(text);
		} catch (e) {
			console.error("文本处理失败:", e);
			return String(text || "");
		}
	},

	code(code, language) {
		try {
			if (language && hljs.getLanguage(language)) {
				return hljs.highlight(code, { language }).value;
			}
			return hljs.highlightAuto(code).value;
		} catch (e) {
			console.error("代码高亮失败:", e);
			return code;
		}
	},

	// 添加其他必要的渲染方法
	paragraph(text) {
		return "<p>" + text + "</p>";
	},

	heading(text, level) {
		return `<h${level}>${text}</h${level}>`;
	},
};

marked.use({
	renderer,
	breaks: true,
	gfm: true,
	mangle: false,
	headerIds: false,
});

const renderedContent = ref("");

watchEffect(() => {
	try {
		if (!props.content) {
			renderedContent.value = "";
			return;
		}

		console.log("开始渲染内容:", props.content);
		const processed = processMath(props.content);
		renderedContent.value = marked(processed);
		console.log("渲染完成");
	} catch (e) {
		console.error("Markdown渲染失败:", e);
		renderedContent.value = props.content || "";
	}
});
</script>

<style>
@import "./markdown.css";
@import "katex/dist/katex.min.css";

.markdown-body {
	padding: 20px;
	line-height: 1.6;
}

.markdown-body pre {
	background-color: #f6f8fa;
	padding: 16px;
	border-radius: 6px;
	overflow: auto;
}

.markdown-body code {
	font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
}

.markdown-body .katex-display {
	margin: 1em 0;
	overflow-x: auto;
	overflow-y: hidden;
}

.markdown-body blockquote {
	padding: 0 1em;
	color: #6a737d;
	border-left: 0.25em solid #dfe2e5;
}

.markdown-body table {
	border-spacing: 0;
	border-collapse: collapse;
	margin: 1em 0;
}

.markdown-body table th,
.markdown-body table td {
	padding: 6px 13px;
	border: 1px solid #dfe2e5;
}

.markdown-body table tr:nth-child(2n) {
	background-color: #f6f8fa;
}
</style>
