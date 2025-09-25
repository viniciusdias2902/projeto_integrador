const BASE_URL = import.meta.env.VITE_APP_API_BASE_URL || 'http://127.0.0.1:8000/api/v1/';

export async function getBoardingList(pollId, tripType) {
  const accessToken = localStorage.getItem('access');

  if (!accessToken) {
    throw new Error('Usuário não autenticado.');
  }

  const url = `${BASE_URL}polls/${pollId}/boarding_list/?trip_type=${tripType}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    throw new Error('Falha ao buscar a lista de embarque.');
  }
  return response.json();
}