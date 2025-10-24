import { API_URLS } from '@/config/api-config'

export async function getTodaysPoll() {
  const accessToken = localStorage.getItem('access')
  if (!accessToken) {
    throw new Error('Usuário não autenticado.')
  }

  const response = await fetch(API_URLS.POLLS, {
    headers: { Authorization: `Bearer ${accessToken}` },
  })

  if (!response.ok) {
    throw new Error('Falha ao buscar as enquetes.')
  }

  const polls = await response.json()

  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  const todayString = `${year}-${month}-${day}`

  const todaysPoll = polls.find((poll) => poll.date === todayString)

  return todaysPoll || null
}

export async function getBoardingList(pollId, tripType) {
  const accessToken = localStorage.getItem('access')

  if (!accessToken) {
    throw new Error('Usuário não autenticado.')
  }

  const url = `${API_URLS.POLLS}${pollId}/boarding_list/?trip_type=${tripType}`

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
  })

  if (!response.ok) {
    throw new Error('Falha ao buscar a lista de embarque.')
  }
  return response.json()
}
