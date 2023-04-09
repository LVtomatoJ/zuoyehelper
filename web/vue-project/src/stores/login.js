import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useLoginStore = defineStore('login', () => {
  const isLoggedIn = ref(false)
  const jwt = ref('')
  return { isLoggedIn,jwt}
})
