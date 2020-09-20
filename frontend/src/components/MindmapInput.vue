<template>
    <div class="main">

        <h3>Given-When Scenario with MindMap</h3>
             <center>
                
                <button @click="zoomIn">Zoon In</button>&nbsp;
                <button @click="zoomOut">Zoom Out</button>
             </center>
             <js-mind :values="mind" :options="options" ref="jsMind" width='200px' height="400px"></js-mind>
             <br>
        <center>
          <a v-on:click.once="getResult"><b>Get Result</b></a> &nbsp;|
          <label for="import"><b>Import map</b></label> &nbsp;|
          <a v-on:click.once="saveLocalFile"><b>Export map</b></a>
  
          <input type='file' @change='openLocalFile' accept="text/plane" ref="input" id="import" style="display:none"/>


        </center>
    </div>

</template>

<style scoped>


</style>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      theme_value:'',
      mind: {
        /* 마인드 맵의 이름, 작성자, 버전 및 기타 정보를 정의하는 메타 데이터 */
        meta: {
          name: "example",
          author: "906106844@qq.com",
          version: "0.2"
        },
        format: "node_array",
        /* 데이터 내용 */
        /* 데이터 형식 선언 */
        data: [
          { id: "root", isroot: true, topic: "Main" },

          { id: "when", parentid: "root", topic: "When", direction: "left" },
          // { id: "easy1", parentid: "easy", topic: "Easy to show" },
          // { id: "easy2", parentid: "easy", topic: "Easy to edit" },
          // { id: "easy3", parentid: "easy", topic: "Easy to store" },
          // { id: "easy4", parentid: "easy", topic: "Easy to embed" },

          {
             id: "given",
             parentid: "root",
             topic: "Given",
             //expanded: false,
             direction: "right"
          },
          // { id: "open1", parentid: "open", topic: "on GitHub" },
          // { id: "open2", parentid: "open", topic: "BSD License" },

          // {
          //   id: "powerful",
          //   parentid: "root",
          //   topic: "Powerful",
          //   direction: "right"
          // },
          // {
          //   id: "powerful1",
          //   parentid: "powerful",
          //   topic: "Base on Javascript"
          // },
          // { id: "powerful2", parentid: "powerful", topic: "Base on HTML5" },
          // { id: "powerful3", parentid: "powerful", topic: "Depends on you" }
        ]
      },
      options: {
        // mode:'side'
      },
      shortCutVal:'',
      keyCode:''
    };
  },
  mounted() {
    this.jm= this.$refs.jsMind.jm
    this.jm.enable_edit()
  },
  methods:{
    getResult(){
      var mind_data = this.jm.get_data('node_array');
      var mind_tree = this.jm.get_data('node_tree')
      var mind_data_str = jsMind.util.json.json2string(mind_data.data);
      var mind_tree_str = jsMind.util.json.json2string(mind_tree.data);
      var router = this.$router 
      axios({
        method : 'post',
        url : 'http://localhost:5000/mindmap',
        data : {
          mindMapData : mind_data_str,
          mindTreeData : mind_tree_str,
        }
      }).then(function(response){
        console.log(response);
        router.push({
          name: 'mindmapresult',
          params: {tabledata:response.data}
        })
      }).catch(function(error){
        router.push({
          name: 'errorpage',
          params : {errormsg:error}
        })
      })
    },
    addNode(){
      var selected_node = this.jm.get_selected_node(); // as parent of new node
        if(!selected_node){alert('please select a node first.');return;}

        var nodeid = jsMind.util.uuid.newid();
        var topic = 'new Node';
        var node = this.jm.add_node(selected_node, nodeid, topic);
    },
    onMoveUp(){
      var selected_id =this.jm.get_selected_node()
        if(!selected_id){alert('please select a node first.');return;}
        this.jm.move_node(selected_id,'_first_');
    },
    onMoveDown(){
      var selected_id = this.jm.get_selected_node();
        if(!selected_id){alert('please select a node first.');return;}

        this.jm.move_node(selected_id,'_last_');
    },
    onRemoveNode(){
      var selected_id = this.get_selected_nodeid();
      console.log(selected_id)
      if(!selected_id){alert('please select a node first.');return;}
      this.jm.remove_node(selected_id);
    },
    addImageNode(){
      var imageChooser = document.getElementById('image-chooser');
      const _this=this
      imageChooser.addEventListener('change', function (event) {
      // Read file here.
      var reader = new FileReader();
      reader.onloadend = (function () {
            var selected_node = _this.jm.get_selected_node();
            var nodeid = jsMind.util.uuid.newid();
            var topic = undefined;
            var data = {
                "background-image": reader.result,
                "width": "100",
                "height": "100"};
            var node = _this.jm.add_node(selected_node, nodeid, topic, data);
        });

        var file = imageChooser.files[0];
        if (file) {
            reader.readAsDataURL(file);
        };

      }, false);
      var selected_node = this.jm.get_selected_node(); // as parent of new node
      if(!selected_node){
          alert('please select a node first.');
          return;
      }

      imageChooser.focus();
      imageChooser.click();
    },
    openLocalFile(){
        var file_input = this.$refs.input;
        var files = file_input.files;
        const _this=this
        if(files.length > 0){
            var file_data = files[0];
            jsMind.util.file.read(file_data,function(jsmind_data, jsmind_name){
                var mind = jsMind.util.json.string2json(jsmind_data);
                if(!!mind){
                    _this.mind=mind
                    _this.jm.show(mind);
                }else{
                    alert('can not open this file as mindmap');
                }
            });
        }else{
            alert('please choose a file first')
        }
    },
    saveLocalFile(){    
      var mind_data = this.jm.get_data();
      var mind_name = mind_data.meta.name;
      var mind_str = jsMind.util.json.json2string(mind_data);
      jsMind.util.file.save(mind_str,'text/jsmind',mind_name+'.jm');
    },
    fontSize(){
      var selected_id = this.get_selected_nodeid();
      if(!selected_id){alert('please select a node first.');return;}
      this.jm.set_node_font_style(selected_id, 28);
    },
    fontColor(){
      var selected_id = this.get_selected_nodeid();
        if(!selected_id){alert('please select a node first.');return;}
        this.jm.set_node_color(selected_id, null, '#000');
    },
    bgColor(){
      var selected_id = this.get_selected_nodeid();
        if(!selected_id){alert('please select a node first.');return;}

        this.jm.set_node_color(selected_id, '#eee', null);
    },
    bgImage(){
       var selected_id = this.get_selected_nodeid();
        if(!selected_id){alert('please select a node first.');return;}
        this.jm.set_node_background_image(selected_id, 'ant.png', 100, 100);
    },
    set_theme(){
      this.jm.set_theme(this.theme_value);
    },
    zoomOut(){
      if(this.jm.view.zoomOut()){
        this.$refs.zoomOut.disabled = false
      }else{
        this.$refs.zoomOut.disabled = true
      }
    },
    zoomIn(){
     if(this.jm.view.zoomIn()){
        this.$refs.zoomIn.disabled = false
      }else{
        this.$refs.zoomIn.disabled = true
      }
    },
    screenshot(){
      this.jm.screenshot.shootDownload();
    },
// 선택한 태그의 ID를 가져옵니다.
    get_selected_nodeid(){
        var selected_node = this.jm.get_selected_node();
        if(!!selected_node){
            return selected_node.id;
        }else{
            return null;
        }
    },
    changeOption(){
      this.options={
        mode:'side'
      }
    },
    // 단일 버튼 바인딩만 지원
    shortcutSet(value){
      if(value.key==='Backspace'||value.key==='Delete'){
        this.shortCutVal=this.shortCutVal.substring(0,this.shortCutVal.lastIndexOf('+'))
        this.keyCode=this.keyCode.substring(0,this.keyCode.lastIndexOf('+'))
        return
      }
      if(this.shortCutVal){
        this.shortCutVal+=' + '
        this.keyCode+='+'
      }
      this.shortCutVal+=value.key
      this.keyCode+=value.keyCode
      console.log('keyCode',this.keyCode)
      this.options={
        shortcut:{
           mapping: {
          // 바로 가기 키 매핑
            addchild: this.keyCode, 
          }
        }
      }
    }
  }
}
</script>