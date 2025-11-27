describe('Gestão de Pontos de Embarque (Admin)', () => {
  
  const mockPoints = [
    { id: 1, name: 'Praça Central', address_reference: 'Centro', route_order: 1 },
    { id: 2, name: 'Posto Ipiranga', address_reference: 'Av. Principal', route_order: 2 }
  ];

  const createMockAdminJwt = () => {
    const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
    const payload = btoa(JSON.stringify({ 
      user_id: 1, 
      role: 'admin',
      exp: 9999999999 
    }));
    return `${header}.${payload}.fake_signature`;
  };

  beforeEach(() => {
    const adminToken = createMockAdminJwt();
    window.localStorage.setItem('access', adminToken);
    window.localStorage.setItem('refresh', 'fake_refresh');

    cy.intercept('POST', '**/api/v1/authentication/token/verify', {
      statusCode: 200, body: {} 
    }).as('verifyToken');

    cy.intercept('GET', '**/api/v1/boarding-points/', {
      statusCode: 200,
      body: mockPoints
    }).as('getPoints');

    cy.visit('/admin/pontos-embarque'); 
    
    cy.wait('@getPoints');
  });

  //CT-17: Listar pontos
  it('Deve listar os pontos de embarque corretamente', () => {
    cy.contains('h1', 'Gestão de Pontos de Embarque').should('be.visible');
    
    // Verifica se os dados do mock apareceram na tabela
    cy.contains('Praça Central').should('be.visible');
    cy.contains('Posto Ipiranga').should('be.visible');
    
    // Verifica dados secundários (referência)
    cy.contains('Centro').should('be.visible');
  });

  // CT-18: Criar
  it('Deve criar um novo ponto de embarque com sucesso', () => {
    const newPoint = { id: 3, name: 'Novo Ponto', address_reference: 'Nova Rua', route_order: 3 };

    cy.intercept('POST', '**/api/v1/boarding-points/', {
      statusCode: 201,
      body: newPoint
    }).as('createPoint');

    cy.intercept('GET', '**/api/v1/boarding-points/', {
      statusCode: 200,
      body: [...mockPoints, newPoint]
    }).as('getPointsUpdated');

    cy.contains('button', 'Novo Ponto').click();

    cy.get('input[placeholder*="Ex: Praça"]').type('Novo Ponto', {force: true}); 
    cy.get('input[placeholder*="Ex: Em frente"]').type('Nova Rua', {force: true});
    
    cy.get('input[type="number"]').clear().type('3');

    cy.contains('button', 'Salvar').click(); 

    cy.wait('@createPoint');
    cy.wait('@getPointsUpdated');
    
    cy.contains('Novo Ponto').should('be.visible'); 
  });

  // CT-19: Editar
  it('Deve editar um ponto existente', () => {
    const updatedPoint = { ...mockPoints[0], name: 'Praça Editada' };

    cy.intercept('PATCH', '**/api/v1/boarding-points/1/', {
      statusCode: 200,
      body: updatedPoint
    }).as('updatePoint');

    cy.intercept('GET', '**/api/v1/boarding-points/', {
      statusCode: 200,
      body: [updatedPoint, mockPoints[1]]
    }).as('getPointsUpdated');

    cy.contains('tr', 'Praça Central').within(() => {
      cy.get('button').first().click();
    });

    cy.get('input[placeholder*="Ex: Praça"]').clear().type('Praça Editada');

    cy.contains('button', 'Salvar').click();

    cy.wait('@updatePoint');
    cy.contains('Praça Editada').should('be.visible');
  });

  // CT-20: Deletar
  it('Deve excluir um ponto', () => {
    cy.intercept('DELETE', '**/api/v1/boarding-points/1/', {
      statusCode: 204,
      body: {}
    }).as('deletePoint');

    cy.intercept('GET', '**/api/v1/boarding-points/', {
      statusCode: 200,
      body: [mockPoints[1]]
    }).as('getPointsUpdated');

    cy.contains('tr', 'Praça Central').within(() => {
        cy.get('button').last().click();
    });

    
    cy.wait('@deletePoint');
    cy.wait('@getPointsUpdated');

    cy.contains('Praça Central').should('not.exist');
  });

});