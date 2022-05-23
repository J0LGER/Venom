import Vue from 'vue';
import Router from 'vue-router';

import Dashboard from '../pages/Dashboard.vue';
import Social from '../pages/Social.vue';
import Media from '../pages/Media.vue';
import Snackbar from '../pages/Snackbar.vue';
import Chart from '../pages/Chart.vue';
import Implants from '../pages/Implants.vue';
import Listeners from '../pages/Listeners.vue';
import Venom from '../pages/Venom.vue';
import Login from '../pages/core/Login.vue';
import Error from '../pages/core/Error.vue';



Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard,
      meta: {
        breadcrumb: [
          { name: 'dashboard' }
        ]
      }
    },
    {
      path: '/implants',
      name: 'implants',
      component: Implants,
      meta: {
        breadcrumb: [
          { name: 'dashboard', href: 'Dashboard' },
          { name: 'implants' }
        ]
      }
    },
    {
      path: '/listeners',
      name: 'listeners',
      component: Listeners,
      meta: {
        breadcrumb: [
          { name: 'dashboard', href: 'Dashboard' },
          { name: 'listeners' }
        ]
      }
    },
    {
      path: '/venom',
      name: 'venom',
      component: Venom,
      meta: {
        breadcrumb: [
          { name: 'dashboard', href: 'Dashboard' },
          { name: 'venom' }
        ]
      }
    },
    {
      path: '/error',
      name: 'Error',
      component: Error,
      meta: {
        allowAnonymous: true
      }
    },
  ]
});
