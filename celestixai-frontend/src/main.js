import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import NotificationModal from '@/components/NotificationModal.vue';
const app = createApp(App);
app.use(router);
app.component('notification-modal', NotificationModal);
app.mount('#app');
