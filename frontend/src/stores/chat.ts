import { defineStore } from 'pinia';
import type { Message } from '@/types';

interface ChatState {
  messages: Message[];
}

export const useChatStore = defineStore('chat', {
  state: (): ChatState => ({
    messages: [],
  }),

  actions: {
    addMessage(message: Message) {
      this.messages.push(message);
    },

    clear() {
      this.messages = [];
    },
  },

  getters: {
    teamMessages: (state) => (team: string) => {
      return state.messages.filter(msg => msg.team === team);
    },
  },
});
