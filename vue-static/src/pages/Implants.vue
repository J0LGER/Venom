<template>
  <div id="implants">
  
  <v-container fluid grid-list-xl>
  <v-layout row wrap>
  <v-flex d-flex lg12 sm12 xs12>
  
  <v-card class="px-4">
  <v-card-text>
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
      v-model="implant"
      :items="implants"
      label="Target OS"
      required
    ></v-select>
    <v-select 
    v-model="id"
    :items="ids"
    label="Bind Listener ID" 
    required
    ></v-select>
    <v-btn
      class="mr-4"
      color="green"
      @click="generateImplant"
    >
      Generate
    </v-btn>
  </form>
  </v-card> 
  </v-card-text>
 
 </v-container> 
 </v-layout> 
 </v-flex>

 <v-container>
  <v-alert v-if="alertCopy" type="success" value="true" width="20%" shaped dense dismissible>Implant copied into clipboard!</v-alert>
</v-container>

  <v-container>
  <v-btn
      v-if="disabled"
      class="btn"
      color="green"
      @click="copy"
      right
    >
      Copy
    </v-btn>
    <v-btn
      v-if="disabled"
      class="btn"
      color="green"
      @click="copy"
      right
    >
      Download
    </v-btn>
    </v-container> 

<!-- Code area text field !--> 
   <v-container fluid>
   <pre v-if="disabled" class="prettyprint" v-text="code" v-on:focus="$event.target.select()" ref="clone">
   </pre>
   </v-container>


  </div>
</template>

<script>

export default {
  data() {
    return {
        code: null, 
        implantCode: null,
        implant: null,
        implants: ['Windows', 'Linux'], 
        ListenerId: null, 
        disabled: false, 
        alertCopy: false,
        listeners: this.getListeners(),
        id: null,
        ids: [],
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
    async generateImplant() { 
      this.disabled = true;
      const res = await axios.post('/implant',{ 
        type: this.implant, 
        id: this.id
      }).then(function (response) {
        return response
      })
      .catch(function (error) {
        return error
      });
      
      if(res.status == 200){   
      this.code = res.data;
      }
      else{ 
      this.code = 'Unexpected error!';  
      } 
    }, 
    async getListeners(){ 
        const res = await axios.get('/listeners')
        .then(function (response) { 
          return response
        })  
        .catch(function (error) { 
          console.log(error); 
        }); 
        //console.log(res.data.listeners);
        for (var i = 0; i < res.data.listeners.length; i++) { 
            this.ids.push(res.data.listeners[i].id);
        } 
        this.listeners = res.data.listeners;
        return this.listeners
      }, 
    copy() {
      var dummy = document.createElement("textarea");
      document.body.appendChild(dummy);
      dummy.value = this.code;
      dummy.select();
      document.execCommand("copy");
      document.body.removeChild(dummy);
      this.alertCopy = true;
    }
} 
} 
</script>

<style >
/*! Color themes for Google Code Prettify | MIT License | github.com/jmblog/color-themes-for-google-code-prettify */
/*! Color themes for Google Code Prettify | MIT License | github.com/jmblog/color-themes-for-google-code-prettify */
.btn { 
  float: right;

}
</style>
