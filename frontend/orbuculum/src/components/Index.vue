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
      <span class="odds">1.29</span>
      <span class="vs">vs</span>
      <span class="odds">1.90</span>
    </div>
    <a href="matches.html" class="team guest">
                <span class="info">
                    <span class="name">Team 2</span>
                    <span class="city">London</span>
                </span>
      <span class="image"><img src="../assets/team-rng.png" alt="main-match"></span>
    </a>
    <div class="count-down"><span>{{countdown}}</span></div>
  </div>

</template>

<script>
  export default {
    name: 'Index',
    mounted () {
      setInterval(() => {
        this.countdown = this.countdown - 1
      }, 1000)
    },

    data () {
      return {
        prediction: 'Which team will be the Summer Champion of LPL?',
        countdown: 1000
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="less">
  @scheme-name: "dota";
  @import "../style/variables";
  @import "../style/less-variables/dota";
  @import "../style/style";

  .amateurs-main-match {
    background: rgba(0, 0, 0, 0);

    &:before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: url('../assets/up-coming-bg.jpg') no-repeat;
      background-size: cover;
      z-index: -1;
      filter: grayscale(0.8) blur(3px);
    }
    .title {
      font-size: @font_size_large;
      font-weight: bold;
    }
    .team .name {
      font-size: @font_size_medium;
    }
    a.team {
      width: 30%;
    }
    .score {
      width: 20%;
      min-width: 250px;
      display: inline-flex;
      justify-content: space-between;
      align-items: center;

      @media (max-width: @media_width_m) {
        width: 100%;
        justify-content: center;
      }

      .vs {
        width: 30px;
        padding: 2px;
        font-size: @font_size_medium;
        color: @color_grey;
        background: @color_white_tp_5;
        @media (max-width: @media_width_m) {
          margin: calc(5%)
        }
      }

      .odds {
        padding: 5px;
        width: 75px;
      }
    }
  }
</style>
