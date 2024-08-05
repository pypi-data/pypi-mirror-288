


<script>

/*
import Choices_with_Text from '$lib/PTO/Nets/Choices_with_Text.svelte'

let net_prepare = () => {
	return {
		net_name: "mainnet"
	}
};

let every_net_enhance = ({
	net_name,
	net_path,
	chain_id
}) => {
	console.info ({
		net_name,
		net_path,
		chain_id
	})
};

<Net_Choices_with_Text 
	prepare={ net_prepare }
	every_enhance={ every_net_enhance }
/>
*/


//
//
import Net_Choices from '$lib/PTO/Nets/Choices.svelte'
import Problem_Alert from '$lib/trinkets/Alerts/Problem.svelte'
import { request_ledger_info } from '$lib/PTO/General/Ledger_Info.API'
//
import { loop } from '$lib/taverns/loop'
//
//
import { has_field } from 'procedures/object/has_field'
import { ConicGradient } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte'
//
//



export let prepare = () => {
	const preparations = {
		net_name: "mainnet"
	}
	
	
	return {
		net_name
	}
};
export let every_enhance = () => {};


let ICANN_addresses = {}


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

$: prepared = "no"

$: net_name = "mainnet"
$: net_path = ""
$: chain_id = ""
$: block_height = ""
$: epoch = ""
$: problem_text = ""
$: custom_address_confirmed = "no"
$: ledger_info_loop_allowed = "no"


let ledger_ask_count = 0;

const clear_info = () => {
	chain_id = "";
	block_height = "";
	epoch = "";
	//
	custom_address_confirmed = "no"
	//
	problem_text = ""
}

//
//	ICANN_net_path
//
//
const on_change = async () => {
	/*
	
	const ask_net_path = net_path;
	try {
		localStorage.setItem ("net_path", net_path)
		localStorage.setItem ("net_name", net_name)
		
		console.log ('on_change ask')		
		
		const { enhanced } = await request_ledger_info ({ net_path })
		const { chain_id: _chain_id } = enhanced;
		if (
			ask_net_path == net_path
		) {
			chain_id = _chain_id;
			block_height = enhanced.block_height;
			epoch = enhanced.epoch;
			
			every_enhance ({
				net_name,
				net_path,
				chain_id,
			})
		}
	}
	catch (exception) {
		console.error (exception)
		if (ask_net_path == net_path) {
			problem_text = exception.message;
		}
	}
	
	*/
}



const the_ledger_ask_loop = loop ({
	wait: 2000,
	wait_for_response: "yes",
	action: async () => {
		const there_is_a_net_path = typeof net_path === "string" && net_path.length >= 1;
		if (there_is_a_net_path !== true) {
			console.info (`There's not a "net path" for the ledger loop.`)
			return;
		}
		
		localStorage.setItem ("net_path", net_path)
		localStorage.setItem ("net_name", net_name)
		
		ledger_ask_count += 1
		const curren_ledger_ask_count = ledger_ask_count;
		
		//console.info ("Asking for the latest stats.", { ledger_ask_count })
		
		const { enhanced } = await request_ledger_info ({ net_path })
		
		//
		//	If the UI changed, after the ask, this filters
		//	the info that was returned from the ask.
		//
		if (ledger_ask_count == curren_ledger_ask_count) {
			console.info ("Modifying the latest stats.")
			
			const { chain_id: _chain_id } = enhanced;
			chain_id = _chain_id;
			block_height = enhanced.block_height;
			epoch = enhanced.epoch;
			
			every_enhance ({
				net_name,
				net_path,
				net_connected: "yes",
				chain_id
			})
		}
	}
})




const on_select_change = async (event) => {
	the_ledger_ask_loop.stop ()
	clear_info ()
	
	net_name = event.target.value;
	let net = nets [ net_name ]
	net_path = net.path;
	custom_address_confirmed = "no"
	
	console.log ({ net })
	
	if (net_name != "custom") {
		on_change ()
	}
	
	the_ledger_ask_loop.play ()
}

const on_textarea_change = async (event) => {
	the_ledger_ask_loop.stop ()
	clear_info ()
	
	net_path = event.target.value;
	// net_name = "custom"
	
	custom_address_confirmed = "no"
	
	the_ledger_ask_loop.play ()
}

const after_confirm_address = () => {
	the_ledger_ask_loop.stop ()
	clear_info ()
	
	
	custom_address_confirmed = "yes"
	the_ledger_ask_loop.play ()
	
	on_change ()
}

