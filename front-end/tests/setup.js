import { config } from '@vue/test-utils';
import { createRouter, createMemoryHistory } from 'vue-router';

const testRoutes = [
  { path: '/', name: 'login', component: { template: '<div></div>' } },
  { path: '/enquetes', name: 'polls', component: { template: '<div></div>' } },
  { path: '/lista-embarque', name: 'boarding-list', component: { template: '<div></div>' } },
  { path: '/cadastro', name: 'registration-page', component: { template: '<div></div>' } },
];

const testRouter = createRouter({
  history: createMemoryHistory(),
  routes: testRoutes,
});

config.global.plugins.push(testRouter);