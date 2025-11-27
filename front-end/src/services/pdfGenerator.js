import jsPDF from 'jspdf'
import { numberToWords } from '@/utils/numberToWords'
import { parseLocalDate } from '@/utils/dateUtils'
import logoImage from '@/assets/images/recibo-logo.png'

export async function generatePaymentReceipt(student) {
  const doc = new jsPDF()

  const universities = {
    UESPI: 'UESPI',
    CHRISFAPI: 'CHRISFAPI',
    IFPI: 'IFPI',
    ETC: 'OUTRO',
  }

  const university = universities[student.university] || student.university
  const monthlyPaymentReais = student.monthly_payment_cents / 100
  const valueInWords = numberToWords(monthlyPaymentReais)

  // Usar a data do último pagamento ao invés da data atual
  let receiptDate
  if (student.last_payment_date && student.last_payment_date !== 'não informado') {
    receiptDate = parseLocalDate(student.last_payment_date)
  } else {
    // Fallback para data atual se não houver data de pagamento
    receiptDate = new Date()
  }

  const day = String(receiptDate.getDate()).padStart(2, '0')
  const months = [
    'JANEIRO',
    'FEVEREIRO',
    'MARÇO',
    'ABRIL',
    'MAIO',
    'JUNHO',
    'JULHO',
    'AGOSTO',
    'SETEMBRO',
    'OUTUBRO',
    'NOVEMBRO',
    'DEZEMBRO',
  ]
  const month = months[receiptDate.getMonth()]
  const year = receiptDate.getFullYear()

  doc.setFontSize(16)
  doc.setFont(undefined, 'bold')
  const title = `Recibo de pagamento (${university})`
  const titleWidth = doc.getTextWidth(title)
  const pageWidth = doc.internal.pageSize.getWidth()
  doc.text(title, (pageWidth - titleWidth) / 2, 30)

  doc.setFontSize(12)
  doc.setFont(undefined, 'normal')

  const marginLeft = 20
  const marginRight = 20
  const textWidth = pageWidth - marginLeft - marginRight
  let yPosition = 50

  const text1 = `Recebi do Sr(a). ${student.name.toUpperCase()} brasileira (o), Residente da cidade de PIRACURUCA, Estado PIAUÍ a quantia de R$(${monthlyPaymentReais.toFixed(2).replace('.', ',')}), ${valueInWords}, referente a transporte, dando-lhe por este recibo a devida quitação.`

  const lines1 = doc.splitTextToSize(text1, textWidth)
  doc.text(lines1, marginLeft, yPosition)
  yPosition += lines1.length * 7 + 20

  doc.text(`Local e Data: PIRACURUCA, ${day} de ${month} de ${year}`, marginLeft, yPosition)
  yPosition += 20

  doc.setFont(undefined, 'italic')
  doc.text('JAQUELINE MACEDO.', marginLeft, yPosition)
  yPosition += 10

  doc.setFont(undefined, 'normal')
  doc.text('Assinatura', marginLeft, yPosition)
  yPosition += 20

  try {
    const img = new Image()
    img.src = logoImage

    await new Promise((resolve, reject) => {
      img.onload = () => {
        const imgWidth = 80
        const imgHeight = (img.height * imgWidth) / img.width
        const imgX = (pageWidth - imgWidth) / 2

        doc.addImage(img, 'PNG', imgX, yPosition, imgWidth, imgHeight)
        resolve()
      }
      img.onerror = reject
    })
  } catch (error) {
    console.error('Error loading image:', error)
  }

  const fileName = `recibo_${student.name.replace(/\s+/g, '_')}_${day}_${month}_${year}.pdf`
  doc.save(fileName)
}
