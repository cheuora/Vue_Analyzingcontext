<template>
    <div class="main">
        <center>
        <h3>Elementary Comparison with MC/DC</h3>
        <h5>Enter (Java like)pseudo code below!</h5>

          <prism-editor class="my-editor height-300" v-model="code" :highlight="highlighter" line-numbers></prism-editor>
          <br>
          <button @click="getResult">Get Result</button>

        </center>
    </div>
</template>

<style scoped>
  /* required class */
  .my-editor {
    /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
    background: #2d2d2d;
    color: #ccc;
 
    /* you must provide font-family font-size line-height. Example: */
    font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
    font-size: 14px;
    line-height: 1.5;
    padding: 5px;
  }
 
  /* optional class for removing the outline */
  .prism-editor__textarea:focus {
    outline: none;
  }
  .height-300 {
   height: 300px;
  }


</style>




<script>
 // import Prism Editor
  import { PrismEditor } from 'vue-prism-editor';
  import 'vue-prism-editor/dist/prismeditor.min.css'; // import the styles somewhere
 
  // import highlighting library (you can use any library you want just return html string)
  import { highlight, languages } from 'prismjs/components/prism-core';
  import 'prismjs/components/prism-clike';
  import 'prismjs/components/prism-javascript';
  import 'prismjs/themes/prism-tomorrow.css'; // import syntax highlighting styles
  import axios from 'axios';


  var temp = "/** Sample **/ \n if ( a || b){ \n    print a;\n}\nelse if ( c && d || e){\n    print b;\n}"
 
  export default {
      components: {
        PrismEditor,
      },
      data: () => ({ code: temp }),
      methods: {

        highlighter(code) {
          return highlight(code, languages.js); //returns html
        },
        getResult(){
            var router = this.$router 
            var url = window.location.origin;
            var temp = url.replace(":8080", "");

            axios({
              method : 'post',
              url : temp + ':5000/mcdcresult',
              data : {
                codes : this.code,
              }
            }).then(function(response){
              var responseData
              responseData = response.data.split(":::")
              router.push({
                name: 'mcdcresult',
                params: {tabledata:responseData[0],
                        xlsxfile:responseData[1]}
              })
            }).catch(function(error){
              router.push({
                name: 'errorpage',
                params : {errormsg:error}
              })
            })
        }
      },

  };

</script>


