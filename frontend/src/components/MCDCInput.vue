<template>
    <div class="main">
        <center>
        <h3>Elementary Comparison with MC/DC</h3>
        <h5>Enter (Java like)pseudo code below!</h5>

          <prism-editor class="my-editor height-300" v-model="code" :highlight="highlighter" line-numbers></prism-editor>
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
          console.log(this.code)
      }
    },

};

</script>


