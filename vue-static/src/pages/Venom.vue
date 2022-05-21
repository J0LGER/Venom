<template>
  <div id="venom">
  
  <v-container fluid grid-list-xl>
  <v-layout row wrap>
  <v-flex d-flex lg12 sm12 xs12>
  
  <v-card class="px-4">
  <v-card-text>
  <v-data-table-header>Alive Agents</v-data-table-header>
  <v-data-table
      :headers="headers"
      :items="agents"
> 
    <template slot="items" slot-scope="myprops">
        <td v-for="header in headers">
        {{ myprops.item[header.value] }}
        </td>
  </v-card> 
  </v-card-text>
 
 </v-container> 
 </v-layout> 
 </v-flex>
  
  <v-container fluid grid-list-xl>
  <v-layout row wrap>
  <v-flex d-flex lg12 sm12 xs12>
  
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
      @click="Venom"
    >
      Venom
    </v-btn>
  </form>
  </v-card> 
  </v-card-text>
 
 </v-container> 
 </v-layout> 
 </v-flex>

  <v-spacer></v-spacer>
  
  <v-container fluid grid-list-xl>
  <v-layout row wrap>
  <v-flex d-flex lg12 sm12 xs12>
  
  <v-card v-if="display" class="px-4">
  <v-card-text>

  <v-shell 
  v-if="id"
  :agentID="id"
  ></v-shell>
     
  </v-card> 
  </v-card-text>
 
  </v-container> 
  </v-layout> 
  </v-flex>
  
  
  </div>
</template>

<script>

export default {
  
  data() {
    return {
        agents: this.getAgents(),
        id: null,
        display: false,
        ids: [],
        headers: [
          {
            text: 'Agent ID',
            align: 'start',
            filterable: false,
            value: 'id',
          },
          { text: 'Connected Listener Port', value: 'port' },
          { text: 'Agent OS', value: 'type' },
        ]
    }
        },
  methods: { 
    async Venom() { 
        if(this.display == false)
        this.display = true;
        else 
        this.display = false;
    }, 
    async getAgents(){ 
        const res = await axios.post('/agents', { 
            status: 'alive'

        })
        .then(function (response) { 
          return response
        })  
        .catch(function (error) { 
          console.log(error); 
        }); 
        for (var i = 0; i < res.data.agents.length; i++) { 
            this.ids.push(res.data.agents[i].id);
        } 
        this.agents = res.data.agents;
        return this.agents
      }
} 
}
</script>

<style >

.btn { 
  float: right; 
  }
  
</style>