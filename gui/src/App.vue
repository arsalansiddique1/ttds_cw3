<template>
  <div id="app">
    <h1>{{ title }}</h1>
    <form @submit.prevent="formSubmitted()">
      <input v-model="searchTerm" class="u-full-width" type="text" id="searchTerm" name="searchTerm">
      <button type="submit">Search</button>
    </form>
    <img v-if="loading" class="loading-image" src="https://assets-v2.lottiefiles.com/a/83c5f61a-1181-11ee-8dbf-6fd67f708c77/NBb1C3ME0z.gif">
    <section class="images">
      <div v-for="image in images" :key="image.url">
        <img :src="image.url" @click="toggleCaption(image)">
        <div v-if="image.showCaption">{{ image.caption }}</div> <!-- Display the caption if showCaption is true -->
      </div>
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
          this.images = images.slice(0, 200).map(image => ({
            url: image.url,
            caption: image.caption,
            showCaption: false, // Initialize showCaption to false
          }));
          this.loading = false;
        });
    },
    toggleCaption(image) {
      // Toggle the showCaption property of the clicked image
      image.showCaption = !image.showCaption;
    },
  },
};
</script>

<style>
#app {
  text-align: center;
}

body {
  width: 80%;
  margin: 2em auto 0 auto;
}

.images {
  column-count: 3;
}

.loading-image {
  width: 35%;
  display: block;
  margin: 0 auto;
}

img {
  width: 100%;
  cursor: pointer; /* Add cursor pointer to indicate image clickability */
}

.caption {
  background-color: lightgray; /* Add light gray background to caption */
  padding: 5px; /* Add padding to caption */
}
</style>
