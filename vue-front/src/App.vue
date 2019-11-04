<template>
  <div id="app">
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <Words></Words>
  </div>
</template>

<script>
import Words from './components/Words.vue'

export default {
  name: 'app',
  components: {
    Words
  }
}
</script>

<style>
#app {
}
</style>
