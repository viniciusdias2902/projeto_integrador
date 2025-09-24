<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({ name: [String, Number], day: String })

const POLLS_URL = `${import.meta.env.VITE_APP_API_URL}polls/`
const VOTES_URL = `${import.meta.env.VITE_APP_API_URL}votes/`

const selectedOption = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const token = localStorage.getItem('access')

function getUserIdFromDecodedToken() {
  try {
    const payload = token.split('.')[1]
    const decoded = JSON.parse(atob(payload))
    return decoded.user_id || decoded.id || null
  } catch {
    return null
  }
}

const userId = token ? getUserIdFromDecodedToken() : null
let existingVoteId = null

async function fetchPoll() {
  errorMessage.value = ''
  try {
    const response = await fetch(`${POLLS_URL}${props.name}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error('Failed to fetch poll')
    }

    const poll = await response.json()

    const userVote = poll.votes.find((vote) => Number(vote.student.id) === Number(userId))
    console.log(userVote)

    if (userVote) {
      existingVoteId = userVote.id
      selectedOption.value = userVote.option
      successMessage.value = 'Você já votou!'
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Falha ao carregar a enquete. Tente atualizar a página.'
  }
}

async function submitVote() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!selectedOption.value) {
    errorMessage.value = 'Selecione uma opção antes de enviar'
    return
  }

  try {
    let response

    if (existingVoteId) {
      response = await fetch(`${VOTES_URL}${existingVoteId}/update/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ option: selectedOption.value }),
      })
    } else {
      response = await fetch(`${VOTES_URL}create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          poll: Number(props.name),
          option: selectedOption.value,
        }),
      })
    }

    if (!response.ok) {
      throw new Error('Failed to submit vote')
    }

    const data = await response.json()
    console.log('Vote submitted:', data)

    successMessage.value = 'Vote enviado!'
    if (!existingVoteId && data.id) {
      existingVoteId = data.id
    }
  } catch (error) {
    console.error(error)
    errorMessage.value = 'Um erro aconteceu ao enviar seu voto. Tente novamente'
  }
}

onMounted(() => {
  if (token && userId) {
    fetchPoll()
  } else {
    errorMessage.value = 'Usuário não autenticado'
  }
})
</script>

<template>
  <fieldset
    class="fieldset bg-base-100 border-base-300 rounded-box border lg:w-200 sm:w-64 p-4 flex flex-col"
  >
    <legend class="fieldset-legend">{{ day }}</legend>

    <LabelComponent :for="`${name}-1`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="round_trip"
        v-model="selectedOption"
        :id="`${name}-1`"
      />
      Ida e volta
    </LabelComponent>

    <LabelComponent :for="`${name}-2`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="one_way_outbound"
        v-model="selectedOption"
        :id="`${name}-2`"
      />
      Apenas ida
    </LabelComponent>

    <LabelComponent :for="`${name}-3`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="one_way_return"
        v-model="selectedOption"
        :id="`${name}-3`"
      />
      Apenas volta
    </LabelComponent>

    <LabelComponent :for="`${name}-4`" class="text-lg">
      <input
        type="radio"
        class="radio radio-primary"
        :name="name"
        value="absent"
        v-model="selectedOption"
        :id="`${name}-4`"
      />
      Não vou
    </LabelComponent>

    <button class="btn btn-primary mt-1 btn-lg" @click="submitVote">Enviar Resposta</button>

    <AlertComponent v-if="errorMessage" class="mt-2">
      {{ errorMessage }}
    </AlertComponent>

    <SuccessComponent v-if="successMessage" class="mt-2 flex self-start">
      {{ successMessage }}
    </SuccessComponent>
  </fieldset>
</template>
