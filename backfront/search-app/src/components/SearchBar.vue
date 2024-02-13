<template>
    <div>
      <input type="text" v-model="query" @keyup.enter="search">
      <button @click="search">Search</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        query: '',
      };
    },
    methods: {
      async search() {
        try {
            const response = await axios.get(`http://localhost:8000/search?query=${this.query}`);
            this.$emit('results', response.data.results); // Emitting results to parent component
          //const response = await axios.get(`YOUR_API_ENDPOINT?q=${this.query}`);
          //this.$emit('results', response.data); // Emitting results to parent component
        } catch (error) {
          console.error('Error searching:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>