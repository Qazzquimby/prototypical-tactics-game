<template>
  Reporting page is wip
</template>

<!-- <script setup lang="ts"> -->
<!-- import yaml from 'js-yaml' -->

<!-- import { GoogleAuthProvider, getAuth, signInWithPopup, signOut } from 'firebase/auth' -->
<!-- import type { Auth } from '@firebase/auth' -->

<!-- import type { Game } from '~/composables/gameTypes' -->

<!-- const isLoggedIn = ref(false) -->
<!-- let auth: Auth -->
<!-- onMounted(() => { -->
<!--  auth = getAuth() -->

<!--  auth.onAuthStateChanged((user) => { -->
<!--    isLoggedIn.value = !!user -->
<!--  }) -->
<!-- }) -->

<!-- async function signInWithGoogle() { -->
<!--  const provider = new GoogleAuthProvider() -->
<!--  await signInWithPopup(auth, provider) -->
<!-- } -->

<!-- async function logOut() { -->
<!--  await signOut(auth) -->
<!-- } -->

<!-- const yamlText = ref('') -->
<!-- const yamlContent = ref<Game>() -->

<!-- onMounted(async () => { -->
<!--  const response = await fetch('/input.yaml') -->
<!--  yamlText.value = await response.text() -->
<!--  // noinspection TypeScriptValidateTypes -->
<!--  yamlContent.value = yaml.load(yamlText.value) -->
<!-- }) -->
<!-- // todo make the yamltext a shared composable, only loaded once -->

<!-- const heroes = computed(() => { -->
<!--  if (!yamlContent.value) { -->
<!--    return [] -->
<!--  } -->

<!--  const heroIds = [] -->
<!--  for (const gameSet of yamlContent.value.sets) { -->
<!--    for (const hero of gameSet.heroes) { -->
<!--      heroIds.push({ nameWithSet: `${hero.name} (${gameSet.name})`, version: hero.version }) -->
<!--    } -->
<!--  } -->
<!--  return heroIds -->
<!-- }) -->

<!-- const maps = computed(() => { -->
<!--  if (!yamlContent.value) { -->
<!--    return [] -->
<!--  } -->

<!--  const mapIds = [] -->
<!--  for (const gameSet of yamlContent.value.sets) { -->
<!--    if (!gameSet.maps) { -->
<!--      continue -->
<!--    } -->
<!--    for (const gameMap of gameSet.maps) { -->
<!--      mapIds.push({ nameWithSet: `${gameMap.name} (${gameSet.name})`, version: gameMap.version }) -->
<!--    } -->
<!--  } -->
<!--  return mapIds -->
<!-- }) -->
<!-- </script> -->

<!-- <template> -->
<!--  <div /> -->
<!-- &lt;!&ndash;  <div mx-auto max-w-30rem border-8px border-gray-4 rd p-4> &ndash;&gt; -->
<!-- &lt;!&ndash;    <div v-if="isLoggedIn"> &ndash;&gt; -->
<!-- &lt;!&ndash;      <p text-center> &ndash;&gt; -->
<!-- &lt;!&ndash;        Signed in as {{ auth.currentUser?.displayName }} &ndash;&gt; -->
<!-- &lt;!&ndash;      </p> &ndash;&gt; -->
<!-- &lt;!&ndash;      <button &ndash;&gt; -->
<!-- &lt;!&ndash;        mx-auto block border border-gray-400 rounded bg-white px-4 py-2 font-semibold text-gray-800 shadow hover:bg-gray-100 &ndash;&gt; -->
<!-- &lt;!&ndash;        @click="logOut" &ndash;&gt; -->
<!-- &lt;!&ndash;      > &ndash;&gt; -->
<!-- &lt;!&ndash;        Sign out &ndash;&gt; -->
<!-- &lt;!&ndash;      </button> &ndash;&gt; -->
<!-- &lt;!&ndash;    </div> &ndash;&gt; -->
<!-- &lt;!&ndash;    <div v-else> &ndash;&gt; -->
<!-- &lt;!&ndash;      <p text-center> &ndash;&gt; -->
<!-- &lt;!&ndash;        Sign in to report your game results, which helps me fine tune. &ndash;&gt; -->
<!-- &lt;!&ndash;      </p> &ndash;&gt; -->
<!-- &lt;!&ndash;      <button &ndash;&gt; -->

<!-- &lt;!&ndash;        mx-auto block border border-gray-400 rounded bg-white px-4 py-2 font-semibold text-gray-800 shadow hover:bg-gray-100 @click="signInWithGoogle" &ndash;&gt; -->
<!-- &lt;!&ndash;      > &ndash;&gt; -->
<!-- &lt;!&ndash;        Sign in with Google &ndash;&gt; -->
<!-- &lt;!&ndash;      </button> &ndash;&gt; -->
<!-- &lt;!&ndash;    </div> &ndash;&gt; -->
<!-- &lt;!&ndash;  </div> &ndash;&gt; -->

<!-- &lt;!&ndash;  <div v-if="isLoggedIn"> &ndash;&gt; -->
<!-- &lt;!&ndash;    <GameReportForm :heroes="heroes" :maps="maps" /> &ndash;&gt; -->
<!-- &lt;!&ndash;  </div> &ndash;&gt; -->
<!-- </template> -->
