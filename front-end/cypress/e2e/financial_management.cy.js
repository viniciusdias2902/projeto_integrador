describe('Gestão Financeira', () => {
  
  const TODAY = '2025-11-24'; 
  const NOW_TIMESTAMP = new Date(`${TODAY}T12:00:00Z`).getTime();

  const DATE_PAID = TODAY; 
  const DATE_LATE = '2025-10-10'; // varios dias atrás

  const mockStudentPaid = {
    id: 1,
    name: 'Aluno Em Dia',
    phone: '11999999999',
    class_shift: 'M',
    university: 'UESPI', 
    boarding_point: 1,
    monthly_payment_cents: 35000, 
    last_payment_date: DATE_PAID
  };

  const mockStudentLate = {
    id: 2,
    name: 'Aluno Atrasado',
    phone: '11888888888',
    class_shift: 'N',
    university: 'IFPI',
    boarding_point: 2,
    monthly_payment_cents: 35000,
    last_payment_date: DATE_LATE
  };

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
    cy.clock(NOW_TIMESTAMP, ['Date']); 

    const adminToken = createMockJwt('admin');
    window.localStorage.setItem('access', adminToken);
    window.localStorage.setItem('refresh', 'fake_refresh');

    cy.intercept('POST', '**/api/v1/authentication/token/verify', { statusCode: 200, body: {} });

    cy.intercept('GET', '**/api/v1/students/', {
      statusCode: 200,
      body: [mockStudentPaid, mockStudentLate]
    }).as('getStudents');

    cy.visit('/admin/estudantes');
    cy.wait('@getStudents');
  });

  // CT-15: Visualizar Tabela
  it('Deve visualizar a tabela com status financeiros calculados corretamente', () => {
    cy.contains('h1', 'Gestão de Estudantes').should('be.visible');

    cy.contains('tr', 'Aluno Em Dia').within(() => {
      cy.contains('Universidade Estadual do Piauí').should('be.visible');
      cy.contains('R$ 350,00').should('be.visible'); 
      cy.contains('24/11/2025').should('be.visible');
      
      cy.contains('Em dia').scrollIntoView().should('be.visible'); 
    });

    cy.contains('tr', 'Aluno Atrasado').within(() => {
      cy.contains('10/10/2025').should('be.visible');
      
      cy.contains('Atrasado').scrollIntoView().should('be.visible');
    });
  });

  // CT-16 Atualizar Pagamento
  it('Deve atualizar o pagamento de um aluno manualmente', () => {

    const updatedStudent = {
      ...mockStudentLate,
      last_payment_date: TODAY,
      monthly_payment_cents: 35000
    };

    cy.intercept('PATCH', `**/api/v1/students/${mockStudentLate.id}/payment/`, {
      statusCode: 200,
      body: updatedStudent
    }).as('updatePayment');

    cy.intercept('GET', '**/api/v1/students/', {
      statusCode: 200,
      body: [mockStudentPaid, updatedStudent] 
    }).as('getStudentsReload');

    cy.contains('tr', 'Aluno Atrasado').within(() => {
      cy.get('button').first().click();
    });

    cy.get('.modal-box').should('be.visible').within(() => {
        cy.contains('h3', 'Editar Pagamento').should('be.visible');
        
        cy.get('input[type="date"]').clear().type(TODAY);
        
        cy.get('input[placeholder="500.00"]').clear().type('350.00');

        cy.contains('button', 'Salvar').click();
    });

    cy.wait('@updatePayment');
    
    cy.get('.alert-success').should('contain', 'Informações de pagamento atualizadas');

    cy.tick(1600); 
    
    cy.wait('@getStudentsReload');

    cy.get('.modal-box').should('not.be.visible');

    cy.contains('tr', 'Aluno Atrasado').within(() => {
        
        cy.contains('Em dia').scrollIntoView().should('be.visible');
        cy.contains('24/11/2025').should('be.visible');
    });
  });


  // CT-17: Exportação CSV (US-14)
  it('Deve permitir exportar os dados para CSV', () => {
    cy.visit('/admin/estudantes', {
      onBeforeLoad(win) {
        cy.spy(win.URL, 'createObjectURL').as('createObjectUrl');
      },
    });
    cy.wait('@getStudents');

    cy.contains('button', 'Exportar como CSV').click();

    cy.get('@createObjectUrl').should('have.been.called');
  });

  // CT-18: Gerar comprovante (teste positivo)
  it('Deve gerar recibo com sucesso para aluno em dia', () => {
    cy.contains('tr', 'Aluno Em Dia').within(() => {
      cy.contains('button', 'Recibo').should('not.be.disabled').click();
    });

    cy.get('.alert-success', { timeout: 10000 })
      .should('be.visible')
      .and('contain.text', 'Recibo gerado com sucesso!');
  });

 // CT-19: Nao pode gerar comprovante (Teste negativo)
  it('Deve impedir geração de recibo para aluno atrasado', () => {
    cy.contains('tr', 'Aluno Atrasado').within(() => {
      cy.get('button[disabled]').should('exist');
      
      cy.contains('.badge', 'Bloqueado').scrollIntoView().should('be.visible');
    });

    cy.get('.alert-success').should('not.exist');
  });

});