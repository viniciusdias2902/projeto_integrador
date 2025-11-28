describe('Funcionalidade de Lista de Embarque', () => {
  
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

  // CT-12: Teste Positivo
  it('Deve exibir a lista de embarque com os pontos e alunos corretos', () => {
    // CONGELAR O TEMPO: Definir  uma data fixa
    const now = new Date('2025-11-24T10:00:00Z');
    cy.clock(now.getTime());
    const fixedDateString = '2025-11-24';

    cy.intercept('GET', '**/api/v1/polls/', {
      statusCode: 200,
      body: [
        { id: 99, date: fixedDateString, status: 'open', votes: [] }
      ]
    }).as('getPolls');

    cy.intercept('GET', '**/boarding_list/?trip_type=*', {
      statusCode: 200,
      body: [
        {
          point: { id: 1, name: 'Praça da Matriz', address_reference: 'Centro' },
          students: [
            { id: 10, name: 'Aluno Teste Cypress' }
          ]
        }
      ]
    }).as('getBoardingList');

    cy.visit('/lista-embarque');

    cy.wait('@getPolls');
    cy.wait('@getBoardingList'); 

    cy.contains('h2', 'Ida').should('be.visible');
    cy.contains('Praça da Matriz').should('be.visible');
    cy.contains('Aluno Teste Cypress').should('be.visible');
  });

  // CT-13: Sem Enquete
  it('Deve exibir mensagem quando não houver enquete para o dia', () => {
    
    cy.intercept('GET', '**/api/v1/polls/', {
      statusCode: 200,
      body: [] 
    }).as('getEmptyPolls');

    cy.visit('/lista-embarque');
    cy.wait('@getEmptyPolls');

    cy.contains('Nenhuma enquete para hoje').should('be.visible');
    cy.contains('h2', 'Ida').should('not.exist');
  });

  //CT-14: Erro na API
  it('Deve exibir erro se a API falhar', () => {
    cy.intercept('GET', '**/api/v1/polls/', {
      statusCode: 500,
      body: { detail: 'Server Error' }
    }).as('getPollsError');

    cy.visit('/lista-embarque');
    cy.wait('@getPollsError');

    cy.get('.alert-error').should('be.visible');
    cy.contains('Erro ao carregar').should('be.visible');
  });

});