<template>
  <div id="app">
    <Header />
    <Photo />
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import Photo from "./components/Photo.vue";

export default {
  name: "app",
  components: {
    Header,
    Photo
  }
};
</script>

<style lang="less">
body {
  background-color: #b0d0d3;
  color: #4b7679;
}

#app {
  font-family: "Indie Flower", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  max-width: 500px;
  margin: 60px auto;
}
</style>
