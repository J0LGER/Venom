<template>
  <v-toolbar
    dark
    app
    :color="$root.themeColor">
    <v-toolbar-title>
      <v-toolbar-side-icon @click="toggleNavigationBar"></v-toolbar-side-icon>
    </v-toolbar-title>
    <v-text-field
      flat
      solo-inverted
      append-icon="search"
      :label="$t('search')">
    </v-text-field>
    <v-spacer></v-spacer>
    
    <v-dialog
      v-model="dialog"
      width="500">
      <v-btn icon slot="activator">
        <v-icon medium>rate_review</v-icon>
      </v-btn>
      <v-card>
        <v-card-title class="headline grey lighten-2"
          primary-title>
          Privacy Policy
        </v-card-title>

        <v-card-text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="dialog = false">
            I accept
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="dialogSettings"
      width="700">
      <v-card>
        <v-card-title class="headline"
          primary-title>
          Settings
        </v-card-title>

        <v-card-text>
          Choose theme color ?
          <swatches v-model="$root.themeColor" inline colors="material-dark" :exceptions="['#FFFFFF']" shapes="circles" show-border></swatches>
        </v-card-text>

        <v-card-text>
          Set Up System User
          <v-form>
            <v-container>
              <v-layout row wrap>

                <v-flex xs12 xs6 md11>
                  <v-text-field
                    v-model="userEmail"
                    label="User Email"
                    hint="Set user email"/>
                </v-flex>

                <v-flex xs12 xs6 md1 />

                <v-flex xs12 sm6 md11>
                  <v-text-field
                    v-model="password"
                    :append-icon="showPassword ? 'visibility_off' : 'visibility'"
                    :type="showPassword ? 'text' : 'password'"
                    label="New Password"
                    hint="Please choose a complex one.."
                    :error="error"
                    @click:append="showPassword = !showPassword" />
                </v-flex>

                <v-flex xs12 sm6 md1 />

                <v-flex xs12 sm6 md11>
                  <v-text-field
                    v-model="passwordConfirm"
                    :append-icon="showPasswordConfirm ? 'visibility_off' : 'visibility'"
                    :type="showPasswordConfirm ? 'text' : 'password'"
                    label="Confirm New Password"
                    hint="and confirm it."
                    :error="error"
                    @click:append="showPasswordConfirm = !showPasswordConfirm" />
                </v-flex>

                <v-flex xs12 sm6 md1 />

                <v-flex xs12 xs6 md11>
                  <v-switch
                    label="Email Notification"
                    color="success"
                    v-model="switchEmailNotification" />
                </v-flex>

                <v-flex xs12 xs6 md1 />

              </v-layout>
            </v-container>
          </v-form>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="setUpSettings">
            Save Changes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      v-model="showResult"
      :timeout="2000"
      top>
      {{ result }}
    </v-snackbar>

    <v-btn icon href="https://github.com/J0LGER/Venom" :ripple="false">
      <v-icon medium>fab fa-github</v-icon>
    </v-btn>
    
    <v-menu class="toolbar-menu-item" offset-y origin="center center" :nudge-bottom="10" transition="scale-transition">
      <v-btn icon large flat slot="activator" :ripple="false">
        <v-avatar size="42px">
          <img src="https://st4.depositphotos.com/1832477/27386/v/1600/depositphotos_273866520-stock-illustration-hacker-using-a-laptop-icon.jpg"/>
        </v-avatar>
      </v-btn>
      <v-list>
        <v-list-tile
          v-for="(item,index) in items"
          :key="index"
          :to="!item.href ? { name: item.name } : null"
          :href="item.href"
          ripple="ripple"
          :disabled="item.disabled"
          :target="item.target"
          @click="item.click">
          <v-list-tile-action v-if="item.icon">
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-menu>
  </v-toolbar>
</template>
<script>

