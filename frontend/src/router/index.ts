import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'JoinRoom',
    component: () => import('@/views/JoinRoom.vue'),
  },
  {
    path: '/team-select',
    name: 'SelectTeam',
    component: () => import('@/views/SelectTeam.vue'),
  },
  {
    path: '/input-name',
    name: 'InputName',
    component: () => import('@/views/InputName.vue'),
  },
  {
    path: '/waiting',
    name: 'WaitingRoom',
    component: () => import('@/views/WaitingRoom.vue'),
  },
  {
    path: '/bp-process',
    name: 'BPProcess',
    component: () => import('@/views/BPProcess.vue'),
  },
  {
    path: '/result',
    name: 'BPResult',
    component: () => import('@/views/BPResult.vue'),
  },
  {
    path: '/admin',
    name: 'AdminLogin',
    component: () => import('@/views/AdminLogin.vue'),
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: () => import('@/views/AdminDashboard.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
