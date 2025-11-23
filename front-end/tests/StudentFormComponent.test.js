import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import StudentForm from '@/components/StudentForm.vue';
import flushPromises from 'flush-promises';

describe("StudentForm", () => {

  const createFetchMock = (postOk, postResponse) => {
    return vi.fn((url, options) => {
      if (url.includes('boarding-points')) {
        return Promise.resolve({
          ok: true,
          json: async () => [
            { id: 1, name: 'Ponto A' },
            { id: 2, name: 'Ponto B' }
          ],
        });
      }

      if (url.includes('students') && options?.method === 'POST') {
        return Promise.resolve({
          ok: postOk,
          json: async () => postResponse,
        });
      }

      return Promise.resolve({ ok: true, json: async () => [] });
    });
  };

  const fillInput = async (wrapper, selector, value) => {
    let input = wrapper.find(selector);
    if (!input.exists()) {
        input = wrapper.find(`${selector} input`);
    }
    if (input.exists()) {
        await input.setValue(value);
    } else {
        const typeSelector = selector.replace('#', 'input[type="').replace('name', 'text') + '"]'; 
        const typeInput = wrapper.find(typeSelector);
        if(typeInput.exists()) await typeInput.setValue(value);
    }
  };

  // Teste Duplicidade
  it("mostra mensagem de erro se o e-mail já estiver sido cadastrado", async () => {
    vi.stubGlobal('fetch', createFetchMock(false, { email: ['This email is already in use'] }));

    const wrapper = mount(StudentForm);
    await flushPromises();

    await fillInput(wrapper, '#name', 'Maria Rita');
    await fillInput(wrapper, '#email', 'teste@email.com');
    await fillInput(wrapper, '#password', 'Senha123');
    await fillInput(wrapper, '#phone', '12345678901');
    
    const selects = wrapper.findAll('select');
    if (selects.length >= 3) {
        await selects[0].setValue('UESPI'); 
        await selects[1].setValue('M');     
        await selects[2].setValue(1); 
    }

    await wrapper.find('form').trigger('submit.prevent');
    await flushPromises(); // espera o submit

    expect(wrapper.text()).toContain('Esse email já está sendo usado por outro usuário.');
  });

  // Teste Limpeza
  it("limpa os campos após cadastro bem-sucedido", async () => {
    vi.stubGlobal('fetch', createFetchMock(true, { id: 1 }));

    const wrapper = mount(StudentForm);
    await flushPromises();

    // Preenche dados
    await fillInput(wrapper, '#name', 'Nome Valido');
    await fillInput(wrapper, '#email', 'novo@email.com');
    await fillInput(wrapper, '#password', 'Senha123');
    await fillInput(wrapper, '#phone', '11999999999');
    
    const selects = wrapper.findAll('select');
    if (selects.length >= 3) {
        await selects[0].setValue('UESPI');
        await selects[1].setValue('M');
        await selects[2].setValue(1);
    }

    await wrapper.find('form').trigger('submit.prevent');
    await flushPromises();

    let emailInput = wrapper.find('#email');
    if (!emailInput.element || emailInput.element.tagName !== 'INPUT') {
        emailInput = wrapper.find('#email input');
    }
    
    if (!emailInput.exists()) emailInput = wrapper.find('input[type="email"]');

    expect(emailInput.element.value).toBe('');
  });
});