


<script>

/*
	requires:
*/

//
// @Invite @Suggest
//
//

////
///
//
// import { ask_commit } from './../Screenplays/ask_consensus_to_commit_transaction' 
//
//
import { ConicGradient } from '@skeletonlabs/skeleton';

import CircleAlert from 'lucide-svelte/icons/circle-alert'

import { ask_consensus_to_add_transaction } from './ask_consensus_to_add_transaction'
import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 

import { onMount, onDestroy } from 'svelte';
//
//\
//\\


import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'

let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	freight.current.land = "Ask_Consensus"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
		console.log ("Transaction Fields: Truck_Monitor", { freight })
	})
	
	prepared = "yes"
});

onDestroy (() => {
	Truck_Monitor.stop ()
});


/*
let waiting_for_transaction_message = ""
let exception_message = ""
let success_message = ""
let transaction_object = ""
*/

let asked = "no"
const ask = () => {
	asked = "yes"
	ask_consensus_to_add_transaction ({ freight })
}




</script>

{#if prepared === "yes" }
<div>
	<div
		style="
			text-align: center;
			padding: 1cm 0 1cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: .2cm 0;
			"
		>The Ask</header>
		<p>With the <b>Transaction</b> and the <b>Signature</b> an ask can be sent to the consensus to attach the transaction to the blockchain.</p>
	</div>

	<div
		style="
			text-align: center;
			padding: 1cm 0 1cm;
		"
	>
		<button 
			send_the_ask
			disabled={ asked === "yes" }
		
			on:click={ ask }
			type="button" 
			class="btn variant-filled-primary"
		>Ask the Consensus to add the Transaction to the Blockchain.</button>
	</div>
	
	{#if freight.ask_consensus.exception_info.length >= 1 }
	<aside 
		class="alert variant-filled-error" 
		style="display: flex; flex-direction: row; margin-bottom: 20px; padding: 25px 20px;"
	>
		<div>
			<CircleAlert />
		</div>
		<p style="margin: 0; padding-left: 10px;">{freight.ask_consensus.exception_info}</p>
	</aside>
	{/if}
	
	{#if freight.ask_consensus.success_info.length >= 1}
	<aside 
		alert_success
	
		class="alert variant-filled" 
		style="display: flex; flex-direction: row; margin: 20px 0; padding: 25px 20px;"
	>
		<p style="margin: 0; padding-left: 10px;">{ freight.ask_consensus.success_info }</p>
	</aside>
	{/if}

	{#if freight.ask_consensus.waiting_info.length >= 1}
	<aside 
		class="alert variant-filled"
		style="
			display: flex;
			flex-direction: row;
			margin: 12px auto;
			max-width: 500px;
		"
	>
		<div>
			<ConicGradient 
				stops={[
					{ color: 'transparent', start: 0, end: 25 },
					{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
				]} 
				spin
				width="w-5"
			/>
		</div>
		<p
			style="
				margin: 0;
				padding-left: 12px;
			"
		>{ freight.ask_consensus.waiting_info }</p>
	</aside>
	{/if}
	
	{#if freight.ask_consensus.transaction_Aptos_object_fiberized.length >= 1}
	<hr class="!border-t-4" style="margin: 5px 0"/>
	<div 
		style="padding: 10px 0 10px;"
	>
		<header
			style="
				text-align: center;
				font-size: 1.4em;
				padding: .2cm 0;
			"
		>The Full Transaction on the Blockchain</header>
		<div
			full_transaction_on_blockchain
		>
			<Code_Wall
				text={ freight.ask_consensus.transaction_Aptos_object_fiberized }
			/>
		</div>
	</div>
	{/if}
	
	
</div>
{/if}