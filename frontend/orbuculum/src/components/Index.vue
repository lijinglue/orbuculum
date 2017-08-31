<template>
  <div class="amateurs-main-match">
    <div class="title">{{prediction}}</div>
    <a href="#" class="team">
      <span class="image"><img src="../assets/team-rng.png" alt="main-match"></span>
      <span class="info">
                    <span class="name">Team 1</span>
                    <span class="city">london</span>
                </span>
    </a>
    <div class="score">
      <span>3:2</span>
    </div>
    <a href="matches.html" class="team guest">
                <span class="info">
                    <span class="name">Team 2</span>
                    <span class="city">London</span>
                </span>
      <span class="image"><img src="../assets/team-rng.png" alt="main-match"></span>
    </a>
    <div class="title">26 september / 8:45 PM</div>
  </div>

</template>

<script>
  export default {
    name: 'Index',
    data () {
      return {
        prediction: 'Which team will be the Summer Champion of LPL?'
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
  @scheme-name: "dota";
  @import "../style/less-variables/dota";
  @import "../style/style";
  @font_size_large: 24px;

  .amateurs-main-match {
    &:before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: url('../assets/up-coming-bg.jpg') no-repeat;
      z-index: -1;
      filter: grayscale(0.8) blur(3px);
    }
    .title {
      font-size: @font_size_large;
    }
  }
</style>
