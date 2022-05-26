<template>
  <v-data-table
    class="table"
    :headers="headers"
    :items="agents"
    :rows-per-page-items="[10, 25]">
    <template slot="items" slot-scope="props">
      <td class="text-xs-left">
        <v-avatar size="42">
          <img :src="randomAvatar()" alt="avatar">
        </v-avatar>
      </td>
      <td class="text-xs-left">{{ props.item.id }}</td>
      <td class="text-xs-left">{{ props.item.ip }}</td>
      <td class="text-xs-left">{{ props.item.port }}</td>
      <td class="text-xs-left">{{ props.item.type }}</td>
    </template>
  </v-data-table>
</template>

<script>
const avatars = [
  'https://st3.depositphotos.com/1007566/12989/v/950/depositphotos_129895474-stock-illustration-hacker-character-avatar-icon.jpg',
  'https://st4.depositphotos.com/5934840/25423/v/1600/depositphotos_254235584-stock-illustration-security-system-technology.jpg',
  'https://st2.depositphotos.com/1432405/11949/v/950/depositphotos_119499226-stock-illustration-hacker-behind-a-computer-icon.jpg',
  'https://st3.depositphotos.com/1832477/19518/v/1600/depositphotos_195187320-stock-illustration-hacker-in-black-clothes-and.jpg',
  'https://st4.depositphotos.com/1832477/27386/v/1600/depositphotos_273866520-stock-illustration-hacker-using-a-laptop-icon.jpg'
];
export default {
   props: { 
        status: String
      },
  data() {
    return {
      agents: [],
      headers: [

          { 
            text: this.status + ' Agents' 
          },
          {
            text: 'Agent ID',
            filterable: false,
            value: 'id',
          },
          { text: 'Agent IP', value: 'ip' },
          { text: 'Connected Listener Port', value: 'port' }, 
          { text: 'Agent OS', value: 'type' },
        ], 
    }
  },
  methods: {
    randomAvatar () {
      return avatars[Math.floor(Math.random() * avatars.length)];
    }
  },
  async created() {
    const vm = this;
    console.log(this.status);
    await vm.axios.post('/agents',{ 
      status: this.status
    })
    .then(response => {
      var result = response && response.data;
      vm.agents = result.agents;
    });
  }
}
</script>

<style>
  .table {
    border-radius: 3px;
    background-clip: border-box;
    border: 1px solid rgba(0, 0, 0, 0.125);
    box-shadow: 1px 1px 1px 1px rgba(0, 0, 0, 0.21);
    background-color: transparent;
  }
</style>