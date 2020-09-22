<template>
    <div class="main">
        <center>
            <h3 id="toc_1"><router-link to="/mindmapinput">MindMap &amp; GWT</router-link></h3>
            <h3 id="toc_3"><router-link to="/mcdcinput"> Comparison with MC/DC</router-link></h3>
            <img src='@/assets/dividingLine.png' width="200px">
            <h3><a v-bind:href="link">   How to Use</a></h3>
        </center>
    </div>
</template>

<style scoped>

</style>

<script>
//import axios from 'axios'

export default{


    data(){ 

        return{
            link: 'http://localhost:5000/static/kor/Helphome.html'
        }

        }

}


</script>

