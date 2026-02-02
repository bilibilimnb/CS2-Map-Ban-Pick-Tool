import { defineStore } from 'pinia';
import type { BPState, MapCard, RollResult, BPResult } from '@/types';
import { OPERATION_TIME } from '@/utils/constants';

interface BPState {
  phase: number;
  currentTeam: string | null;
  currentUser: string | null;
  remainingTime: number;
  maps: MapCard[];
  rollResult: RollResult | null;
  result: BPResult | null;
}

export const useBPStore = defineStore('bp', {
  state: (): BPState => ({
    phase: 0,
    currentTeam: null,
    currentUser: null,
    remainingTime: OPERATION_TIME,
    maps: [
      { id: 'map01', name: 'Mirage', icon: '/assets/images/default-map-icon.png', status: 'available' },
      { id: 'map02', name: 'Inferno', icon: '/assets/images/default-map-icon.png', status: 'available' },
      { id: 'map03', name: 'Dust2', icon: '/assets/images/default-map-icon.png', status: 'available' },
      { id: 'map04', name: 'Nuke', icon: '/assets/images/default-map-icon.png', status: 'available' },
      { id: 'map05', name: 'Anubis', icon: '/assets/images/default-map-icon.png', status: 'available' },
      { id: 'map06', name: 'Vertigo', icon: '/assets/images/default-map-icon.png', status: 'available' },
      { id: 'map07', name: 'Ancient', icon: '/assets/images/default-map-icon.png', status: 'available' },
    ],
    rollResult: null,
    result: null,
  }),

  actions: {
    setPhase(phase: number) {
      this.phase = phase;
    },

    setCurrentTeam(team: string) {
      this.currentTeam = team;
    },

    setCurrentUser(user: string) {
      this.currentUser = user;
    },

    setRemainingTime(time: number) {
      this.remainingTime = time;
    },

    updateMapStatus(mapId: string, status: 'banned' | 'picked' | 'decider', team?: string) {
      const map = this.maps.find(m => m.id === mapId);
      if (map) {
        map.status = status;
        if (team) {
          if (status === 'banned') {
            map.banned_by = team;
          } else {
            map.picked_by = team;
          }
        }
      }
    },

    setRollResult(result: RollResult) {
      this.rollResult = result;
    },

    setResult(result: BPResult) {
      this.result = result;
    },

    reset() {
      this.phase = 0;
      this.currentTeam = null;
      this.currentUser = null;
      this.remainingTime = OPERATION_TIME;
      this.maps.forEach(m => {
        m.status = 'available';
        m.banned_by = undefined;
        m.picked_by = undefined;
        m.teammate_intent = undefined;
      });
      this.rollResult = null;
      this.result = null;
    },
  },
});
