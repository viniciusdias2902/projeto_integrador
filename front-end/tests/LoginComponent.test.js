import { mount } from '@vue/test-utils';
import LoginComponent from '@/components/LoginComponent.vue';  
import { describe, it, expect } from 'vitest';


describe("LoginComponent", () => {
  it("retorna se o email tem formato válido", async() => {
    const wrapper = mount(LoginComponent);
    const emailInput = wrapper.find('input[type="email"]')

    await emailInput.setValue('teste@email.com')
    expect(emailInput.element.validity.valid).toBe(true);
  });
    it("retorna erro se o email for inválido", async() => {
      const wrapper = mount(LoginComponent);
      const emailInput = wrapper.find('input[type="email"]')

      await emailInput.setValue('testeerro.com')
      expect(emailInput.element.validity.valid).toBe(false);
    });
  });


describe("LoginComponent", () => {
  it("retorna se a senha tem formato válido", async() => {
    const wrapper = mount(LoginComponent);
    const senhaInput = wrapper.find('input[type="password"]')

    await senhaInput.setValue('senha123')
    const senhaValida = senhaInput.element.value.length >= 8;
    expect(senhaValida).toBe(true);
  });

  it("retorna erro se a senha for inválida", async() => {
    const wrapper = mount(LoginComponent);
    const senhaInput = wrapper.find('input[type="password"]')

    await senhaInput.setValue('123')
    const senhaValida = senhaInput.element.value.length >= 8;
    expect(senhaValida).toBe(false);
  });
});

