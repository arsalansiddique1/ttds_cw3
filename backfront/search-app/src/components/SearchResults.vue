<template>
    <div class="search-results">
      <h2>Search Results</h2>
      <ul v-if="results.length > 0" class="results-list">
        <li v-for="(result, index) in results" :key="index" class="result-item">
          <a :href="result.filenames" target="_blank">{{ result.captions }}</a>
          <p>{{ result.description }}</p>
        </li>
      </ul>
      <p class="no-results" v-else>No results found.</p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      results: {
        type: Array,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
.search-results {
  text-align: center; /* Center align the content */
}

.results-list {
  list-style-type: none; /* Remove default list styles */
  padding: 0; /* Remove default padding */
}

.result-item {
  margin-bottom: 20px; /* Add margin between each result */
}

.no-results {
  margin-top: 10px; /* Add margin to separate from search results */
}
  /* Add your styles here */
  </style>