<template>
  <div class="min-h-screen bg-gray-900 p-4">
    <div class="max-w-7xl mx-auto">
      <!-- 顶部进度条 -->
      <div class="mb-6">
        <div class="flex justify-between items-center mb-2">
          <h2 class="text-2xl font-bold text-orange-500">BP 流程</h2>
          <div class="text-right">
            <span class="text-4xl font-bold" :class="bpStore.remainingTime <= 5 ? 'text-red-500' : 'text-white'">
              {{ bpStore.remainingTime }}
            </span>
            <span class="text-gray-400 ml-2">秒</span>
          </div>
        </div>
        
        <!-- 阶段指示器 -->
        <div class="flex gap-2 mb-2">
          <div
            v-for="(phase, index) in BP_PHASES"
            :key="phase.phase"
            :class="[
              'flex-1 text-center py-2 rounded',
              index + 1 === bpStore.phase ? 'bg-orange-500' : 'bg-gray-700'
            ]"
          >
            <div class="text-sm font-medium">{{ phase.instruction }}</div>
            <div v-if="index + 1 === bpStore.phase" class="text-xs mt-1 text-white">
              {{ bpStore.remainingTime }}s
            </div>
          </div>
        </div>
      </div>

      <!-- 主界面 -->
      <div class="grid grid-cols-12 gap-4">
        <!-- 左侧队伍 A -->
        <div class="col-span-2 bg-gray-800 rounded-lg p-4">
          <div class="flex items-center mb-4">
            <img :src="roomStore.teamA.icon" class="w-10 h-10 mr-2" />
            <h3 class="text-lg font-bold">{{ roomStore.teamA.name }}</h3>
          </div>
          <div class="space-y-2">
            <div
              v-for="user in roomStore.users.team_a"
              :key="user.id"
              class="bg-gray-700 rounded p-2 text-sm"
              :class="{
                'border-2 border-orange-500': bpStore.currentTeam === 'team_a' && bpStore.currentUser === user.display_name
              }"
            >
              {{ user.display_name }}
            </div>
          </div>
        </div>

        <!-- 中间地图池 -->
        <div class="col-span-8 bg-gray-800 rounded-lg p-6">
          <div class="text-center mb-4">
            <div v-if="bpStore.phase === 0" class="text-2xl font-bold text-yellow-500">
              等待 Roll 点
            </div>
            <div v-else class="text-lg font-semibold">
              <span v-if="bpStore.currentTeam === 'team_a'" class="text-orange-500">
                {{ roomStore.teamA.name }}
              </span>
              <span v-else class="text-blue-500">
                {{ roomStore.teamB.name }}
              </span>
              <span class="text-gray-400">正在</span>
              <span v-if="['ban1', 'ban2', 'ban3', 'ban4'].includes(getCurrentPhaseName())" class="text-red-500">
                禁用
              </span>
              <span v-else class="text-green-500">
                选择
              </span>
              <span class="text-gray-400">地图</span>
            </div>
          </div>

          <!-- 地图网格 -->
          <div class="grid grid-cols-7 gap-3">
            <div
              v-for="map in bpStore.maps"
              :key="map.id"
              @click="handleMapClick(map)"
              :class="[
                'relative rounded-lg p-3 cursor-pointer transition-all',
                getMapCardClass(map)
              ]"
            >
              <!-- 地图图标 -->
              <img :src="map.icon" class="w-full aspect-square object-cover rounded mb-2" />
              
              <!-- 地图名称 -->
              <div class="text-center font-bold text-white text-sm mb-1">
                {{ map.name }}
              </div>

              <!-- 队友意向 -->
              <div v-if="map.teammate_intent" class="text-xs text-gray-400 text-center">
                {{ map.teammate_intent }}
              </div>

              <!-- 状态图标 -->
              <div v-if="map.status !== 'available'" class="absolute top-2 right-2">
                <div v-if="map.status === 'banned'" class="bg-red-500 text-white px-2 py-1 rounded text-xs font-bold">
                  ×
                </div>
                <div v-else-if="map.status === 'picked'" class="bg-green-500 text-white px-2 py-1 rounded text-xs font-bold">
                  ✓
                </div>
                <div v-else-if="map.status === 'decider'" class="bg-yellow-500 text-white px-2 py-1 rounded text-xs font-bold">
                  DECIDER
                </div>
              </div>

              <!-- 操作标签 -->
              <div v-if="map.status !== 'available'" class="absolute top-0 left-0 right-0 bg-black bg-opacity-70 rounded-t-lg px-2 py-1">
                <div class="text-xs text-white font-bold text-center">
                  <span v-if="map.order === 1">1st - {{ map.picked_by }}</span>
                  <span v-else-if="map.order === 2">2nd - {{ map.picked_by }}</span>
                  <span v-else-if="map.status === 'decider'">3rd - DECIDER</span>
                  <span v-else>{{ map.banned_by }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧队伍 B -->
        <div class="col-span-2 bg-gray-800 rounded-lg p-4">
          <div class="flex items-center mb-4">
            <img :src="roomStore.teamB.icon" class="w-10 h-10 mr-2" />
            <h3 class="text-lg font-bold">{{ roomStore.teamB.name }}</h3>
          </div>
          <div class="space-y-2">
            <div
              v-for="user in roomStore.users.team_b"
              :key="user.id"
              class="bg-gray-700 rounded p-2 text-sm"
              :class="{
                'border-2 border-blue-500': bpStore.currentTeam === 'team_b' && bpStore.currentUser === user.display_name
              }"
            >
              {{ user.display_name }}
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天框 -->
      <div class="mt-6 bg-gray-800 rounded-lg p-4">
        <div class="flex items-center mb-4">
          <h3 class="text-lg font-bold">队伍聊天</h3>
          <span class="text-gray-400 text-sm ml-4">（仅队内可见）</span>
        </div>
        <div class="h-48 overflow-y-auto mb-4 space-y-2">
          <div
            v-for="msg in chatStore.teamMessages(userStore.team!)"
            :key="msg.timestamp"
            class="bg-gray-700 rounded p-2"
          >
            <span class="text-orange-500 font-bold">[{{ roomStore.teamA.name === userStore.team ? roomStore.teamA.name : roomStore.teamB.name }}]</span>
            <span class="text-white font-semibold ml-2">{{ msg.user_name }}:</span>
            <span class="text-gray-300 ml-2">{{ msg.content }}</span>
          </div>
        </div>
        <div class="flex gap-2">
          <input
            v-model="chatMessage"
            type="text"
            placeholder="输入消息..."
            class="flex-1 px-4 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:border-orange-500 focus:outline-none"
            @keyup.enter="sendChat"
          />
          <button
            @click="sendChat"
            :disabled="!chatMessage.trim()"
            class="px-6 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:bg-gray-600 disabled:cursor-not-allowed"
          >
            发送
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useRoomStore } from '@/stores/room';
import { useUserStore } from '@/stores/user';
import { useBPStore } from '@/stores/bp';
import { useChatStore } from '@/stores/chat';
import socketService from '@/services/socket';
import { BP_PHASES } from '@/utils/constants';

