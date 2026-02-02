<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <div class="bg-gray-800 rounded-lg p-8 w-full max-w-md">
      <h2 class="text-2xl font-bold text-center mb-6">输入名称</h2>
      
      <div class="mb-6">
        <label class="block text-sm font-medium mb-2">你在队伍中的名称</label>
        <input
          v-model="displayName"
          type="text"
          placeholder="输入你的游戏内名称"
          class="w-full px-4 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:border-orange-500 focus:outline-none"
          maxlength="50"
        />
      </div>

      <button
        @click="submitName"
        :disabled="!displayName.trim()"
        class="w-full bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
      >
        确认
      </button>

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

const displayName = ref('');
const error = ref('');

const submitName = async () => {
  if (!displayName.value.trim()) {
    error.value = '请输入名称';
    return;
  }

  try {
    await roomApi.join(roomStore.roomId!, {
      session_id: userStore.sessionId,
      team: userStore.team,
      display_name: displayName.value.trim(),
    });

    userStore.setDisplayName(displayName.value.trim());
    socketService.emitUpdateName(roomStore.roomId!, userStore.sessionId, displayName.value.trim());
    
    router.push('/waiting');
  } catch (err: any) {
    error.value = err.response?.data?.message || '设置名称失败';
  }
};
</script>
