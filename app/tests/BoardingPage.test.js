import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import BoardingComponent from '@/components/BoardingComponent.vue';
import flushPromises from 'flush-promises';

beforeEach(() => {
  vi.stubGlobal('localStorage', {
    getItem: vi.fn().mockReturnValue('fake_token'),
  });
});

describe('BoardingComponent', () => {

  it('deve buscar e renderizar a lista de embarque quando montado com um pollId', async () => {
    const mockBoardingData = [
      {
        point: { id: 1, name: 'Ponto A - Praça Central' },
        students: [
          { id: 10, name: 'Ana Silva' },
          { id: 12, name: 'Bruno Costa' },
        ],
      },
    ];

    vi.stubGlobal('fetch', vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: async () => mockBoardingData,
      })
    ));

    const wrapper = mount(BoardingComponent, {
      props: {
        boardingType: 'Ida',
        pollId: 5,
      },
    });

    await flushPromises();

    const componentText = wrapper.text();
    expect(componentText).toContain('Ponto A - Praça Central (2 alunos)');
    expect(componentText).toContain('Ana Silva');
    expect(componentText).toContain('Bruno Costa');
    expect(componentText).not.toContain('Nenhum aluno confirmado');
  });

});