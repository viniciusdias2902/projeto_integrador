import { mount } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import PollsPage from '@/pages/PollsPage.vue';
import PollComponent from '@/components/PollComponent.vue';
import flushPromises from 'flush-promises';

beforeEach(() => {
  vi.stubGlobal('localStorage', {
    getItem: vi.fn().mockReturnValue('fake_token'),
  });
});

describe('PollsPage', () => {
  it('deve renderizar a lista de enquetes quando a API retorna com sucesso', async () => {
    const mockPolls = [
      { id: 1, date: '2025-10-13', votes: [] },
      { id: 2, date: '2025-10-14', votes: [] },
      { id: 3, date: '2025-10-15', votes: [] },
    ];
    vi.stubGlobal('fetch', vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: async () => mockPolls,
      })
    ));

    const wrapper = mount(PollsPage);

    await flushPromises();

    const pollComponents = wrapper.findAllComponents(PollComponent);
    expect(pollComponents.length).toBe(3);
  });
});
