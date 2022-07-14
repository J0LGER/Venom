<template>
  <v-card
    class="mx-auto timeline"
    max-width="380">
    <v-card
      dark
      flat>
      <v-card-title class="pa-2 purple lighten-3">
        <h3 class="title font-weight-light text-xs-center grow">Current Time</h3>
      </v-card-title>
      <v-img
        src="https://img.freepik.com/free-photo/colorful-3d-shapes-vaporwave-style_23-2148981126.jpg?w=996&t=st=1653735300~exp=1653735900~hmac=9542c704eb1046966f79a02b3579651597c28ca03b783a9f41cfafe09361080c"
        gradient="to top, rgba(0,0,0,.44), rgba(0,0,0,.44)">
        <v-container fill-height>
          <v-layout align-center>
            <strong class="display-3 font-weight-light mr-4">{{ this.time }}</strong>
            <v-layout column justify-end>
              <div class="headline font-weight-light">{{ this.date }}</div>
            </v-layout>
          </v-layout>
        </v-container>
      </v-img>
</template>

<script>
export default {
  data() {
    return {
      date: '',
      time: '',
      avatarIcon: 'https://st3.depositphotos.com/1832477/19518/v/1600/depositphotos_195187320-stock-illustration-hacker-in-black-clothes-and.jpg', 

    }
  },

  methods: {
    async getTime() {
      
      const vm = await axios.get('/getTime') 
      this.date = vm.data.date;
      this.time = vm.data.time;

    }

  }, 
  async created(){ 
    while(true) {
    const vm = await axios.get('/getTime') 
      this.date = vm.data.date;
      this.time = vm.data.time;
      await new Promise(r => setTimeout(r, 60000));
    } 
  }
}
</script>

<style>
  .timeline {
    border-radius: 3px;
    background-clip: border-box;
    box-shadow: 1px 1px 1px 1px rgba(0, 0, 0, 0.21);
    background-color: transparent;
  }
</style>
