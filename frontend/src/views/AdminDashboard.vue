<template>
  <div class="min-h-screen bg-gray-900">
    <!-- 顶部导航 -->
    <div class="bg-gray-800 border-b border-gray-700">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <h1 class="text-2xl font-bold text-orange-500">管理员后台</h1>
        <button
          @click="logout"
          class="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
        >
          退出登录
        </button>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="max-w-7xl mx-auto p-4">
      <!-- 标签页 -->
      <div class="flex gap-4 mb-6">
        <button
          @click="currentTab = 'rooms'"
          :class="[
            'px-6 py-2 rounded-lg transition-colors',
            currentTab === 'rooms' ? 'bg-orange-500 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          ]"
        >
          房间管理
        </button>
        <button
          @click="currentTab = 'mappools'"
          :class="[
            'px-6 py-2 rounded-lg transition-colors',
            currentTab === 'mappools' ? 'bg-orange-500 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
          ]"
        >
          地图池管理
        </button>
      </div>

      <!-- 房间管理 -->
      <div v-if="currentTab === 'rooms'" class="space-y-4">
        <!-- 创建房间表单 -->
        <div class="bg-gray-800 rounded-lg p-6 mb-6">
          <h2 class="text-xl font-bold mb-4">创建新房间</h2>
          
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label class="block text-sm font-medium mb-2">队伍 A 名称</label>
              <input
                v-model="newRoom.team_a_name"
                type="text"
                class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-orange-500 focus:outline-none"
              />
            </div>
            <div>
              <label class="block text-sm font-medium mb-2">队伍 B 名称</label>
              <input
                v-model="newRoom.team_b_name"
                type="text"
                class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-orange-500 focus:outline-none"
              />
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">地图池</label>
            <select
              v-model="newRoom.mappool_config_id"
              class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-orange-500 focus:outline-none"
            >
              <option v-for="pool in mapPools" :key="pool.id" :value="pool.id">
                {{ pool.name }}
              </option>
            </select>
          </div>

          <button
            @click="createRoom"
            :disabled="!canCreateRoom"
            class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
          >
            创建房间
          </button>
        </div>

        <!-- 房间列表 -->
        <div class="bg-gray-800 rounded-lg p-6">
          <h2 class="text-xl font-bold mb-4">房间列表</h2>
          
          <div class="space-y-2">
            <div
              v-for="room in rooms"
              :key="room.id"
              class="bg-gray-700 rounded p-4 flex justify-between items-center"
            >
              <div>
                <div class="font-bold">{{ room.room_code }}</div>
                <div class="text-sm text-gray-400">
                  {{ room.team_a_name }} vs {{ room.team_b_name }}
                </div>
                <div class="text-sm">
                  状态: 
                  <span :class="getStatusClass(room.status)">{{ getStatusText(room.status) }}</span>
                </div>
              </div>
              <button
                @click="viewRoomDetail(room.id)"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              >
                查看详情
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 地图池管理 -->
      <div v-else class="space-y-4">
        <!-- 创建地图池表单 -->
        <div class="bg-gray-800 rounded-lg p-6 mb-6">
          <h2 class="text-xl font-bold mb-4">创建新地图池</h2>
          
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2">地图池名称</label>
            <input
              v-model="newMapPool.name"
              type="text"
              class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-orange-500 focus:outline-none"
            />
          </div>

          <div class="grid grid-cols-7 gap-2 mb-4">
            <div v-for="i in 7" :key="i">
              <label class="block text-sm font-medium mb-2">地图 {{ i + 1 }}</label>
              <input
                v-model="newMapPool[`map${i < 10 ? `0${i}` : i}`_name`]"
                type="text"
                class="w-full px-3 py-2 bg-gray-700 rounded border border-gray-600 focus:border-orange-500 focus:outline-none"
              />
            </div>
          </div>

          <button
            @click="createMapPool"
            :disabled="!canCreateMapPool"
            class="w-full bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
          >
            创建地图池
          </button>
        </div>

        <!-- 地图池列表 -->
        <div class="bg-gray-800 rounded-lg p-6">
          <h2 class="text-xl font-bold mb-4">地图池列表</h2>
          
          <div class="space-y-2">
            <div
              v-for="pool in mapPools"
              :key="pool.id"
              class="bg-gray-700 rounded p-4 flex justify-between items-center"
            >
              <div>
                <div class="font-bold">{{ pool.name }}</div>
                <div class="text-sm text-gray-400">
                  {{ pool.is_default ? '默认地图池' : '自定义地图池' }}
                </div>
              </div>
              <button
                @click="deleteMapPool(pool.id)"
                class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
              >
                删除
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import adminApi from '@/services/api';

