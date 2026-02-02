<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <div class="bg-gray-800 rounded-lg p-8 w-full max-w-md">
      <h1 class="text-3xl font-bold text-center mb-8 text-orange-500">CS2 地图 Ban Pick 工具</h1>
      
      <div class="mb-6">
        <label class="block text-sm font-medium mb-2">房间码</label>
        <input
          v-model="roomCode"
          type="text"
          placeholder="输入8位房间码"
          class="w-full px-4 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:border-orange-500 focus:outline-none"
          maxlength="8"
        />
      </div>

      <button
        @click="joinRoom"
        :disabled="!roomCode.trim()"
        class="w-full bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
      >
        加入房间
      </button>

      <div v-if="error" class="mt-4 text-red-500 text-sm">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import roomApi from '@/services/api';
import { useRoomStore } from '@/stores/room';
import { useUserStore } from '@/stores/user';
import storage from '@/utils/storage';

const router = useRouter();
const roomStore = useRoomStore();
const userStore = useUserStore();

const roomCode = ref('');
const error = ref('');

const joinRoom = async () => {
  if (!roomCode.value.trim()) {
    error.value = '请输入房间码';
    return;
  }

  try {
    const response = await roomApi.getByCode(roomCode.value.trim());
    const room = response.data.data;
    
    roomStore.setRoom(room);
    
    // 获取用户信息
    const sessionId = storage.getSessionId();
    const joinResponse = await roomApi.join(room.id, {
      session_id: sessionId,
      team: null,
      display_name: null,
    });
    
    userStore.setSessionId(sessionId);
    userStore.setUserId(joinResponse.data.data.user_id);
    
    router.push('/team-select');
  } catch (err: any) {
    error.value = err.response?.data?.message || '加入房间失败，请检查房间码是否正确';
  }
};
</script>
