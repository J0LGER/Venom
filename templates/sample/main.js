var agentsList = Vue.component('agents-list', { 

	props: ['description'], 

	template: `<div>
	<agents v-for:"agent in agents"> {{ description }} </agents>
	</div>`, 


	data() { 

		return { 
			agents: [
			{ description: 'This is agent 1', active: true },
			{ description: 'This is agent 2', active: false },
			{ description: 'This is agent 3', active: true },
			{ description: 'This is agent 4', active: false },
			{ description: 'This is agent 5', active: true } 
			]
		};  
	}

});


var agents = Vue.component('tabs', { 

	template: `
	
	<div>
		<div class="tabs">
		<ul>
		<li class="is-active"><a>About Venom</a></li>
		<li><a>Our Venom</a></li>
		<li><a>Github</a></li>
		<li><a>Donate</a></li>
		</ul>
	</div>
	
		<div class="tabs-details"> 
	
			<slot></slot> 

			</div>
	</div>
 
  `, 


	data() { 

		return { 

			description: 'This is an agent' 


		}; 

	}, 
	mounted() { }

});


var app = new Vue({

	el: '#root',

	data: {

		isLoading: false,
		title: 'This title is shown by Vue.js',
		message: 'Hello from vue.js!',
		names: ['Joe', 'Mary', 'Jane', 'Jack'],
		className: 'color-red',
		listeners: [ 

		{ description: 'Port 8080', active: true  }, 
		{ description: 'Port 9091', active: true  },
		{ description: 'Port 1234', active: false },
		{ description: 'Port 1337', active: true  }

		]
	},

	methods: {

		addNameAndToggle() {

			this.names.push(this.message)
			this.message = '';
			this.isLoading = true;
		}


	},

	computed: { 

	   reversedMessage() { 
	   
		   return this.message.split('').reverse().join('')

	   }, 

	   inactiveListeners() { 

			return this.listeners.filter(listener => !listener.active)

		}	


	}, 
	components: { 

		agentsList: agentsList, 
		agents: agents 

	}, 
	mounted() {

		//alert('ready');
	}

});

//To add a single element into the names, we can 
//app.names.push('NewElement'); 


//Defining Vue Componenets