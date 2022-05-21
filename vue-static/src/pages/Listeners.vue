<template>
  <div id="listeners">
  <v-container fluid grid-list-xl>
  <v-layout row wrap>
  <v-flex d-flex lg12 sm12 xs12>
   <v-card class="px-4">
    <v-card-title>
      Listeners
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="listeners"
    > 
    <template slot="items" slot-scope="myprops">
        <td v-for="header in headers">
        {{ myprops.item[header.value] }}
        </td>
      </template>
  </v-data-table>
  </v-card>
  </v-container>
  </v-layout> 
  </v-flex>

  <v-container fluid grid-list-xl>
  <v-layout row wrap>
  <v-flex d-flex lg12 sm12 xs12>
   
    <v-container>
    <v-card class="px-4">
    <v-card-text>
    <v-form>
        <div v-if="msgC"><v-alert :type="typeC" value="true" v-text="msgC" width="20%" shaped dense elevation="24" dismissible></v-alert></div>
        <v-row>
            <v-col class="d-flex" cols="5" align-self="center">
                <v-text-field v-model="port" label="port" :rules="portRules" required></v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col class="d-flex" cols="5" align-self="center">
            <v-spacer></v-spacer>
            </v-col>
        </v-row>    
    </v-form>
    <v-btn rounded x-small width="7%" :disabled="false" color="green" @click="createListener">Create listener</v-btn>
    </v-card-text>
    </v-card> 
    </v-container> 
    
    <!-- Start Listener deletion form !--> 
   <v-container> 
    <v-card class="px-4">
    <v-card-text>
    <v-form>
        <div v-if="msgD"><v-alert :type="typeD" value="true" v-text="msgD" width="20%" shaped dense elevation="24" dismissible></v-alert></div>
        <v-row>
            <v-col class="d-flex" cols="5" align-self="center">
                <v-text-field v-model="id" label="id" required></v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col class="d-flex" cols="5" align-self="center">
            <v-spacer></v-spacer>
            </v-col>
        </v-row>    
    </v-form>
    <v-btn rounded x-small width="7%" :disabled="false" color="red" @click="deleteListener">Delete listener</v-btn>
    </v-card-text>
    </v-card>
    </v-container> 
    
  </div>
  </v-container> 
  </v-layout> 
  </v-flex>
</template>

<script>

export default {
  data() {
    return {
      port: '', 
      id: '',
      portRules: [
      v => !!v || 'Port number is required',
      v => (v && v >= 1 && v <= 65535) || 'Port Number must be in range!',
      ], 
      msgC: null,
      msgD: null, 
      typeC: null,
      typeD: null,
      search: '',
      listeners: this.getListeners(),
        headers: [
          {
            text: 'Listener ID',
            align: 'start',
            filterable: false,
            value: 'id',
          },
          { text: 'Encryption Key', value: 'key' },
          { text: 'Listener Port', value: 'port' },
        ], 
      } 
        },  
  methods: { 
    async createListener() {  
      const result = await axios.post('/listeners',{ 
        action: 'create', 
        port: this.port
      })
      .then(function (response) {
        return response
      })
      .catch(function (error) {
        return error
      });
      this.getListeners();
      if(result.status == 200){ 
      this.typeC = 'success';
      this.msgC = result.data;
      }
      else if (result.status == 206) {
      this.typeC = 'warning';
      this.msgC = result.data;
      }
      else { 
      this.typeC = 'error';
      this.msgC = 'Some unexpected error  occured!';
      }
      //console.log(result.data);
      //console.log(result.error.data);
      //this.$alert(result.data,"Success","success");
     },
     async deleteListener() {  
      const result = await axios.post('/listeners',{ 
        action: 'delete', 
        ListenerId: this.id
      })
      .then(function (response) {
        return response
      })
      .catch(function (error) {
        return error
      });
      this.getListeners();
      if(result.status == 200){ 
      this.typeD = 'success';
      this.msgD = result.data;
      }
      else if (result.status == 206) {
      this.typeD = 'warning';
      this.msgD = result.data;
      }
      else { 
      this.typeD = 'error';
      this.msgD = 'Some unexpected error  occured!';
      }
      //console.log(result.data);
      //console.log(result.error.data);
      //this.$alert(result.data,"Success","success");
     }, 
     async getListeners(){ 
        const res = await axios.get('/listeners')
        .then(function (response) { 
          return response
        })  
        .catch(function (error) { 
          console.log(error); 
        }); 
        console.log(res.data.listeners);
        this.listeners = res.data.listeners;
        return this.listeners
      }  
} 
} 
</script>

<style>
  

</style>