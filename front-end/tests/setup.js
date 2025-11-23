import { config } from '@vue/test-utils';
import { createRouter, createMemoryHistory } from 'vue-router';
import { vi } from 'vitest';

// 1. Configura o Roteador Mock
const testRoutes = [
  { path: '/', name: 'login', component: { template: '<div>Login</div>' } },
  { path: '/enquetes', name: 'polls', component: { template: '<div>Polls</div>' } },
  { path: '/lista-embarque', name: 'boarding-list', component: { template: '<div>Boarding</div>' } },
  { path: '/cadastro', name: 'registration-page', component: { template: '<div>Register</div>' } },
];

const testRouter = createRouter({
  history: createMemoryHistory(),
  routes: testRoutes,
});

config.global.plugins.push(testRouter);

// 2. CORREÇÃO DO TOKEN: JWT Falso com estrutura válida (Base64)
// Header.Payload.Signature -> O payload contém { "user_id": 1 }
const FAKE_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxfQ.signature";

// 3. Mock Global do LocalStorage
const localStorageMock = {
  getItem: vi.fn((key) => {
    if (key === 'access') return FAKE_JWT;
    return null;
  }),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

vi.stubGlobal('localStorage', localStorageMock);

// 4. MOCK GLOBAL DO FETCH (Segurança contra ECONNREFUSED)
// Se um teste não definir seu próprio mock, este será usado.
const globalFetch = vi.fn((url) => {
  // Se for autenticação, retorna sucesso para não quebrar o fluxo
  if (url.includes('token') || url.includes('verify')) {
    return Promise.resolve({ ok: true, json: async () => ({}) });
  }
  // Para qualquer outra coisa, retorna lista vazia para não quebrar .map ou .length
  return Promise.resolve({ ok: true, json: async () => [] });
});

vi.stubGlobal('fetch', globalFetch);