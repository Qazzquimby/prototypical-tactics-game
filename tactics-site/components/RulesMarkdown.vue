<script setup lang="ts">
import MarkdownIt from 'markdown-it'

const { data: markdownText } = await useFetch('/rules.md')

const md = new MarkdownIt()
const rulesMarkdown = computed(() => md.render(markdownText.value || ''))
</script>

<template>
  <div class="rules" mx-auto max-w-50rem v-html="rulesMarkdown" />
</template>

<style scoped>
.rules {
  padding: 1rem;
}
</style>
