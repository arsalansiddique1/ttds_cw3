<template>
  <div id="app">
    <h1>{{ title }}</h1>
    <form class="search-bar">
      <input v-model="searchTerm" type="text" id="searchTerm" name="searchTerm" placeholder="search anything or use dropdown for advanced search" :readonly="showQueryBuilder" spellcheck="true" >
      <button type="submit" class="search-button2" :class="{ 'active': showQueryBuilder }" @click.prevent="formSubmitted()"><img src="../images/search.png" alt=""></button>
      <button class="search-button1" @click.prevent="toggleQueryBuilder()">
        <img v-if="!showQueryBuilder" src="../images/down.png" alt=""> <!-- Original icon when showQueryBuilder is false -->
        <img v-else src="../images/up.png" alt=""> <!-- New icon when showQueryBuilder is true -->
      </button>
    </form>
    <label v-if="!showQueryBuilder" for="queryExpansion" style="font-size: 14px;">Use Query Expansion</label>
    <input v-if="!showQueryBuilder" id="queryExpansion" type="checkbox" v-model="queryExpansionEnabled" style="font-size: 12px;">

    <QueryBuilder v-if="showQueryBuilder" @clicked="onClickChild"></QueryBuilder>
    <img v-if="loading" class="loading-image" src="https://assets-v2.lottiefiles.com/a/83c5f61a-1181-11ee-8dbf-6fd67f708c77/NBb1C3ME0z.gif">
    <div  v-if="!loading && retrievalTime > 0" class="retrieval-time">
      Retrieval time: {{ retrievalTime }} seconds
    </div>
    <div v-if="!loading && images.length > 0" class="portfolio" id = "portfolio">
      <div class="portfolio__item" v-for="(image, index) in loadedImages" :key="image.id">
        <img :src="image.url" @click="openLightbox(index)"> <!-- change to line above to filter invalid images -->
      </div>
    </div>
    <div v-if="!loading && images.length === 0 && retrievalTime > 0">
      No results found.
    </div>
    <div class="portfolio-lightboxes">
      <div  class="portfolio-lightbox" v-for="(image, index) in loadedImages" :key="image.id" :id="'lightbox-' + index">
        <div class="portfolio-lightbox__content">
          <a href="#portfolio" class="close"></a>
          <img :src="image.url">
          <p class="portfolio-lightbox__body">{{ image.caption }}</p>
          <p>Date: {{ image.date || 'Unknown' }}, License: {{ image.license || 'Unknown' }}</p>
          <p>Size: {{ image.size || 'Unknown number of' }} bytes, Dimensions: {{ image.width || 'Unknown' }} x {{ image.height || 'Unknown' }} pixels</p>
          <a :href="'https://en.wikipedia.org/wiki/' + image.title.replace(/\s+/g, '_')" class="portfolio-lightbox__website" target="_blank" style="color: white ;">Full article: {{ image.title }}</a>
        </div>
      </div>
    </div>
    <div class="pagination" v-if="images.length > 0">
      <button @click="prevPage" :disabled="currentPage === 1" class="circular-btn">
        <span>&#9664;</span> <!-- Unicode character for left arrow -->
      </button>
      <span>{{ currentPage }}</span>
      <span> of </span>
      <span>{{ totalPages }}</span> <!-- Display total number of pages -->
      <button @click="nextPage" :disabled="currentPage === totalPages" class="circular-btn">
        <span>&#9654;</span> <!-- Unicode character for right arrow -->
      </button>
    </div>
  </div>
</template>

<script>
import API from './API';
import QueryBuilder from './components/QueryBuilder'

