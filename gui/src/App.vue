<template>
  <div id="app">
    <h1>{{title}}</h1>
    <form @submit.prevent="formSubmitted()">
      <input v-model="searchTerm" class="u-full-width" type="text" id="searchTerm" name="searchTerm">
      <button type="submit">Search</button>
    </form>
    <img v-if="loading" class="loading-image" src="https://assets-v2.lottiefiles.com/a/83c5f61a-1181-11ee-8dbf-6fd67f708c77/NBb1C3ME0z.gif">
    <section class="images">
      <img v-for="image in images" :key="image" :src="image">
    </section>
  </div>
</template>

<script>
import API from './API';

export default {
  name: 'app',
  data() {
    return {
      title: 'WIKI IMAGE SEARCH',
      searchTerm: '',
      images: [],
      loading: false,
    };
  },
  methods: {
    formSubmitted() {
      this.loading = true;
      this.images = [];
      API.search(this.searchTerm)
        .then(images => {
          this.images = images.slice(0, 200); // Limiting the number of results to 200
          this.loading = false;
        });
    },
  },
};
</script>

<style>

#app {
  text-align: center; /* Center align the contents of the app */
}

body {
  width: 80%;
  margin: 2em auto 0 auto;
}

.images {
  column-count: 5;
}

.loading-image {
  width: 35%;
  display: block; /* Ensure the image is a block element */
  margin: 0 auto; /* Center the image horizontally */
}

img {
  width: 100%;
}
</style>
