describe('RF 02 - Visualização de Enquetes Semanais', () => {
  
  beforeEach(() => {
    cy.request({
      method: 'POST',
      url: 'http://127.0.0.1:8000/api/v1/authentication/token/',
      body: { username: 'ana.silva@example.com', password: 'Password123' },
    }).then((response) => {
      window.localStorage.setItem('access', response.body.access);
      window.localStorage.setItem('refresh', response.body.refresh);
    });
  });

  //CT_09
  it('Deve exibir a lista de enquetes da semana corretamente', () => {
    cy.visit('/enquetes');

    cy.contains('h1', 'Enquetes de Transporte').should('be.visible');

    cy.get('fieldset').should('have.length.at.least', 1);

    cy.get('fieldset').each(($el) => {
      cy.wrap($el).invoke('text').should('match', /(Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo)/);
    });
  });

  //CT_10
  it('Deve exibir mensagem amigável quando não houver enquetes', () => {
    cy.intercept('GET', '**/api/v1/polls/', {
      statusCode: 200,
      body: [] 
    }).as('getEmptyPolls');

    cy.visit('/enquetes');
    
    cy.wait('@getEmptyPolls');

    cy.contains('Nenhuma enquete disponível').should('be.visible');
    cy.contains('Não há enquetes ativas no momento.').should('be.visible');
  });

  //CT_11
  it('Deve exibir alerta de erro quando a API falhar', () => {
    cy.intercept('GET', '**/api/v1/polls/', {
      statusCode: 500,
      body: { detail: 'Erro interno do servidor' }
    }).as('getPollsError');

    cy.visit('/enquetes');
    
    cy.wait('@getPollsError');

    cy.get('.alert-error').should('be.visible');
    cy.contains('Erro ao carregar').should('be.visible');
  });
});