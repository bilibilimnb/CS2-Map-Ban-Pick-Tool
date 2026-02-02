<template>
  <div class="min-h-screen bg-gray-900 p-4">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部信息 -->
      <div class="text-center mb-6">
        <h1 class="text-3xl font-bold text-orange-500 mb-2">等待准备</h1>
        <p class="text-gray-400">房间码: {{ roomStore.roomCode }}</p>
      </div>

      <!-- 队伍列表 -->
      <div class="grid grid-cols-2 gap-6 mb-6">
        <!-- 队伍 A -->
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="flex items-center mb-4">
            <img :src="roomStore.teamA.icon" class="w-12 h-12 mr-3" />
            <h2 class="text-xl font-bold">{{ roomStore.teamA.name }}</h2>
          </div>
          <div class="space-y-2">
            <div
              v-for="user in roomStore.users.team_a"
              :key="user.id"
              class="flex items-center justify-between bg-gray-700 rounded p-2"
            >
              <span>{{ user.display_name }}</span>
              <span
                :class="user.is_ready ? 'text-green-500' : 'text-gray-500'"
                class="text-sm"
              >
                {{ user.is_ready ? '已准备' : '未准备' }}
              </span>
            </div>
          </div>
          <div class="text-center text-gray-500 text-sm">
            {{ roomStore.users.team_a.length }}/5 人
          </div>
        </div>

        <!-- 队伍 B -->
        <div class="bg-gray-800 rounded-lg p-4">
          <div class="flex items-center mb-4">
            <img :src="roomStore.teamB.icon" class="w-12 h-12 mr-3" />
            <h2 class="text-xl font-bold">{{ roomStore.teamB.name }}</h2>
          </div>
          <div class="space-y-2">
            <div
              v-for="user in roomStore.users.team_b"
              :key="user.id"
              class="flex items-center justify-between bg-gray-700 rounded p-2"
            >
              <span>{{ user.display_name }}</span>
              <span
                :class="user.is_ready ? 'text-green-500' : 'text-gray-500'"
                class="text-sm"
              >
                {{ user.is_ready ? '已准备' : '未准备' }}
              </span>
            </div>
          </div>
          <div class="text-center text-gray-500 text-sm">
            {{ roomStore.users.team_b.length }}/5 人
          </div>
        </div>
      </div>

      <!-- 准备按钮 -->
      <div class="text-center">
        <button
          @click="toggleReady"
          :disabled="!userStore.team"
          :class="[
            'px-8 py-3 rounded-lg font-semibold transition-colors',
            userStore.isReady
              ? 'bg-gray-600 hover:bg-gray-700'
              : 'bg-green-500 hover:bg-green-600'
          ]"
        >
          {{ userStore.isReady ? '取消准备' : '我已准备' }}
        </button>
      </div>

      <!-- 提示信息 -->
      <div v-if="roomStore.users.team_a.length < 5 || roomStore.users.team_b.length < 5" class="mt-4 text-center text-yellow-500">
        等待所有玩家加入房间并准备（每队5人）
      </div>
      <div v-else-if="!allReady" class="mt-4 text-center text-yellow-500">
        等待所有玩家准备完毕
      </div>
      <div v-else class="mt-4 text-center text-green-500">
        所有玩家已准备，等待管理员开始 BP
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue';
import roomApi from '@/services/api';
import { useRoomStore } from '@/stores/room';
import { useUserStore } from '@/stores/user';
import socketService from '@/services/socket';

const roomStore = useRoomStore();
const userStore = useUserStore();

const allReady = computed(() => {
  const teamAReady = roomStore.users.team_a.every(u => u.is_ready);
  const teamBReady = roomStore.users.team_b.every(u => u.is_ready);
  return teamAReady && teamBReady;
});

const toggleReady = async () => {
  const newReady = !userStore.isReady;
  userStore.setReady(newReady);
  
  try {
    await roomApi.updateReady(roomStore.roomId!, {
      session_id: userStore.sessionId,
      is_ready: newReady,
    });
    socketService.emitReady(roomStore.roomId!, userStore.sessionId, newReady);
  } catch (err: any) {
    console.error('Update ready failed:', err);
    userStore.setReady(!newReady);
  }
};

const loadUsers = async () => {
  try {
    const response = await roomApi.getUsers(roomStore.roomId!);
    roomStore.updateUsers(response.data.data);
  } catch (err: any) {
    console.error('Load users failed:', err);
  }
};

onMounted(() => {
  socketService.connect(roomStore.roomId!, userStore.sessionId);
  socketService.on('user_joined', () => loadUsers());
  socketService.on('user_left', () => loadUsers());
  socketService.on('team_updated', () => loadUsers());
  loadUsers();
});

onUnmounted(() => {
  socketService.disconnect();
});
</script>
