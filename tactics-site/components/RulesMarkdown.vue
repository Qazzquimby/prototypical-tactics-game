<script setup lang="ts">
import MarkdownIt from 'markdown-it'

const rulesMarkdown = ref('')

onMounted(async () => {
  const md = new MarkdownIt()
  const markdownFile = await fetch('/rules.md')
  const markdownText = await markdownFile.text()

  rulesMarkdown.value = md.render(markdownText)
})
</script>

<template>
  <div v-html="rulesMarkdown" />
</template>

<!-- @apply text-4xl font-bold; -->

<style scoped>
h1 {
  font-size: 2.5rem;
}

h2 {
  @apply text-3xl font-bold;
}

h3 {
  @apply text-2xl font-bold;
}
</style>
