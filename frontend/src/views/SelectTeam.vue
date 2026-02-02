<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <div class="bg-gray-800 rounded-lg p-8 w-full max-w-md">
      <h2 class="text-2xl font-bold text-center mb-6">选择队伍</h2>
      
      <div class="grid grid-cols-2 gap-4 mb-6">
        <button
          @click="selectTeam('team_a')"
          class="p-6 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors"
        >
          <div class="text-center">
            <img :src="roomStore.teamA.icon" class="w-16 h-16 mx-auto mb-2" />
            <h3 class="text-lg font-semibold">{{ roomStore.teamA.name }}</h3>
          </div>
        </button>

        <button
          @click="selectTeam('team_b')"
          class="p-6 bg-gray-700 rounded-lg hover:bg-gray-600 transition-colors"
        >
          <div class="text-center">
            <img :src="roomStore.teamB.icon" class="w-16 h-16 mx-auto mb-2" />
            <h3 class="text-lg font-semibold">{{ roomStore.teamB.name }}</h3>
          </div>
        </button>
      </div>

      <div v-if="error" class="mt-4 text-red-500 text-sm">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import roomApi from '@/services/api';
import { useRoomStore } from '@/stores/room';
import { useUserStore } from '@/stores/user';
import socketService from '@/services/socket';

const router = useRouter();
const roomStore = useRoomStore();
const userStore = useUserStore();

const error = ref('');

const selectTeam = async (team: string) => {
  try {
    await roomApi.join(roomStore.roomId!, {
      session_id: userStore.sessionId,
      team,
      display_name: null,
    });

    userStore.setTeam(team);
    socketService.emitSelectTeam(roomStore.roomId!, userStore.sessionId, team);
    
    router.push('/input-name');
  } catch (err: any) {
    error.value = err.response?.data?.message || '选择队伍失败';
  }
};
</script>
