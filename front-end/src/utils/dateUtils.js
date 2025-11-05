export function parseLocalDate(dateString) {
  if (!dateString || dateString === 'não informado') {
    return null
  }

  const [year, month, day] = dateString.split('-').map(Number)
  return new Date(year, month - 1, day)
}

export function formatDateBR(dateString) {
  if (!dateString || dateString === 'não informado') {
    return 'Não informado'
  }

  const date = parseLocalDate(dateString)
  return date.toLocaleDateString('pt-BR')
}

export function formatDateISO(date) {
  if (!date) return null

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}
