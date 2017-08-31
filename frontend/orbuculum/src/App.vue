<template>
  <div id="app">
    <div class="header">
      <div class="hex-logo">
        <div class="hex-logo-icon">
          <img src="./assets/hextech.png" width="45">
        </div>
        <div class="hex-logo-text"><span>HEXBET</span></div>
      </div>

    </div>

    <router-view></router-view>
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
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
</style>
