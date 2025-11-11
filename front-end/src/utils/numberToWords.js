export function numberToWords(value) {
  const unidades = ['', 'UM', 'DOIS', 'TRÊS', 'QUATRO', 'CINCO', 'SEIS', 'SETE', 'OITO', 'NOVE']
  const dezADezenove = [
    'DEZ',
    'ONZE',
    'DOZE',
    'TREZE',
    'QUATORZE',
    'QUINZE',
    'DEZESSEIS',
    'DEZESSETE',
    'DEZOITO',
    'DEZENOVE',
  ]
  const dezenas = [
    '',
    '',
    'VINTE',
    'TRINTA',
    'QUARENTA',
    'CINQUENTA',
    'SESSENTA',
    'SETENTA',
    'OITENTA',
    'NOVENTA',
  ]
  const centenas = [
    '',
    'CENTO',
    'DUZENTOS',
    'TREZENTOS',
    'QUATROCENTOS',
    'QUINHENTOS',
    'SEISCENTOS',
    'SETECENTOS',
    'OITOCENTOS',
    'NOVECENTOS',
  ]

  if (value === 0) return 'ZERO REAIS'
  if (value === 100) return 'CEM REAIS'

  const reais = Math.floor(value)
  const centavos = Math.round((value - reais) * 100)

  let resultado = ''

  if (reais >= 100) {
    const c = Math.floor(reais / 100)
    resultado += centenas[c]
    const resto = reais % 100
    if (resto > 0) resultado += ' E '
  }

  const dezena = reais % 100

  if (dezena >= 10 && dezena <= 19) {
    resultado += dezADezenove[dezena - 10]
  } else {
    const d = Math.floor(dezena / 10)
    const u = dezena % 10

    if (d > 0) {
      resultado += dezenas[d]
      if (u > 0) resultado += ' E '
    }

    if (u > 0) {
      resultado += unidades[u]
    }
  }

  resultado += reais === 1 ? ' REAL' : ' REAIS'

  if (centavos > 0) {
    resultado += ' E '
    if (centavos >= 10 && centavos <= 19) {
      resultado += dezADezenove[centavos - 10]
    } else {
      const d = Math.floor(centavos / 10)
      const u = centavos % 10

      if (d > 0) {
        resultado += dezenas[d]
        if (u > 0) resultado += ' E '
      }

      if (u > 0) {
        resultado += unidades[u]
      }
    }
    resultado += centavos === 1 ? ' CENTAVO' : ' CENTAVOS'
  }

  return resultado
}
