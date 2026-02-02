<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <div class="bg-gray-800 rounded-lg p-8 w-full max-w-md">
      <h1 class="text-2xl font-bold text-center mb-6 text-orange-500">管理员登录</h1>
      
      <div class="mb-4">
        <label class="block text-sm font-medium mb-2">用户名</label>
        <input
          v-model="username"
          type="text"
          placeholder="输入管理员用户名"
          class="w-full px-4 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:border-orange-500 focus:outline-none"
        />
      </div>

      <div class="mb-6">
        <label class="block text-sm font-medium mb-2">密码</label>
        <input
          v-model="password"
          type="password"
          placeholder="输入密码"
          class="w-full px-4 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:border-orange-500 focus:outline-none"
          @keyup.enter="login"
        />
      </div>

      <button
        @click="login"
        :disabled="!username.trim() || !password.trim()"
        class="w-full bg-orange-500 text-white py-2 px-4 rounded-lg hover:bg-orange-600 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
      >
        登录
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
import adminApi from '@/services/api';
import storage from '@/utils/storage';

const router = useRouter();

const username = ref('');
const password = ref('');
const error = ref('');

const login = async () => {
  if (!username.value.trim() || !password.value.trim()) {
    error.value = '请输入用户名和密码';
    return;
  }

  try {
    const response = await adminApi.login({
      username: username.value.trim(),
      password: password.value.trim(),
    });
    
    const token = response.data.data.token;
    localStorage.setItem('admin_token', token);
    
    router.push('/admin/dashboard');
  } catch (err: any) {
    error.value = err.response?.data?.message || '登录失败，请检查用户名和密码';
  }
};
</script>
