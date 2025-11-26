describe('RF 11 - Gestão e Visualização de Viagens', () => {
  
  const FIXED_DATE = '2025-11-24'; 
  const NOW_TIMESTAMP = new Date(`${FIXED_DATE}T10:00:00Z`).getTime();

  const mockPoll = { id: 1, date: FIXED_DATE, status: 'open' };
  
  const mockPoints = [
    { id: 1, name: 'Ponto A', route_order: 0 },
    { id: 2, name: 'Ponto B', route_order: 1 }
  ];

  const mockStopsA = [
    { boarding_point: mockPoints[0], is_current: true, students: [], student_count: 0 },
    { boarding_point: mockPoints[1], is_current: false, students: [], student_count: 0 }
  ];

  const mockStopsB = [
    { boarding_point: mockPoints[0], is_current: false, students: [], student_count: 0 },
    { boarding_point: mockPoints[1], is_current: true, students: [], student_count: 0 }
  ];

  const mockTripPending = {
    id: 100, poll: 1, trip_type: 'outbound', status: 'pending',
    current_boarding_point: null, total_stops: 2, current_stop_index: null, 
    stops: mockStopsA
  };

  const mockTripInProgressA = {
    ...mockTripPending, status: 'in_progress', current_boarding_point: mockPoints[0],
    stops: mockStopsA
  };

  const mockTripInProgressB = {
    ...mockTripPending, status: 'in_progress', current_boarding_point: mockPoints[1],
    stops: mockStopsB
  };

  const mockTripCompleted = {
    ...mockTripPending, status: 'completed', current_boarding_point: null,
    stops: mockStopsB
  };

  const createMockJwt = (role) => {
    const header = btoa(JSON.stringify({ alg: "HS256", typ: "JWT" }));
    const payload = btoa(JSON.stringify({ user_id: 1, role: role, exp: 9999999999 }));
    return `${header}.${payload}.fake_signature`;
  };

  beforeEach(() => {
    cy.clock(NOW_TIMESTAMP); 
    cy.intercept('POST', '**/api/v1/authentication/token/verify', { statusCode: 200, body: {} }).as('verifyToken');
    cy.intercept('GET', '**/api/v1/polls/', { statusCode: 200, body: [mockPoll] }).as('getPolls');
  });

  // set up do motorista
  describe('Visão do Motorista (Controle)', () => {
    beforeEach(() => {
      const driverToken = createMockJwt('driver');
      window.localStorage.setItem('access', driverToken);
      window.localStorage.setItem('refresh', 'fake_refresh');

      cy.intercept('GET', '**/api/v1/trips/?*', { statusCode: 200, body: [mockTripPending] }).as('checkTrip');
      
      cy.intercept('GET', '**/api/v1/trips/100/', { statusCode: 200, body: mockTripPending }).as('getTripDetails');
      
      cy.intercept('GET', '**/trips/*/status/', { statusCode: 200, body: { trip: mockTripPending } });
    });

    //CT-13 crud de viagens
    it('Deve permitir iniciar, avançar e finalizar uma viagem', () => {
      // --- MOCKS DE AÇÃO (POST) ---
      cy.intercept('POST', '**/trips/100/start/', { statusCode: 200, body: { message: 'Iniciada', trip: mockTripInProgressA } }).as('startTrip');
      cy.intercept('POST', '**/trips/100/next_stop/', { statusCode: 200, body: { message: 'Avançado', trip: mockTripInProgressB } }).as('nextStop');
      cy.intercept('POST', '**/trips/100/complete/', { statusCode: 200, body: { message: 'Finalizada', trip: mockTripCompleted } }).as('completeTrip');

      // --- INÍCIO ---
      cy.visit('/viagens'); 
      cy.wait('@getPolls');
      cy.wait(1000);

      cy.get('select').first().should('have.value', '1');
      cy.contains('button', 'Carregar Viagem').click();
      cy.wait('@checkTrip'); 

      cy.contains('Pendente').should('be.visible');
      
      cy.intercept('GET', '**/api/v1/trips/100/', { body: mockTripInProgressA }); 
      cy.intercept('GET', '**/trips/*/status/', { body: { trip: mockTripInProgressA } });

      cy.contains('button', 'Iniciar').click(); 
      cy.wait('@startTrip');

      cy.tick(1100); 

      
      cy.contains('Ponto A').should('be.visible');

      cy.intercept('GET', '**/api/v1/trips/100/', { body: mockTripInProgressB });
      cy.intercept('GET', '**/trips/*/status/', { body: { trip: mockTripInProgressB } });

      cy.contains('button', 'Próximo').click(); 
      cy.wait('@nextStop');
      
      cy.tick(1100);

      cy.contains('Ponto B').should('be.visible');

      cy.intercept('GET', '**/api/v1/trips/100/', { body: mockTripCompleted });

      cy.contains('button', 'Encerrar Viagem').click(); 
      cy.wait('@completeTrip');

      cy.get('.alert-success').should('exist');
    });
  });

  //set up aluno
  describe('Visão do Aluno (Visualização)', () => {
    beforeEach(() => {
      const studentToken = createMockJwt('student');
      window.localStorage.setItem('access', studentToken);
      window.localStorage.setItem('refresh', 'fake_refresh');
    });

    // CT-14 visualizar viagem
    it('Deve exibir o status atual e o ponto do ônibus', () => {
      const activeTrip = mockTripInProgressA;

      cy.intercept('GET', '**/api/v1/trips/?*', (req) => {
        if (req.url.includes('outbound')) req.reply({ statusCode: 200, body: [activeTrip] });
        else req.reply({ statusCode: 200, body: [] });
      }).as('getOutboundList');

      cy.intercept('GET', `**/api/v1/trips/${activeTrip.id}/`, {
        statusCode: 200, body: activeTrip
      }).as('getTripDetail');
      
      cy.intercept('GET', `**/api/v1/trips/${activeTrip.id}/status/`, {
         trip: activeTrip, current_students: [], current_student_count: 0
      }).as('getTripStatus');

      cy.visit('/acompanhar-viagem');
      cy.wait('@getPolls');
      cy.wait(1000);

      cy.get('body').then(($body) => {
        if ($body.find(':contains("Ponto A")').length === 0) {
           if ($body.find('button:contains("Carregar")').length > 0) {
               cy.contains('button', 'Carregar').click();
           }
        }
      });

      cy.wait('@getOutboundList');
      
      cy.tick(1100);

      cy.contains('Ponto A').should('be.visible'); 
    });
  });
});