describe('Funcionalidade de Login', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('Deve fazer login com sucesso com credenciais válidas e redirecionar', () => {
    const userEmail = 'ana.silva@example.com';
    const userPassword = 'Password123';

    cy.get('input[type="email"]').type(userEmail);
    cy.get('input[type="password"]').type(userPassword);

    cy.contains('button', 'Login').click();

    cy.url().should('include', '/enquetes');
    cy.window().its('localStorage').invoke('getItem', 'access').should('exist');
  });

  it('Deve mostrar mensagem de erro com credenciais inválidas', () => {
    const invalidEmail = 'usuario@errado.com';
    const invalidPassword = 'senhaerrada';

    cy.get('input[type="email"]').type(invalidEmail);
    cy.get('input[type="password"]').type(invalidPassword);

    cy.contains('button', 'Login').click();

    cy.get('.alert-error', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Email ou senha inválidos');
    cy.url().should('not.include', '/enquetes');
  });

  it('Deve mostrar erro se tentar logar com campos vazios', () => {
     cy.contains('button', 'Login').click();
     cy.url().should('not.include', '/enquetes');
  });
});