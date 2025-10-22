describe('Cadastro de estudante', () => {
  const baseUrl = 'http://localhost:5173/cadastro' 

  it('Deve cadastrar um novo estudante com sucesso', () => {
    cy.visit(baseUrl, { timeout: 20000 })

    cy.get('form', { timeout: 20000 }).should('exist')

    cy.contains('Nome Completo').parent().find('input', { timeout: 10000 }).type('José Henrique')
    cy.contains('E-mail').parent().find('input', { timeout: 10000 }).type('teste@cypress.com')
    cy.contains('Senha').parent().find('input', { timeout: 10000 }).type('Senha1234')
    cy.contains('Telefone').parent().find('input', { timeout: 10000 }).type('1234567890')
    cy.contains('Universidade').parent().find('select').select('UESPI')
    cy.contains('Turno').parent().find('select').select('M')

    cy.get('button[type="submit"]').click()

    cy.get('div.alert-success', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Cadastro realizado com sucesso')
  })
})
