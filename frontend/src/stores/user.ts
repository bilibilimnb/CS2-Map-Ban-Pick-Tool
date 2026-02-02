import { defineStore } from 'pinia';
import type { User } from '@/types';
import { storage } from '@/utils/storage';

interface UserState {
  sessionId: string;
  userId: string | null;
  team: string | null;
  displayName: string | null;
  isReady: boolean;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    sessionId: storage.getSessionId(),
    userId: storage.getUserId(),
    team: null,
    displayName: null,
    isReady: false,
  }),

  actions: {
    setSessionId(sessionId: string) {
      this.sessionId = sessionId;
      storage.setSessionId(sessionId);
    },

    setUserId(userId: string) {
      this.userId = userId;
      storage.setUserId(userId);
    },

    setTeam(team: string) {
      this.team = team;
    },

    setDisplayName(displayName: string) {
      this.displayName = displayName;
    },

    setReady(ready: boolean) {
      this.isReady = ready;
    },

    clear() {
      this.userId = null;
      this.team = null;
      this.displayName = null;
      this.isReady = false;
      storage.clearUserData();
    },
  },

  getters: {
    isLoggedIn: (state) => !!state.userId,
    isTeamA: (state) => state.team === 'team_a',
    isTeamB: (state) => state.team === 'team_b',
    displayOrSessionName: (state) => state.displayName || `玩家${state.sessionId.slice(-4)}`,
  },
});
