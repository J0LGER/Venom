<template>
  <v-navigation-drawer
    v-model="toggle"
    fixed app>
    <v-toolbar flat dark :color="$root.themeColor" class="toolbar">
      <router-link :to="{ name: 'Dashboard' }">
        <img src="static/app/logo.png" width="36px"></img>
      </router-link>
      <router-link :to="{ name: 'Dashboard' }" class="text">
         Venom
      </router-link>
    </v-toolbar>
    <v-list>
      <v-list-tile @click="changeRoute('Dashboard', 1)">
        <v-list-tile-action>
          <v-icon>dashboard</v-icon>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 1}, 'item-title' ]" >{{ $t('dashboard') }}</v-list-tile-title>
      </v-list-tile>

      <v-list-tile @click="changeRoute('listeners', 2)">
        <v-list-tile-action>
          <v-icon>group</v-icon>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 2}, 'item-title' ]"> {{ $t('Listeners') }}</v-list-tile-title>
      </v-list-tile>

      <v-list-tile @click="changeRoute('implants', 3)">
        <v-list-tile-action>
          <v-icon>mail</v-icon>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 3}, 'item-title' ]">{{ $t('Implants') }}</v-list-tile-title>
      </v-list-tile>

      
     <v-list-tile @click="changeRoute('venom', 4)">
        <v-list-tile-action>
          <v-icon>group</v-icon>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 3}, 'item-title' ]">{{ $t('Venom') }}</v-list-tile-title>
      </v-list-tile>



      <v-list-group
        prepend-icon="select_all">
        <v-list-tile slot="activator">
          <v-list-tile-title class="item-title">{{ $t('overlays') }}</v-list-tile-title>
        </v-list-tile>
        <v-list-tile @click="changeRoute('Snackbar', 7)">
          <v-list-tile-action>
            <v-icon>event_note</v-icon>
          </v-list-tile-action>
          <v-list-tile-title :class="[{'active': selectedIndex === 7}, 'item-title' ]">{{ $t('snackbar') }}</v-list-tile-title>
        </v-list-tile>
    </v-list-group>

      <v-list-group
        prepend-icon="fingerprint">
        <v-list-tile slot="activator">
          <v-list-tile-title class="item-title">{{ $t('authorization') }}</v-list-tile-title>
        </v-list-tile>

        <v-list-tile @click="$router.push({ name: 'Error', params: { errorCode: '403' } })">
          <v-list-tile-action>
            <v-icon>cancel</v-icon>
          </v-list-tile-action>
          <v-list-tile-title class="item-title">403</v-list-tile-title>
        </v-list-tile>

        <v-list-tile @click="$router.push({ name: 'Error', params: { errorCode: '404' } })">
          <v-list-tile-action>
            <v-icon>cancel</v-icon>
          </v-list-tile-action>
          <v-list-tile-title class="item-title">404</v-list-tile-title>
        </v-list-tile>

        <v-list-tile @click="$router.push({ name: 'Error', params: { errorCode: '500' } })">
          <v-list-tile-action>
            <v-icon>cancel</v-icon>
          </v-list-tile-action>
          <v-list-tile-title class="item-title">500</v-list-tile-title>
        </v-list-tile>

        <v-list-tile @click="$router.push({ name: 'Login' })">
          <v-list-tile-action>
            <v-icon>cancel</v-icon>
          </v-list-tile-action>
          <v-list-tile-title class="item-title">{{ $t('login') }}</v-list-tile-title>
        </v-list-tile>
    </v-list-group>

      <v-list-group
      prepend-icon="account_circle">
      <v-list-tile slot="activator">
        <v-list-tile-title class="item-title">{{ $t('users') }}</v-list-tile-title>
      </v-list-tile>
        <v-list-tile  @click="">
            <v-list-tile-action>
              <v-icon v-text="'people_outline'"></v-icon>
            </v-list-tile-action>
            <v-list-tile-title v-text="'Management'"></v-list-tile-title>
      </v-list-tile>
      <v-list-tile  @click="">
          <v-list-tile-action>
            <v-icon v-text="'settings'"></v-icon>
          </v-list-tile-action>
          <v-list-tile-title v-text="'Settings'"></v-list-tile-title>
      </v-list-tile>
    </v-list-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    toggle: {
        type: Boolean,
        required: false,
        default: true
    }
  },

  data() {
    return {
      selectedIndex: 1
    }
  },

  methods: {
    changeRoute(routeName, selectedIndex) {
      const vm = this;

      vm.selectedIndex = selectedIndex;

      return vm.$router.push({ name: routeName });
    }
  }
}
</script>

<style>
  .toolbar {
    font-weight: bold;
    font-size: 18px;
  }

  .toolbar .text {
    padding-left: 15px;
    color: white;
    text-decoration:none;
  }

  .item-title {
    font-size: 17px;
    font-weight: 500;
  }
  .item-sub-title {
    font-size: 15px;
    font-weight: 500;
  }

  .active {
    font-weight: bold;
  }
</style>
