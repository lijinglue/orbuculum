<template>
  <div id="app">
    <link rel="stylesheet"
          href="https://fonts.googleapis.com/css?family=Montserrat">
    <div class="header">
      <div class="hex-nav-bar">
        <div class="hex-logo">
          <div class="hex-logo-icon">
            <img src="./assets/hextech.png">
          </div>
          <div class="hex-logo-text"><span>HEXBET</span></div>
        </div>
      </div>
    </div>
    <div class="hex-container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'app'
  }
</script>

<style lang="less">
  @import "style/variables.less";
  @import "style/hextech.less";

  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
  }
</style>
