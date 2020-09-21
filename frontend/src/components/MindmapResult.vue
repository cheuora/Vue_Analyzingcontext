<template>
    <div class="main">
        <h3>Scenario Result</h3>
        <center>
        <p v-html="table"></p>
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
      }
    },
    methods: {},
  } 

</script>