export default {
  data() {
    return {
      rating: null,
      dialog: false,
      dialogSettings: false,
      switchEmailNotification: true,
      showPassword: null,
      showPasswordConfirm: null,
      userEmail: null,
      password: null,
      passwordConfirm: null,
      error: false,
      showResult: false,
      result: '',
      items: [
        {
          icon: 'account_circle',
          href: '#',
          title: 'Profile',
          click: (e) => {
          }
        },
        {
          icon: 'settings',
          href: '#',
          title: 'Settings',
          click: () => {
            const vm = this;

            vm.dialogSettings = true;
          }
        },
        {
          icon: 'exit_to_app',
          href: '#',
          title: 'Log Out',
          click: () => {
            const vm = this;

            vm.$router.push({ name: 'Login' });
          }
        }
      ],
      notifications:
      [
        {
          title: 'New mail from Adam Joe',
          color: 'light-blue',
          icon: 'email',
          actionAt: '12 min ago',
          isActive: true,
          onClick: () => {
            const vm = this;

            vm.$router.push({ name: 'Mailbox' });
          }
        },
        {
          title: 'Scheculed meeting',
          color: 'red',
          icon: 'calendar_today',
          actionAt: '46 min ago',
          isActive: true,
          onClick: () => {
            const vm = this;

            vm.$router.push({ name: 'Calendar' });
          }
        },
        {
          title: 'New mail from Github',
          color: 'light-blue',
          icon: 'email',
          isActive: true,
          timeLabel: '2 hour ago',
          onClick: () => {
            const vm = this;

            vm.$router.push({ name: 'Mailbox' });
          }
        }
      ],
      languages: [
        { name: 'English', languageCode: 'en', path: require('../../assets/flags/en.png') },
        { name: 'Turkish', languageCode: 'tr', path: require('../../assets/flags/tr.png') },
        { name: 'French', languageCode: 'fr', path: require('../../assets/flags/fr.png') },
        { name: 'German', languageCode: 'de', path: require('../../assets/flags/de.png') },
        { name: 'Japanese', languageCode: 'ja', path: require('../../assets/flags/ja.png') },
        { name: 'Simplified Chinese', languageCode: 'ch', path: require('../../assets/flags/ch.png') }
      ]
    }
  },

  computed: {
    selectedLanguageFlag() {
      const vm = this;

      switch(vm.$i18n.locale) {
        case 'en': return require('../../assets/flags/en.png');
        case 'tr': return require('../../assets/flags/tr.png');
        case 'fr': return require('../../assets/flags/fr.png');
        case 'de': return require('../../assets/flags/de.png');
        case 'ja': return require('../../assets/flags/ja.png');
        case 'ch': return require('../../assets/flags/ch.png');
      }
    }
  },
  methods: {
    toggleNavigationBar() {
      const vm = this;

      vm.$emit('toggleNavigationBar');
    },

    setUpSettings() {
      const vm = this;

      if (vm.userEmail === null || vm.password === null || vm.passwordConfirm === null) {

        vm.result = "Email and Password can't be null.";
        vm.showResult = true;

        return;
      }

      if (vm.password !== vm.passwordConfirm) {

        vm.error = true;
        vm.result = "Passwords does not match the confirm password.";
        vm.showResult = true;

        return;
      }

      vm.$root.userEmail = vm.userEmail;
      vm.$root.userPassword = vm.password;

      vm.result = "Email and password changed succesfully.";
      vm.showResult = true;

      vm.dialogSettings = false;
    },

    selectLanguage(code) {
      const vm = this;

      vm.$root.setLanguage(code);
    }
  }
};
</script>
<style>
  .toolbar-menu-item {
    padding-left: 5px;
  }

  .selected-language-flag {
    max-width: 45px;
  }

  .language-flag {
    max-width: 40px;
  }


  .languages-list-item {
    cursor: pointer;
    margin-top: -2px;
    margin-left: 1px;
  }

  .languages-list-item-title {
    font-size: 16px;
  }

  .languages-list-item-title:hover {
    color: #41B883;
    font-weight: bold;
  }
  .language-menu {
    border-radius: 25px;
    width: 235px;
    margin-right: 10px;
  }
  
  
</style>