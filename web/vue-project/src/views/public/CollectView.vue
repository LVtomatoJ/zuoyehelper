<script setup>
import { service } from '../../stores/axios.js'
import { onMounted,ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute();
const collect_id = route.params.collect_id
let collect_exist = ref(null)
let collect_data = ref(null)
import Collect from '../../components/public/Collect.vue'

function get_collect(){
  service({method:'get',url:'/public/getcollect',params:{collect_id:collect_id}}).then(res=>{
        const data = res.data
        collect_data.value = data
        collect_exist.value = true
}).catch((error)=>{
  // let message = error.response.data.detail
  collect_exist.value = false
})
}
onMounted(() => {
  get_collect()
})
</script>

<template>
  <template  v-if="collect_exist===false">
    <Exception type="404"/>
  </template>
  <template v-else-if="collect_exist===true">

      <div style="text-align: center;padding-top: 20px;">
        <h1>作业帮收件箱</h1>
      </div>
    <div style="padding-top: 20px;">
      <Row>
        <Col span="4"></Col>
        <Col span="16">
          <Collect :collect_data='collect_data'></Collect>
        </Col>
        <Col span="4"></Col>
    </Row>
      
  </div>
  </template>
</template>
