<template>
  <v-container fluid grid-list-xl>
    <v-layout row wrap>
      <!-- Widgets-->
      <v-flex d-flex lg3 sm6 xs12>
        <widget
          icon="computer"
          subTitle="Alive agents"
          color="#48d339"
          :title="activeAgents"
        />
        </v-flex>
        <v-flex d-flex lg3 sm6 xs12>
        <widget
          icon="computer"
          subTitle="Idle agents"
          color="#f81539" 
          :title="idleAgents"
        />
      </v-flex>
      <!-- Widgets Ends -->
      <!-- DataTable&TimeLine Starts -->
      <v-flex d-flex lg8 sm6 xs12> 
      <data-table status="alive"/> </v-flex>
      <v-card class="px-4">
  <v-card-text>
  <form>
    <v-select 
    v-model="id"
    :items="ids"
    label="Agent ID" 
    required
    ></v-select>
    <v-btn
      class="mr-4"
      color="green"
      @click="deleteAgent"
    >
      DELETE AGENT
    </v-btn>
  </form>
  </v-card> 
  </v-card-text>


      <v-flex d-flex lg8 sm6 xs12> <data-table status="dead"/> </v-flex>
      <v-flex d-flex lg4 sm6 xs12> <time-line /> </v-flex>
      <!-- DataTable&TimeLine Ends -->
      <v-flex d-flex lg6 sm6 xs12> <stepper /> </v-flex>
      <v-flex d-flex lg6 sm6 xs12> <user-tree-view /> </v-flex>
    </v-layout>
  </v-container>
</template>

<script>

export default {
    data() {
      return {
        activeAgents: '',
        idleAgents: ''
      }
    }, 
        async mounted() {
          this.activeAgents = await axios.get('/api/getAgentStatusCount/1')
          .then(function (response) {
          return response.data.agents
                                    })
          .catch(function (error) {
          console.log(error);
                                });
        
          this.idleAgents = await axios.get('/api/getAgentStatusCount/2')
          .then(function (response) {
          return response.data.agents
                                    })
          .catch(function (error) {
          console.log(error);
                                });
         } } 

</script>

<style></style>