const currentTab = ref('rooms');
const rooms = ref<any[]>([]);
const mapPools = ref<any[]>([]);

const newRoom = ref({
  team_a_name: '',
  team_b_name: '',
  mappool_config_id: '',
});

const newMapPool = ref({
  name: '',
  map01_name: '',
  map02_name: '',
  map03_name: '',
  map04_name: '',
  map05_name: '',
  map06_name: '',
  map07_name: '',
});

const canCreateRoom = computed(() => {
  return newRoom.value.team_a_name.trim() &&
         newRoom.value.team_b_name.trim() &&
         newRoom.value.mappool_config_id;
});

const canCreateMapPool = computed(() => {
  return newMapPool.value.name.trim() &&
         newMapPool.value.map01_name.trim() &&
         newMapPool.value.map02_name.trim() &&
         newMapPool.value.map03_name.trim() &&
         newMapPool.value.map04_name.trim() &&
         newMapPool.value.map05_name.trim() &&
         newMapPool.value.map06_name.trim() &&
         newMapPool.value.map07_name.trim();
});

const getStatusClass = (status: string) => {
  const classes: Record<string, string> = {
    waiting: 'text-yellow-500',
    rolling: 'text-orange-500',
    ban1: 'text-red-500',
    ban2: 'text-red-500',
    pick1: 'text-green-500',
    decider: 'text-green-500',
    finished: 'text-gray-400',
  };
  return classes[status] || 'text-gray-400';
};

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    waiting: '等待中',
    rolling: 'Roll 点',
    ban1: '第一轮 Ban',
    ban2: '第二轮 Ban',
    pick1: 'Pick',
    decider: '决胜图',
    finished: '已完成',
  };
  return texts[status] || status;
};

const loadRooms = async () => {
  try {
    const response = await adminApi.getRooms();
    rooms.value = response.data.data.items;
  } catch (err: any) {
    console.error('Load rooms failed:', err);
  }
};

const loadMapPools = async () => {
  try {
    const response = await adminApi.getMapPools();
    mapPools.value = response.data.data;
  } catch (err: any) {
    console.error('Load map pools failed:', err);
  }
};

const createRoom = async () => {
  try {
    await adminApi.createRoom(newRoom.value);
    newRoom.value = { team_a_name: '', team_b_name: '', mappool_config_id: '' };
    loadRooms();
  } catch (err: any) {
    alert(err.response?.data?.message || '创建房间失败');
  }
};

const createMapPool = async () => {
  try {
    await adminApi.createMapPool(newMapPool.value);
    newMapPool.value = {
      name: '',
      map01_name: '',
      map02_name: '',
      map03_name: '',
      map04_name: '',
      map05_name: '',
      map06_name: '',
      map07_name: '',
    };
    loadMapPools();
  } catch (err: any) {
    alert(err.response?.data?.message || '创建地图池失败');
  }
};

const deleteMapPool = async (id: string) => {
  if (!confirm('确定要删除这个地图池吗？')) return;
  
  try {
    await adminApi.delete(`/admin/mappools/${id}`);
    loadMapPools();
  } catch (err: any) {
    alert(err.response?.data?.message || '删除地图池失败');
  }
};

const viewRoomDetail = (roomId: string) => {
  // TODO: 实现房间详情查看
  alert('房间详情查看功能待实现');
};

const logout = () => {
  localStorage.removeItem('admin_token');
  window.location.href = '/admin';
};

onMounted(() => {
  loadRooms();
  loadMapPools();
});
</script>
