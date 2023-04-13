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
    collect {{ collect_id }}
    <Collect :collect_data='collect_data'></Collect>
  </template>
</template>