const on_change_1 = () => {
	the_ledger_ask_loop.stop ()
	clear_info ()
	
	const preparations = prepare ()
	net_name = preparations.net_name;
	let net = nets [ net_name ]
	net_path = net.path;
	
	if (typeof localStorage.net_name === "string") {
		net_name = localStorage.net_name	
	}
	if (typeof localStorage.net_path === "string") {
		net_path = localStorage.net_path	
	}
	
	console.info ({ 
		net_path,
		net_name
	})
	
	prepared = "yes"
	
	the_ledger_ask_loop.play ()
	
	on_change ()
}



onMount (() => {
	on_change_1 ()
})

onDestroy (() => {
	the_ledger_ask_loop.stop ()
})

</script>

{#if prepared === "yes"}
<div
	net_group_choices
	style="
		width: 100%;
	"
>
	<header style="text-align: center; font-size: 1.2em; padding: 10px 0">Group</header>
	<div style="padding: 0 0 0.5cm">
		<p
			style="text-align: center; font-size: 1em"
		>This is for net that the dapp connects to.</p>
		<div style="height: 12px"></div>
		<p
			style="text-align: center; font-size: 1em"
		>The consensus is currently based on the responses from one address.</p>
		<p
			style="text-align: center; font-size: 1em"
		>Asking for responses from multiple addresses is on the agenda.</p>
	</div>
	<select 
		nets-choices
		
		class="select" 
		bind:value={ net_name }
		on:change={ on_select_change }
	>
		<option value="mainnet">mainnet</option>
		<option value="devnet">devnet</option>
		<option value="testnet">testnet</option>
		<option value="custom">custom</option>
	</select>
	<div style="height: 6px"></div>
	
	{#if net_name === "custom" }
	
	<div
		custom_net_path_region
		style="
			display: grid;
			grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
			gap: 4px;
		"
	>
		<div>
			<div 
				style="
					display: flex;
					align-items: center;
					justify-content: center;
					
					opacity: { custom_address_confirmed === "yes" ? 1 : 0}
				"
			>
				<ConicGradient 
					stops={[
						{ color: 'transparent', start: 0, end: 25 },
						{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
					]} 
					spin width="w-6"
				/>
			</div>
		
			<div class="card p-2"
				style="
					display: flex;
					align-items: center;
				"
			>
				<span icann_net_address>Net Path</span>
			</div>
		</div>

		<textarea 
			icann_net_address
			
			on:keyup={ on_textarea_change }
			bind:value={ net_path }
			
			style="
				flex: 1 1 200px;
				padding: 5px 10px
			"
			
			class="textarea"
			type="text" 
			placeholder=""
			
			rows="1"
		/>
		
		<button 
			type="button" 
			class="btn variant-filled"
			on:click={ after_confirm_address }
			disabled={ custom_address_confirmed === "yes" }
		>Confirm Address</button>
	</div>
	{:else}
	<div
		style="
			display: flex;
			gap: 5px;
			width: 100%;
		"
	>
		<div 
			style="
				display: flex;
				align-items: center;
				justify-content: center;
			"
		>
			<ConicGradient 
				stops={[
					{ color: 'transparent', start: 0, end: 25 },
					{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
				]} 
				spin width="w-6"
			/>
		</div>
		<div class="card p-2"
			style="
			
			"
		>
			<span>ICANN Address</span>
		</div>
		<div class="card p-2"
			style="
				flex: 1 1 200px;
			"
		>
			<span icann_net_address>{ net_path }</span>
		</div>
	</div>
	{/if}
	
	{#if typeof chain_id === "number"}
	<div
		style="
			display: grid;
			grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
			gap: 4px;
			width: 100%;
			margin: 4px 0;
		"
	>
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.2em;
			"
		>
			<span>Chain ID</span>
			<span class="badge variant-filled-surface">{ chain_id }</span>
		</span>
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.1em;
			"
		>
			<span>Epoch</span>
			<span class="badge variant-filled-surface">{ epoch }</span>
		</span>
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.1em;
			"
		>
			<span>Block Height</span>
			<span class="badge variant-filled-surface">{ block_height }</span>
		</span>
	</div>
	{/if}
	
	{#if problem_text.length >= 1}
	<Problem_Alert 
		text={ problem_text }
	/>
	{/if}
</div>
{/if}