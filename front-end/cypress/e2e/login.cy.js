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

});