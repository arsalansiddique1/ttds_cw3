<template>
  <div id="app">
    <h1>{{ title }}</h1>
    <form @submit.prevent="formSubmitted()">
      <input v-model="searchTerm" class="u-full-width" type="text" id="searchTerm" name="searchTerm">
      <button type="submit">Search</button>
    </form>
    <img v-if="loading" class="loading-image" src="https://assets-v2.lottiefiles.com/a/83c5f61a-1181-11ee-8dbf-6fd67f708c77/NBb1C3ME0z.gif">
    <section class="images">
      <div v-for="image in displayedImages" :key="image.url">
        <img :src="image.url" @click="toggleCaption(image)">
        <div v-if="image.showCaption">{{ image.caption }}</div> <!-- Display the caption if showCaption is true -->
      </div>
    </section>
    <div class="pagination" v-if="images.length > 0">
      <button @click="prevPage" :disabled="currentPage === 1" class="circular-btn">
        <span>&#9664;</span> <!-- Unicode character for left arrow -->
      </button>
      <span>{{ currentPage }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="circular-btn">
        <span>&#9654;</span> <!-- Unicode character for right arrow -->
      </button>
    </div>
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
      currentPage: 1,
      pageSize: 10, // Number of images per page
      preloadedImages: [],
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.images.length / this.pageSize);
    },
    displayedImages() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = this.currentPage * this.pageSize;
      return this.images.slice(startIndex, endIndex);
    },
  },
  methods: {
    formSubmitted() {
      this.loading = true;
      this.currentPage = 1; // Reset currentPage to 1
      this.images = [];
      this.preloadedImages = []; // Reset preloadedImages
      API.search(this.searchTerm)
        .then(images => {
          this.images = images.map(image => ({
            url: image.url,
            caption: image.caption,
            showCaption: false, // Initialize showCaption to false
          }));
          this.loading = false;
          this.preloadNextPageImages(); // Preload images for next page after search
        });
    },
    toggleCaption(image) {
      // Toggle the showCaption property of the clicked image
      image.showCaption = !image.showCaption;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.preloadNextPageImages(); // Preload images for next page when navigating to next page
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.preloadPrevPageImages(); // Preload images for previous page when navigating to previous page
      }
    },
    preloadNextPageImages() {
      const nextPageStartIndex = this.currentPage * this.pageSize;
      const nextPageEndIndex = nextPageStartIndex + this.pageSize;
      const nextPageImages = this.images.slice(nextPageStartIndex, nextPageEndIndex);
      this.preloadImages(nextPageImages);
    },
    preloadPrevPageImages() {
      const prevPageStartIndex = (this.currentPage - 2) * this.pageSize;
      const prevPageEndIndex = prevPageStartIndex + this.pageSize;
      const prevPageImages = this.images.slice(prevPageStartIndex, prevPageEndIndex);
      this.preloadImages(prevPageImages);
    },
    preloadImages(images) {
      for (const image of images) {
        const img = new Image();
        img.src = image.url;
        this.preloadedImages.push(img);
      }
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
  column-count: 5;
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

.pagination {
  margin-top: 20px;
}

.pagination button {
  margin: 0 5px;
}

.circular-btn {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  padding: 0;
  background-color: #ddd; /* Add background color for circular buttons */
  border: none;
  cursor: pointer;
  display: inline-flex;
  justify-content: center;
  align-items: center;
}

.circular-btn span {
  font-size: 20px;
}
</style>
