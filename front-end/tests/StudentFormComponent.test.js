import StudentForm from '@/components/StudentForm.vue';  
import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import  flushPromises  from 'flush-promises';

describe("StudentForm", () => {
    it("mostra mensagem de erro se o e-mail já estiver sido cadastrado", async() => {
        vi.stubGlobal('fetch', vi.fn(() =>
          Promise.resolve({
            ok: false,
            json: async () => ({ email: ['This email is already in use'] }),
})
    ));

    const wrapper = mount(StudentForm);

     await wrapper.setData({
      form: {
        name: 'Maria Rita',
        email: 'teste@email.com',
        password: 'senha123',
        phone: '1234567890',
        university: 'UESPI',
        class_shift: 'A',
        boarding_point: 1,
      }
    })
    await wrapper.find('form').trigger('submit.prevent');
    await flushPromises();
    expect(wrapper.text()).toContain('Esse email já está sendo usado por outro usuário.');

    });
});