<template>
    待完成
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute();
let collect_id = ref('')
collect_id.value = ref(route.params.collect_id)

</script>