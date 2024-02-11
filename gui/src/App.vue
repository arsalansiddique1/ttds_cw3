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

      this.images = this.getWikiLinks();
      this.loading = false;
    },
    getWikiLinks(){
      return [
      'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Mtberlin_%2830745595202%29.jpg/800px-Mtberlin_%2830745595202%29.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/d/dd/Presidente_Nayib_Bukele_%28cropped%29.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Magna_Lykseth_in_Tristan_och_Isolde_at_Kungliga_Operan_1909_-_SMV_-_GL164.jpg/800px-Magna_Lykseth_in_Tristan_och_Isolde_at_Kungliga_Operan_1909_-_SMV_-_GL164.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/6/6d/Puu_Oo_cropped.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/3/38/Great_American_Biotic_Interchange_examples.svg',
      'https://upload.wikimedia.org/wikipedia/commons/3/37/Turritellatricarinata.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/5/58/Life_reconstruction_of_the_terror_bird_Titanis_walleri.jpg',
      'https://upload.wikimedia.org/wikipedia/en/c/c1/Charles_Mitchill_Bogert_1955.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/3/34/Mesa_County_Court_House.jpg',
      'https://upload.wikimedia.org/wikipedia/commons/6/60/Colorado_in_United_States.svg'
      ];
    }
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
