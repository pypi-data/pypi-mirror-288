

<script>


/*
	@ Present
		@ Current
		@ Latest
		@ Freshest
*/

import Panel from '$lib/trinkets/panel/trinket.svelte'

import { onMount, onDestroy } from 'svelte'
import { ConicGradient } from '@skeletonlabs/skeleton';

import { parse_styles } from '$lib/trinkets/styles/parse.js';
import { ask_latest_block_number } from '$lib/PTO/Blocks/Latest'
import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
	

import {
	check_roomies_truck,
	monitor_roomies_truck
} from '$lib/Roomies/Trucks'

let RT_Prepared = "no"
let RT_Monitor;
$: RT_Freight = ""

let plays = {
	epoch: "",
	block_height: ""
}

$: got_consensus_info = "no"
const block_height_number = async () => {
	if (running !== "yes") {
		return;
	}
	
	const { 
		enhanced
	} = await ask_latest_block_number ({
		net_path: RT_Freight.net_path
	})
	plays = enhanced
	
	got_consensus_info = "yes"
	
	await new Promise ((resolve) => {
		setTimeout (() => {
			resolve ()
		}, 2000)
	})
	
	block_height_number ()
}

let latest = ""
let running = "no"
onMount (() => {
	const Truck = check_roomies_truck ()
	RT_Freight = Truck.freight; 
	
	RT_Monitor = monitor_roomies_truck ((_freight) => {
		RT_Freight = _freight;
	})
	
	RT_Prepared = "yes"
	running = "yes"
	block_height_number ()
})
onDestroy (() => {
	console.log ("on destroy")
	RT_Monitor.stop ()
	running = "no"
})

const conicStops = [
	{ color: 'transparent', start: 0, end: 25 },
	{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
];

</script>

<style>

@media (max-width: 600px) {
    #latest-block-panel {
		flex-direction: column !important;
	}
}

</style>

{#if RT_Prepared === "yes" }
<Panel 
	styles={{ 
		"width": "100%",
		"min-height": "100px"
	}}
> 
	<header style="{parse_styles ({
		position: 'relative',
		padding: '.3cm',
		'font-size': '2em',
		'text-align': 'center',
		display: 'flex',
		'justify-content': 'space-around',
		'align-items': 'center',
		width: '100%'
	})}">
		<div
			style="
				position: absolute;
				top: 10px;
				left: 10px;
			"
		>
			<ConicGradient epoch
				stops={[
					{ color: 'transparent', start: 0, end: 25 },
					{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
				]} 
				spin
				width="w-5"
			/>
		</div>
		
		<div style="width: 10px"></div>
		<span>Stats</span>
		<div style="width: 10px"></div>
	</header> 
	
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
				
				display: flex;
				justify-content: center;
				flex-wrap: wrap;
				
				//display: grid;
				//grid-template-columns: repeat(2, 1fr);
				//align-items: center;
			"
		>
			<span>Ledger Time</span>
			{#if got_consensus_info === "yes" }
			<span class="badge variant-filled-surface">{ 
				new Date (plays.ledger_timestamp / 1000).toUTCString () 
			}</span>
			{/if}
		</span>
		
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.2em;
				
				display: flex;
				justify-content: center;
				flex-wrap: wrap;
			"
		>
			<span>Ledger Version</span>
			{#if got_consensus_info === "yes" }
			<span class="badge variant-filled-surface">{ 
				parse_with_commas (plays.ledger_version)
			}</span>
			{/if}
		</span>
	</div>	
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
				
				display: flex;
				justify-content: center;
				flex-wrap: wrap;
			"
		>
			<span>Chain ID</span>
			{#if got_consensus_info === "yes" }
			<span class="badge variant-filled-surface">{ plays.chain_id }</span>
			{/if}
		</span>
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.1em;
				
				display: flex;
				justify-content: center;
				flex-wrap: wrap;
			"
		>
			<span>Epoch</span>
			{#if got_consensus_info === "yes" }
			<span class="badge variant-filled-surface">{ plays.epoch }</span>
			{/if}
		</span>
		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.1em;
				
				display: flex;
				justify-content: center;
				flex-wrap: wrap;
			"
		>
			<span>Block Height</span>
			{#if got_consensus_info === "yes" }
			<span class="badge variant-filled-surface">{ 
				parse_with_commas (plays.block_height) 
			}</span>
			{/if}
		</span>
	</div>
</Panel>
{/if}