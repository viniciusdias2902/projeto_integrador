describe('Segurança e Controle de Acesso', () => {
  
  const createMockJwt = (role) => {
    const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
    const payload = btoa(JSON.stringify({ 
      user_id: 1, 
      role: role, 
      exp: 9999999999 
    }));
    return `${header}.${payload}.fake_signature`;
  };

  beforeEach(() => {
    cy.intercept('GET', '**/api/v1/polls/', { body: [] });
    cy.intercept('GET', '**/api/v1/trips/?*', { body: [] });
  });

  // CT-05: Bloquear aluno
  it('Deve redirecionar ALUNO tentando acessar área de ADMIN', () => {
    const token = createMockJwt('student');
    window.localStorage.setItem('access', token);
    
    cy.intercept('POST', '**/api/v1/authentication/token/verify', { statusCode: 200 });

    cy.visit('/admin/estudantes');

    cy.url().should('include', '/enquetes');
    cy.url().should('not.include', '/admin');
  });

  // CT-06: Bloquar Motorista
  it('[US-03] Deve redirecionar MOTORISTA tentando acessar área de ADMIN', () => {
    const token = createMockJwt('driver');
    window.localStorage.setItem('access', token);
    
    cy.intercept('POST', '**/api/v1/authentication/token/verify', { statusCode: 200 });

    cy.visit('/admin/estudantes');

    cy.url().should('include', '/viagens');
    cy.url().should('not.include', '/admin');
  });

  // CT-26: Sessão Expirada
  it('[US-16] Deve redirecionar para LOGIN se o token estiver expirado/inválido', () => {
    const token = createMockJwt('student');
    window.localStorage.setItem('access', token);

    cy.intercept('POST', '**/api/v1/authentication/token/verify', { 
      statusCode: 401, 
      body: { detail: "Token invalid" } 
    }).as('verifyTokenFail');

    cy.visit('/enquetes');

    cy.wait('@verifyTokenFail');

    cy.location('pathname').should('eq', '/'); // Ou '/login' dependendo da sua rota base
    cy.contains('button', 'Login').should('be.visible');
  });

});