<script setup>
import { service } from '../../stores/axios.js'
import { onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute();
const collect_id = route.params.collect_id
onBeforeMount(() => {
    service({method:'get',url:'/public/getcollect',params:{collect_id:collect_id}}).then(res=>{
        const data = res.data
        console.log(data)
})
})
</script>

<template>
  <main>
    collect {{ collect_id }}
  </main>
</template>
