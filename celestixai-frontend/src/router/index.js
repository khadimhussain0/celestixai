import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '../components/LandingPage.vue';
import Dashboard from '../views/Dashboard.vue';
import TextCorpus from '../views/TextCorpus.vue';
import LLMs from '../views/LLMs.vue';
import LLMConstellation from '../views/LLMConstellation.vue';
import Chat from '../views/Chat.vue';
import Deployments from '../views/Deployments.vue';
import Auth from '../components/Auth.vue'
import MainApp from '../views/MainApp.vue';

const routes = [
  { path: '/landingpage', component: LandingPage },
  { path: '/', redirect: '/landingpage', meta: { requiresAuth: true } },
  { path: '/:catchAll(.*)', redirect: '/landingpage' },
  {path:  '/auth', component : Auth},
  { path: '/app', component: MainApp, meta: { requiresAuth: true } },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/text-corpus', component: TextCorpus, meta: { requiresAuth: true } },
  { path: '/llms', component: LLMs, meta: { requiresAuth: true } },
  { path: '/llm-constellation', component: LLMConstellation, meta: { requiresAuth: true } },
  { path: '/chat', component: Chat, meta: { requiresAuth: true } },
  { path: '/deployments', component: Deployments, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem('accessToken');

  if (to.matched.some(record => record.meta.requiresAuth) && !isLoggedIn) {
    next('/auth');
  } else {
    next();
  }
});

export default router;
