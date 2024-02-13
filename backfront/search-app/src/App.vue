<template>
  <div id="app">
    <img src="./assets/coollogo.gif" alt="Logo" />

    <!--SearchBar @results="handleSearchResults" / -->

    <SearchEngine />
    <!-- Other components and content -->
  </div>

  <!-- img alt="Vue logo" src="./assets/logo.png" -->
  <!-- HelloWorld msg="Welcome to Your Vue.js App"/ -->
</template>

<script>
//import HelloWorld from './components/HelloWorld.vue';
//import SearchBar from './components/SearchBar.vue';
import SearchEngine from './components/SearchEngine.vue';

export default {
  name: 'App',
  components: {
    //HelloWorld,
    //SearchBar,
    SearchEngine
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  background-color: black;
}

body, html {
  margin: 0;
  padding: 0;
  background-color: black;
}
</style>
