<script setup lang="ts">
</script>

<template>
  <ContentDoc class="nuxt-content" />
</template>

<style>
.nuxt-content {
  /* Base styles */
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #e3dddd;
}

/* Headings */
.nuxt-content h1 {
  font-size: 2.5em;
  margin-bottom: 0.5em;
  color: #c4c6c8;
}

.nuxt-content h2 {
  font-size: 2em;
  margin-bottom: 0.5em;
  color: #a8aaac;
}

.nuxt-content h3 {
  font-size: 1.5em;
  margin-bottom: 0.5em;
  color: #7f8c8d;
}

/* Paragraphs */
.nuxt-content p {
  margin-bottom: 1em;
}

/* Links */
.nuxt-content a {
  color: #3498db;
  text-decoration: none;
}

.nuxt-content a:hover {
  text-decoration: underline;
}

/* Lists */
.nuxt-content ul, .nuxt-content ol {
  margin-bottom: 1em;
  padding-left: 2em;
}

.nuxt-content ol {
  list-style: decimal;
}

.nuxt-content ul {
  list-style: disc
}

/* Code blocks */
.nuxt-content pre {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1em;
  overflow-x: auto;
}

.nuxt-content code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

/* Blockquotes */
.nuxt-content blockquote {
  border-left: 4px solid #ccc;
  margin: 0;
  padding-left: 1em;
  font-style: italic;
}

/* Tables */
.nuxt-content table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 1em;
}

.nuxt-content th, .nuxt-content td {
  border: 1px solid #ddd;
  padding: 0.5em;
}

.nuxt-content th {
  background-color: #f2f2f2;
  font-weight: bold;
}
</style>
