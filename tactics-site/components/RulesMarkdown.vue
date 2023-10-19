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
  <div class="rules" v-html="rulesMarkdown" />
</template>

<style scoped>

</style>
