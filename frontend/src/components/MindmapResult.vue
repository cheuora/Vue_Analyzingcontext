<template>
    <div class="main">
        <h3>Scenario Result</h3>

        <p v-html="table"></p>
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

