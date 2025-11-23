describe('Funcionalidade de Votação nas Enquetes', () => {
  beforeEach(() => {
    cy.request({
      method: 'POST',
      url: 'http://127.0.0.1:8000/api/v1/authentication/token/',
      body: { username: 'ana.silva@example.com', password: 'Password123' },
    }).then((response) => {
      window.localStorage.setItem('access', response.body.access);
      window.localStorage.setItem('refresh', response.body.refresh);
    });
    cy.visit('/enquetes');
    cy.wait(1500);
  });

  //CT_5
  it('Deve permitir que um aluno vote em uma opção e mostrar sucesso', () => {
    cy.contains('fieldset', 'Sexta', { timeout: 10000 }).should('be.visible').within(() => {
      cy.contains('label', 'Ida e volta').find('input[type="radio"]').check();
      cy.contains('button', 'Enviar Resposta').click();

      cy.get('.alert-success', { timeout: 10000 })
        .should('be.visible')
        .and('contain.text', 'Voto enviado com sucesso!');
    });
  });

  //CT_6
  it('Deve permitir que o aluno altere o voto', () => {
     cy.contains('fieldset', 'Sexta', { timeout: 10000 }).should('be.visible').within(() => {
        cy.contains('label', 'Apenas ida').find('input[type="radio"]').check();
        cy.contains('button', 'Atualizar Voto').click(); 
        cy.get('.alert-success', { timeout: 10000 })
          .should('be.visible')
          .and('contain.text', 'Voto atualizado com sucesso!');

        cy.contains('label', 'Não vou').find('input[type="radio"]').check();
        cy.contains('button', 'Atualizar Voto').click();

        cy.get('.alert-success', { timeout: 10000 })
          .should('be.visible')
          .and('contain.text', 'Voto atualizado com sucesso!'); 
     });
  });
});