export default {
  name: 'app',
  data() {
    return {
      title: 'Wikimage Search',
      searchTerm: '',
      images: [],
      loading: false,
      currentPage: 1,
      totalPages: 1,
      pageSize: 10, // Number of images per page
      preloadedImages: [],
      showQueryBuilder: false, // Add a boolean data property to control visibility
      retrievalTime: 0,
      loadedImages: [],
      queryExpansionEnabled: false,
    };
  },
  components: {
    QueryBuilder
  },
  methods: {
    loadImages() {
      const BASE_URL = "https://upload.wikimedia.org/wikipedia/commons/";  
      const ALT_URL = "https://upload.wikimedia.org/wikipedia/en/"    
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = this.currentPage * this.pageSize;

      let imageArray = this.images.slice(startIndex, endIndex)

      for (let i = 0; i < imageArray.length; i++) {
        const image = imageArray[i];
        const img = new Image();
        const filename = image.filename
        img.src = BASE_URL + filename;
        img.valid = true;
        imageArray[i].valid = true;
        imageArray[i].url = BASE_URL + filename;
        img.onerror = () => {
          //try loading one more time with this alternative url
          const image = imageArray[i];
          const img = new Image();
          img.src = BASE_URL + image.filename;
          img.valid = true;
          imageArray[i].valid = true;
          imageArray[i].url = ALT_URL + filename;
          img.onerror = () => {
            imageArray[i].valid = false;
          };
        };
        
      }  
      this.loadedImages = imageArray;
    },
      
    openLightbox(index) {
      // Construct the lightbox ID
      const lightboxId = 'lightbox-' + index;
      // Set the location hash to trigger the :target pseudo-class
      location.hash = lightboxId;
    },
    onClickChild (value) {
          console.log(value) // someValue
          this.searchTerm = value
          const startTime = performance.now();
          this.loading = true;
          this.currentPage = 1; // Reset currentPage to 1
          this.images = [];
          this.preloadedImages = []; // Reset preloadedImages
          API.boolean_search(this.searchTerm)
            .then(images => {
              this.images = images.map(image => ({
                id: image.id,
                title: image.title,
                url: image.url,
                filename: image.filename,
                caption: image.caption,
                date: image.date,
                license: image.license,
                size: image.size,
                width: image.width,
                height: image.height,
                showCaption: false, // Initialize showCaption to false
              }));
              this.totalPages = Math.ceil(this.images.length / this.pageSize);
              this.loading = false;
              this.loadImages();
              const endTime = performance.now(); // Get the current timestamp when the response is received
              this.retrievalTime = ((endTime - startTime) / 1000).toFixed(2); // Calculate the retrieval time in seconds and update retrievalTime
          });
      },
    formSubmitted() {
      const startTime = performance.now();
      this.loading = true;
      this.currentPage = 1; // Reset currentPage to 1
      this.images = [];
      this.preloadedImages = []; // Reset preloadedImages
      API.search(this.searchTerm, this.queryExpansionEnabled)
        .then(images => {
          this.images = images.map(image => ({
            id: image.id,
            title: image.title,
            url: image.url,
            filename: image.filename,
            caption: image.caption,
            date: image.date,
            license: image.license,
            size: image.size,
            width: image.width,
            height: image.height,
            showCaption: false, // Initialize showCaption to false
          }));
          this.totalPages = Math.ceil(this.images.length / this.pageSize);
          this.loading = false;
          this.loadImages();
          const endTime = performance.now(); // Get the current timestamp when the response is received
          this.retrievalTime = ((endTime - startTime) / 1000).toFixed(2); // Calculate the retrieval time in seconds and update retrievalTime
        });
    },
    toggleQueryBuilder() {
      this.showQueryBuilder = !this.showQueryBuilder;
    },
    toggleQueryExpansion() {
      // Toggle the value of queryExpansionEnabled
      this.queryExpansionEnabled = !this.queryExpansionEnabled;
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.loadImages();
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.loadImages();
      }
    },
  },
};
</script>

<style>
#app {
  text-align: center;
  font-family: 'Montserrat';
  font-size: 30px;
}

body {
  width: 80%;
  margin: 2em auto 0 auto;
}

.images {
  column-count: 5;
  margin-top: 20px;
}

.loading-image {
  width: 35%;
  display: block;
  margin: 0 auto;
}

img {
  max-width: 100%;
  cursor: pointer; /* Add cursor pointer to indicate image clickability */
}

.pagination {
  margin-top: 20px;
  font-size: medium;
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
.search-bar{
  width: 100%;
  max-width: 700px;
  background: rgba(25, 25, 25, 0.15);
  display: flex;
  align-items: center;
  border-radius: 60px;
  padding: 10px 20px;
  backdrop-filter: blur(4px) saturate(180%);
  margin: 0 auto; /* Center align the search bar */
}
.search-bar input[readonly] {
  pointer-events: none; /* Set to none to make it unclickable */
}

.search-bar input{
  background: transparent;
  flex: 1;
  border: 0;
  outline: none;
  padding: 24px 20px;
  font-size: 20px;
  color:  rgba(25, 25, 25, 0.5);
}

::placeholder{
  color:  rgba(25, 25, 25, 0.5);
}

.search-bar button img{
  width: 25px;
}
.search-bar button.search-button1 {
  border: 0;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  background: rgba(150, 150, 150, 0.8);
  cursor: pointer;
  margin-left: 5px;
}


.search-bar button.search-button2.active {
  pointer-events: none;
  background-color: rgba(150, 150, 150, 0.8);
}

.search-bar button.search-button2 {
  border: 0;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  background: rgb(67, 100, 152); /* Change color as desired */ /* Different color for the second button */
  cursor: pointer;
  margin-left: 5px;
}


/* to set font */
@import '../font.css';

.portfolio {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  grid-gap: 1em;
  padding: 1em 3em; /* 1em top and bottom, 5em left and right */
  background-color: white;
  align-content: start;
}

.portfolio__item {
  background: white;
}

.portfolio__desc{
  margin-top: 0;
  font-size: 0.5em;
}

.portfolio-lightbox{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: scale(0,1);
  transform-origin: right;
  transition: transform ease-in-out 500ms;
}

.portfolio-lightbox:target {
  transform: scale(1,1);
  transform-origin: left;
}

.portfolio-lightbox__content {
  max-width: 50vw;
  max-height: 90vh;
  background: rgba(150, 150, 150, 0.95);
  padding: 1em;
  position: relative;
  font-size: 0.5em;
}

.portfolio-lightbox__content img {
  max-width: 100%; /* Ensure the image fits within its container */
  max-height: 35vh; /* Limit the maximum height of the image */
  object-fit: contain; /* Maintain aspect ratio while fitting the image within the specified dimensions */
}

.close {
  position: absolute;
  width: 1em;
  height: 1em;
  background: red;
  top: -1em;
  right: -1em;
  border-radius: 50%;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close::after {
  content: 'X';
  color: white;
  font-weight: 700;
  
}

.retrieval-time {
  margin-top: 10px;
  font-size: 18px;
}

</style>
