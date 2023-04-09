<script setup>
import { useLoginStore } from '../stores/login'
const store = useLoginStore()
</script>

<template>
  <main>
    about {{ store.jwt }}
  </main>
</template>
