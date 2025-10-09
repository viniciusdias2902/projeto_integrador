import { ref } from 'vue'


export function useDelayedLoading(minDelay = 500) {
    const isLoading = ref(false)


    async function executeWithLoading(asyncFn, withDelay = false) {
        isLoading.value = true

        try {
            if (withDelay) {
                const [result] = await Promise.all([
                    asyncFn(),
                    new Promise(resolve => setTimeout(resolve, minDelay))
                ])
                return result
            } else {
                return await asyncFn()
            }
        } finally {
            isLoading.value = false
        }
    }

    return {
        isLoading,
        executeWithLoading
    }
}