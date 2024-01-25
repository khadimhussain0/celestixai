import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import TextCorpus from '../views/TextCorpus.vue';
import LLMs from '../views/LLMs.vue';
import LLMConstellation from '../views/LLMConstellation.vue';
import Chat from '../views/Chat.vue';
import Deployments from '../views/Deployments.vue';
import CreateAccount from '../components/CreateAccount.vue'
import Login from '../views/Login.vue';
import MainApp from '../views/MainApp.vue';

const routes = [
  { path: '/', redirect: '/dashboard', meta: { requiresAuth: true } },
  { path: '/app', component: MainApp, meta: { requiresAuth: true } },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/text-corpus', component: TextCorpus, meta: { requiresAuth: true } },
  { path: '/llms', component: LLMs, meta: { requiresAuth: true } },
  { path: '/llm-constellation', component: LLMConstellation, meta: { requiresAuth: true } },
  { path: '/chat', component: Chat, meta: { requiresAuth: true } },
  { path: '/deployments', component: Deployments, meta: { requiresAuth: true } },
  {path:  '/signup', component : CreateAccount},
  { path: '/login', component: Login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('accessToken');

  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;
