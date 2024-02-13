<template>
    <div>
      <SearchBar @results="handleSearchResults" />
      <SearchResults :results="searchResults" />
    </div>
  </template>
  
  <script>
  import SearchBar from './SearchBar.vue'; // Adjust the path as per your project structure
  import SearchResults from './SearchResults.vue'; // Adjust the path as per your project structure
  
  export default {
    components: {
      SearchBar,
      SearchResults
    },
    data() {
      return {
        searchResults: []
      };
    },
    methods: {
      handleSearchResults(results) {
        this.searchResults = results;
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>