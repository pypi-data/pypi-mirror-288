




<script>

import Panel from '$lib/trinkets/panel/trinket.svelte'
import { parse_styles } from '$lib/trinkets/styles/parse'
import Net_Choices_with_Text from '$lib/PTO/Nets/Choices_with_Text/Trinket.svelte'

import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { LightSwitch } from '@skeletonlabs/skeleton';
import * as AptosSDK from "@aptos-labs/ts-sdk";
import { onMount, onDestroy } from 'svelte'

import {
	check_roomies_truck,
	monitor_roomies_truck
} from '$lib/Roomies/Trucks'

import Refresh_Browser_Storage from '$lib/Roomies/Plays/Refresh_Browser_Storage.svelte'

let RT_Prepared = "no"
let RT_Monitor;
let RT_Freight;
onMount (async () => {
	const Truck = check_roomies_truck ()
	RT_Freight = Truck.freight; 
	
	RT_Monitor = monitor_roomies_truck ((_freight) => {
		RT_Freight = _freight;
		
		console.info ({ RT_Freight })
	})
	
	RT_Prepared = "yes"
});

onDestroy (() => {
	RT_Monitor.stop ()
}); 

let net_prepare = () => {
	return {
		net_name: "mainnet"
	}
};
let every_net_enhance = ({
	net_name,
	net_path,
	net_connected,
	chain_id
}) => {
	console.info ('every_net_enhance', {
		net_name,
		net_path,
		chain_id
	})
	
	RT_Freight.net_path = net_path
	RT_Freight.net_name = net_name
	RT_Freight.aptos = new AptosSDK.Aptos (new AptosSDK.AptosConfig ({		
		fullnode: net_path,
		network: AptosSDK.Network.CUSTOM
	}));
};

const trends = {
	panel: {
		position: 'relative',
		display: 'inline-flex',
		'width': '33%', 
		'height': '150px',
		'align-items': 'center',
		'justify-content': 'center'
	},
	anchor: parse_styles ({
		position: 'absolute',
		height: '100%',
		width: '100%',
		
		display: 'flex',
		'align-items': 'center',
		'justify-content': 'center',
		'text-decoration': 'none',
		'text-align': 'center',
		'font-size': '2em'
	})
}

</script>

<style>

@media (max-width: 600px) {
    .latest-block-panel {
		flex-direction: column !important;
	}
}
a {
	line-height: 110%;
}

</style>

<svelte:head>
	<title>Roomies</title>
	<meta name="description" content="Roomies" />
</svelte:head>

{#if RT_Prepared === "yes" }
<div>
	
	<Refresh_Browser_Storage />
	
	<div style="height: 12px"></div>

	<div
		class="card p-4"
		style="
			display: flex;
			align-items: center;
			justify-content: center;
			flex-direction: column;
		"
	>
		<header
			style="
				font-size: 1.2em;
				line-height: 200%;
			"
		>Theme</header>
		<div style="width: 10px"></div>
		<div
			style="
				display: flex;
				align-items: center;
				justify-content: center;
				gap: 8px;
			"
		>
			<div>nocturnal</div>
			<LightSwitch />
			<div>diurnal</div>
		</div>
	</div>
	
	
	<div style="height: 12px"></div>
	
	
	<div
		class="card p-4"
		style="
			display: flex;
			align-items: center;
			justify-content: center;
		"
	>
		<Net_Choices_with_Text 
			prepare={ net_prepare }
			every_enhance={ every_net_enhance }
		/>
	</div>
</div>
{/if}