<script setup lang="ts">
import MarkdownIt from 'markdown-it'

const response = await useFetch('/rules_markdown.md')
const markdownText = response.data
console.log('markdown text', markdownText.value)
const md = new MarkdownIt()
const rulesMarkdown = computed(() => md.render(markdownText.value || ''))
</script>

<template>
  <div class="rules" mx-auto max-w-50rem v-html="rulesMarkdown" />
</template>
