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
          <v-icon>headphones</v-icon>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 2}, 'item-title' ]"> {{ $t('Listeners') }}</v-list-tile-title>
      </v-list-tile>

      <v-list-tile @click="changeRoute('implants', 3)">
        <v-list-tile-action>
          <v-icon>grass</v-icon>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 3}, 'item-title' ]">{{ $t('Implants') }}</v-list-tile-title>
      </v-list-tile>

      
     <v-list-tile @click="changeRoute('venom', 4)">
        <v-list-tile-action>
          <v-icon>crisis_alert</v-icon>
        </v-list-tile-action>
        <v-list-tile-title :class="[{'active': selectedIndex === 4}, 'item-title' ]">{{ $t('Venom') }}</v-list-tile-title>
      </v-list-tile>

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
