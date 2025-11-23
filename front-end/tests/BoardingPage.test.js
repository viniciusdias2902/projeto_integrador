import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import BoardingPage from '@/pages/BoardingPage.vue';
import flushPromises from 'flush-promises';

describe('BoardingPage', () => {
  
  beforeEach(() => {
    vi.clearAllMocks();
  });

  // Teste positivo de carregamento bem sucedido
  it('deve buscar a enquete do dia e renderizar a lista de embarque', async () => {
    const today = new Date().toISOString().split('T')[0];
    
    vi.stubGlobal('fetch', vi.fn((url) => {
      if (url.includes('token')) return Promise.resolve({ ok: true, json: async () => ({}) });

      if (url.includes('polls/') && !url.includes('boarding_list')) {
        return Promise.resolve({
          ok: true,
          json: async () => [{ id: 5, date: today }], 
        });
      }

      if (url.includes('boarding_list')) {
        return Promise.resolve({
          ok: true,
          json: async () => [
            { 
              point: { id: 1, name: 'Ponto A - Praça Central' }, 
              students: [{ id: 10, name: 'Ana Silva' }] 
            }
          ],
        });
      }

      return Promise.resolve({ ok: true, json: async () => [] });
    }));

    const wrapper = mount(BoardingPage);
    
    await flushPromises(); // Carrega Enquete
    await flushPromises(); // Carrega Lista

    expect(wrapper.text()).toContain('Ana Silva');
    expect(wrapper.text()).toContain('Ponto A - Praça Central');
  });

  // teste falha de rede
  it('deve mostrar uma mensagem de erro se a busca da enquete falhar', async () => {
    vi.stubGlobal('fetch', vi.fn((url) => {
      if (url.includes('token')) return Promise.resolve({ ok: true });
      return Promise.reject(new Error('Falha de rede'));
    }));

    const wrapper = mount(BoardingPage);
    await flushPromises();

    expect(wrapper.text()).toContain('Erro ao carregar');
  });

  // Teste ausencia de enquetes
  it('deve mostrar mensagem se não houver enquete para o dia', async () => {
    vi.stubGlobal('fetch', vi.fn((url) => {
        if (url.includes('token')) return Promise.resolve({ ok: true });
        return Promise.resolve({ ok: true, json: async () => [] });
    }));

    const wrapper = mount(BoardingPage);
    await flushPromises();

    expect(wrapper.text()).toContain('Nenhuma enquete para hoje');
  });
});