const router = useRouter();
const roomStore = useRoomStore();
const userStore = useUserStore();
const bpStore = useBPStore();
const chatStore = useChatStore();

const chatMessage = ref('');

const getCurrentPhaseName = () => {
  const phaseNames: Record<number, string> = {
    1: 'ban1',
    2: 'ban2',
    3: 'pick1',
    4: 'pick2',
    5: 'ban3',
    6: 'ban4',
    7: 'decider',
  };
  return phaseNames[bpStore.phase];
};

const getMapCardClass = (map: any) => {
  if (map.status === 'banned') {
    return 'opacity-50 border-2 border-red-500';
  }
  if (map.status === 'picked') {
    return 'border-2 border-green-500';
  }
  if (map.status === 'decider') {
    return 'border-2 border-yellow-500';
  }
  if (map.is_current) {
    return 'border-2 border-orange-500 hover:border-orange-400';
  }
  return 'hover:bg-gray-700';
};

const canOperate = computed(() => {
  return bpStore.currentTeam === userStore.team && bpStore.currentUser === userStore.displayName;
});

const handleMapClick = (map: any) => {
  if (!canOperate.value) return;
  if (map.status !== 'available') return;
  
  const action = ['ban1', 'ban2', 'ban3', 'ban4'].includes(getCurrentPhaseName()) ? 'ban_map' : 'pick_map';
  socketService[action](roomStore.roomId!, userStore.sessionId, map.id);
};

const sendChat = () => {
  if (!chatMessage.value.trim()) return;
  
  socketService.emitSendChat(roomStore.roomId!, userStore.sessionId, chatMessage.value.trim());
  chatMessage.value = '';
};

onMounted(() => {
  socketService.connect(roomStore.roomId!, userStore.sessionId);
  
  socketService.on('bp_started', (data) => {
    bpStore.setRollResult(data);
  });
  
  socketService.on('bp_phase_changed', (data) => {
    bpStore.setPhase(data.phase);
    bpStore.setCurrentTeam(data.current_team);
    bpStore.setCurrentUser(data.current_user);
    bpStore.setRemainingTime(15);
  });
  
  socketService.on('map_banned', (data) => {
    bpStore.updateMapStatus(data.map_id, 'banned', data.team);
  });
  
  socketService.on('map_picked', (data) => {
    bpStore.updateMapStatus(data.map_id, 'picked', data.team);
  });
  
  socketService.on('timer_tick', (data) => {
    bpStore.setRemainingTime(data.remaining_time);
  });
  
  socketService.on('chat_message', (data) => {
    chatStore.addMessage(data);
  });
  
  socketService.on('bp_finished', (data) => {
    bpStore.setResult(data);
    router.push('/result');
  });
});

onUnmounted(() => {
  socketService.disconnect();
});
</script>
