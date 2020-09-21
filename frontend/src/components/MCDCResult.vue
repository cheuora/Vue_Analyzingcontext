<template>
    <div class="main">
        <h3>MCDC Result</h3>
        <center>
        <p v-html="table"></p>
                <button @click="download">Down</button>
        </center>
    </div>
</template>

<style scoped>

</style>

<script>
  export default {
    data() {
      return {
        table: this.$route.params.tabledata
        url : "/assets/tmp"
      }
    },
    methods: {
      download() {
        
      }
    },
  } 

</script>

