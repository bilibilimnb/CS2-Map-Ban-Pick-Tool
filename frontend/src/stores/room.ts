import { defineStore } from 'pinia';
import type { Room, MapPoolConfig, RoomStatus } from '@/types';

interface RoomState {
  roomId: string | null;
  roomCode: string | null;
  teamA: { name: string; icon: string };
  teamB: { name: string; icon: string };
  status: RoomStatus;
  mappool: MapPoolConfig;
  users: { team_a: any[]; team_b: any[] };
}

export const useRoomStore = defineStore('room', {
  state: (): RoomState => ({
    roomId: null,
    roomCode: null,
    teamA: { name: '队伍 A', icon: '/assets/images/default-team-icon.png' },
    teamB: { name: '队伍 B', icon: '/assets/images/default-team-icon.png' },
    status: 'waiting',
    mappool: {
      map01_name: 'Mirage',
      map01_icon: '/assets/images/default-map-icon.png',
      map02_name: 'Inferno',
      map02_icon: '/assets/images/default-map-icon.png',
      map03_name: 'Dust2',
      map03_icon: '/assets/images/default-map-icon.png',
      map04_name: 'Nuke',
      map04_icon: '/assets/images/default-map-icon.png',
      map05_name: 'Anubis',
      map05_icon: '/assets/images/default-map-icon.png',
      map06_name: 'Vertigo',
      map06_icon: '/assets/images/default-map-icon.png',
      map07_name: 'Ancient',
      map07_icon: '/assets/images/default-map-icon.png',
    },
    users: { team_a: [], team_b: [] },
  }),

  actions: {
    setRoom(room: Room) {
      this.roomId = room.id;
      this.roomCode = room.room_code;
      this.teamA = { name: room.team_a_name, icon: room.team_a_icon };
      this.teamB = { name: room.team_b_name, icon: room.team_b_icon };
      this.status = room.status;
      this.mappool = room.mappool;
    },

    setRoomStatus(status: RoomStatus) {
      this.status = status;
    },

    updateUsers(users: { team_a: any[]; team_b: any[] }) {
      this.users = users;
    },

    clear() {
      this.roomId = null;
      this.roomCode = null;
      this.status = 'waiting';
      this.users = { team_a: [], team_b: [] };
    },
  },
});
