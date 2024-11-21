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

// 创建自定义渲染器
const renderer = {
	text(text) {
		if (!text) return "";

		try {
			// 处理行内数学公式
			text = text.replace(/\$([^\$]+)\$/g, (_, formula) => {
				try {
					return katex.renderToString(formula, { throwOnError: false });
				} catch (e) {
					console.error("行内公式渲染失败:", e);
					return formula;
				}
			});

			// 处理块级数学公式
			text = text.replace(/\$\$([^\$]+)\$\$/g, (_, formula) => {
				try {
					return katex.renderToString(formula, {
						displayMode: true,
						throwOnError: false,
					});
				} catch (e) {
					console.error("块级公式渲染失败:", e);
					return formula;
				}
			});

			return text;
		} catch (e) {
			console.error("文本处理失败:", e);
			return text || "";
		}
	},

	// 添加其他渲染方法
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
};

// 配置 marked
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

		console.log("渲染内容:", props.content);
		renderedContent.value = marked(props.content);
		console.log("渲染结果:", renderedContent.value);
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
</style>
