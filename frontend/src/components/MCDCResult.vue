<template>
    <div class="main">
        <h3>MCDC Result</h3>
        <center>
        <p v-html="table"></p>
        </center>
    </div>
</template>

<style scoped>

</style>

<script>
  import axios from 'axios';

  export default {
    data() {
      var temp1 = window.location.origin;
      var temp = temp1.replace(":8080", "");
      return {
        table: this.$route.params.tabledata,
        url: temp + ":5000/static/temp/" + this.$route.params.xlsxfile
      }
    },
    methods: {
      downLoad() {
        axios({
          url: this.url,
          method: 'GET',
          responseType: 'blob',
        }).then((response) => {
          var fileURL = window.URL.createObjectURL(new Blob([response.data]));
          var fileLink = document.createElement('a');
          fileLink.href = fileURL;
          fileLink.setAttribute('download', 'result.xlsx');
          document.body.appendChild(fileLink);
          fileLink.click();
        })
      },
    },
  } 

</script>

