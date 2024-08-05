

<script>

/*
import Net_Choices from '$lib/PTO/Nets/Choices.svelte'
<Net_Choices
	net_name={ "devnet" }
	on_change={ on_change }
/>
const on_change = ({ net }) => {
	const net_name = net.name;
	const net_path = net.path;
	
}
*/


import { request_ledger_info } from '$lib/PTO/General/Ledger_Info.API'
import { onMount } from 'svelte'

export let on_change;

const nets = {
	"mainnet": {
		"name": "mainnet",
		"path": "https://api.mainnet.aptoslabs.com/v1"
	},
	"testnet": {
		"name": "testnet",
		"path": "https://api.testnet.aptoslabs.com/v1"
	},
	"devnet": {
		"name": "devnet",
		"path": "https://api.devnet.aptoslabs.com/v1"
	},
	"custom": {
		"name": "custom",
		"path": ""
	}
}

export let net_name = "mainnet"

const net_change = async (value) => {
	console.log ("net_name", net_name)
	
	const net = nets [ net_name ]
	if (net_name === "custom") {
		on_change ({
			net
		});
		return;
	}
	
	const { enhanced } = await request_ledger_info ({ net_path: net.path })
	const { chain_id } = enhanced;
	on_change ({
		net,
		chain_id
	})
}

onMount (() => {
	net_change ("mainnet")
})


</script>

<div style="max-width: 200px">
	<select 
		nets-choices
		
		class="select" 
		bind:value={ net_name }
		on:change={ net_change }
	>
		<option value="mainnet">mainnet</option>
		<option value="devnet">devnet</option>
		<option value="testnet">testnet</option>
		<option value="custom">custom</option>
	</select>
</div>