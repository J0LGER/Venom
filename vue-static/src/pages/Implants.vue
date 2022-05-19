<template>
  <div id="implants">
  
  <v-container fluid grid-list-xl>
  <v-layout row wrap>
  <v-flex d-flex lg12 sm12 xs12>
  
  <v-card class="px-4">
  <v-card-text>
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
    v-model="id"
    :items="ids"
    label="Bind Listener ID" 
    required
    ></v-select>
    <v-select
      v-model="implant"
      :items="implants"
      label="Target OS"
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


  <v-btn
      class="btn"
      color="green"
      @click="copy"
      right
    >
      Copy
    </v-btn>
    <v-btn
      class="btn"
      color="green"
      @click="copy"
      right
    >
      Download
    </v-btn>

<!-- Code area text field !--> 
   <v-container fluid>
   <pre class="prettyprint lang-powershell" v-text="code" v-on:focus="$event.target.select()" ref="clone" >
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
        const res = await axios.get('/api/getListeners/')
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
      this.$refs.clone.focus();
      document.execCommand('copy');
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
.prettyprint {
  border-radius: 10px;  
  background: #2f3640;
  font-family: Menlo, "Bitstream Vera Sans Mono", "DejaVu Sans Mono", Monaco, Consolas, monospace;
  border: 0 !important;
}

.pln {
  color: #e6e9ed;
}

/* Specify class=linenums on a pre to get line numbering */
ol.linenums {
  margin-top: 0;
  margin-bottom: 0;
  color: #656d78;
}

li.L0,
li.L1,
li.L2,
li.L3,
li.L4,
li.L5,
li.L6,
li.L7,
li.L8,
li.L9 {
  padding-left: 1em;
  background-color: #2f3640;
  list-style-type: decimal;
}

@media screen {

  /* string content */

  .str {
    color: #ffce54;
  }

  /* keyword */

  .kwd {
    color: #4fc1e9;
  }

  /* comment */

  .com {
    color: #656d78;
  }

  /* type name */

  .typ {
    color: #4fc1e9;
  }

  /* literal value */

  .lit {
    color: #ac92ec;
  }

  /* punctuation */

  .pun {
    color: #e6e9ed;
  }

  /* lisp open bracket */

  .opn {
    color: #e6e9ed;
  }

  /* lisp close bracket */

  .clo {
    color: #e6e9ed;
  }

  /* markup tag name */

  .tag {
    color: #ed5565;
  }

  /* markup attribute name */

  .atn {
    color: #a0d468;
  }

  /* markup attribute value */

  .atv {
    color: #ffce54;
  }

  /* declaration */

  .dec {
    color: #ac92ec;
  }

  /* variable name */

  .var {
    color: #e6e9ed;
  }

  /* function name */

  .fun {
    color: #e6e9ed;
  }
}
</style>
