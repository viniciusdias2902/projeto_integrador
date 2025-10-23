import { ref, onUnmounted } from 'vue'

export function usePolling(callback, interval = 5000) {
  const isPolling = ref(false)
  let intervalId = null

  function startPolling() {
    if (isPolling.value) return

    isPolling.value = true
    intervalId = setInterval(() => {
      callback()
    }, interval)
  }

  function stopPolling() {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
    isPolling.value = false
  }

  onUnmounted(() => {
    stopPolling()
  })

  return {
    isPolling,
    startPolling,
    stopPolling,
  }
}
