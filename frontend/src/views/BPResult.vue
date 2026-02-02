<template>
  <div class="min-h-screen bg-gray-900 p-4">
    <div class="max-w-6xl mx-auto">
      <!-- 顶部 Roll 结果 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-orange-500 mb-4">BP 结果</h1>
        <div class="flex justify-center gap-8 mb-6">
          <div class="bg-gray-800 rounded-lg p-6 flex-1">
            <img :src="roomStore.teamA.icon" class="w-16 h-16 mx-auto mb-2" />
            <h2 class="text-2xl font-bold">{{ roomStore.teamA.name }}</h2>
            <div class="text-4xl font-bold mt-4">{{ bpStore.rollResult?.roll_a ?? '-' }}</div>
          </div>
          <div class="text-4xl font-bold text-gray-400">VS</div>
          <div class="bg-gray-800 rounded-lg p-6 flex-1">
            <img :src="roomStore.teamB.icon" class="w-16 h-16 mx-auto mb-2" />
            <h2 class="text-2xl font-bold">{{ roomStore.teamB.name }}</h2>
            <div class="text-4xl font-bold mt-4">{{ bpStore.rollResult?.roll_b ?? '-' }}</div>
          </div>
        </div>
        <p class="text-gray-400">
          {{ bpStore.rollResult?.roll_a! > bpStore.rollResult?.roll_b ? roomStore.teamA.name : roomStore.teamB.name }}
          获得先手
        </p>
      </div>

      <!-- 结果网格 -->
      <div class="grid grid-cols-7 gap-3 mb-8">
        <div
          v-for="(result, index) in resultItems"
          :key="index"
          :class="[
            'relative rounded-lg overflow-hidden',
            result.type === 'banned' ? 'opacity-50' : ''
          ]"
        >
          <!-- 地图图片 -->
          <img :src="result.map.icon" class="w-full aspect-square object-cover" />
          
          <!-- 标签 -->
          <div
            :class="[
              'absolute top-0 left-0 right-0 px-2 py-1 text-center text-white text-xs font-bold',
              result.type === 'banned' ? 'bg-red-500' : 'bg-green-500'
            ]"
          >
            <span v-if="result.type === 'banned'">
              BANED BY {{ result.team === 'team_a' ? roomStore.teamA.name : roomStore.teamB.name }}
            </span>
            <span v-else-if="result.type === 'picked'">
              PICKED BY {{ result.team === 'team_a' ? roomStore.teamA.name : roomStore.teamB.name }}
            </span>
            <span v-else>DECIDER</span>
          </div>

          <!-- 地图名称 -->
          <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-80 px-2 py-1 text-center">
            <div class="text-white font-bold">{{ result.map.name }}</div>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div class="text-center">
        <button
          @click="exitRoom"
          class="px-8 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
        >
          退出房间
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useRoomStore } from '@/stores/room';
import { useBPStore } from '@/stores/bp';
import { useUserStore } from '@/stores/user';
import socketService from '@/services/socket';

const router = useRouter();
const roomStore = useRoomStore();
const bpStore = useBPStore();
const userStore = useUserStore();

const resultItems = computed(() => {
  if (!bpStore.result) return [];
  
  const items = [
    bpStore.result.phase_1_ban,
    bpStore.result.phase_2_ban,
    bpStore.result.phase_3_pick,
    bpStore.result.phase_4_pick,
    bpStore.result.phase_5_ban,
    bpStore.result.phase_6_ban,
    { map_id: bpStore.result.decider.map_id, type: 'decider', team: '' },
  ];
  
  return items.map((item, index) => ({
    ...item,
    map: {
      id: item.map_id,
      name: getMapName(item.map_id),
      icon: getMapIcon(item.map_id),
    },
    type: index < 2 ? 'banned' : index < 4 ? 'picked' : index < 6 ? 'banned' : 'decider',
  }));
});

const getMapName = (mapId: string) => {
  const mapNames: Record<string, string> = {
    map01: roomStore.mappool.map01_name,
    map02: roomStore.mappool.map02_name,
    map03: roomStore.mappool.map03_name,
    map04: roomStore.mappool.map04_name,
    map05: roomStore.mappool.map05_name,
    map06: roomStore.mappool.map06_name,
    map07: roomStore.mappool.map07_name,
  };
  return mapNames[mapId] || '未知地图';
};

const getMapIcon = (mapId: string) => {
  const mapIcons: Record<string, string> = {
    map01: roomStore.mappool.map01_icon,
    map02: roomStore.mappool.map02_icon,
    map03: roomStore.mappool.map03_icon,
    map04: roomStore.mappool.map04_icon,
    map05: roomStore.mappool.map05_icon,
    map06: roomStore.mappool.map06_icon,
    map07: roomStore.mappool.map07_icon,
  };
  return mapIcons[mapId] || '/assets/images/default-map-icon.png';
};

const exitRoom = () => {
  roomStore.clear();
  bpStore.reset();
  userStore.clear();
  socketService.disconnect();
  router.push('/');
};

onMounted(() => {
  // BP 结果已在 BPProcess 组件中设置
});
</script>
