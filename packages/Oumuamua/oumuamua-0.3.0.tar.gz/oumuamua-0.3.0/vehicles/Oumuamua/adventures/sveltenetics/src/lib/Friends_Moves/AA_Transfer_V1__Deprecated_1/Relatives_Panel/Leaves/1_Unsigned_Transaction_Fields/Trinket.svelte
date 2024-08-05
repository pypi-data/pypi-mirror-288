

<script>

///
//
import Barcode_Camera from './Barcode_Camera/Trinket.svelte'
import Hexadecimal_String_Field from './Hexadecimal_String_Field/Trinket.svelte'
//
import { 
	parse_styles 
} from '$lib/trinkets/styles/parse.js';
import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
//
import { getModalStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
import { getToastStore } from '@skeletonlabs/skeleton';	
//
//\


import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Logistics/Truck'
let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	freight.current.land = "Unsigned_Transaction_Fields"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
	})
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});



/*
let action__add_UT_hexadecimal_string = ({
	unsigned_tx,
	unsigned_tx_stringified,
	unsigned_tx_hexadecimal_string
}) => {
	console.log ("action__add_UT_hexadecimal_string")
	
	message = "The unsigned transaction was added."
	
	unsigned_transaction_scanned ({
		unsigned_tx,
		unsigned_tx_stringified,
		unsigned_tx_hexadecimal_string
	})
}
*/


let current_tab = 0;

</script>


{#if prepared === "yes"}
<div unsigned_transaction_fields_leaf>
	<div
		style="
			text-align: center;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: 0 0 0.3cm;
			"
		>Transaction Petition Field</header>
		<p>A QR code picture or a hexadecimal string of the transaction petition can be added here.</p>
	</div>

	<div style="height: 0.5cm" ></div>

	<aside class="alert variant-filled"
		style="
			display: flex;
			flex-direction: row;
			margin: 12px auto;
			max-width: 500px;
		"
	>
		<div>
			{#if freight.Unsigned_Transaction_Fields.hexadecimal_string.length === 0}
			<ConicGradient 
				stops={[
					{ color: 'transparent', start: 0, end: 25 },
					{ color: 'rgb(var(--color-primary-500))', start: 75, end: 100 }
				]} 
				spin
				width="w-5"
			/>
			{/if}
		</div>
		<p
			style="
				margin: 0;
				padding-left: 12px;
			"
		>{ freight.Unsigned_Transaction_Fields.info_text }</p>
	</aside>

	<div style="height: 0.5cm" ></div>

	<TabGroup justify="justify-center">
		<Tab bind:group={current_tab} name="tab1" value={0}>
			<span barcode_camera_button>Barcode Camera</span>
		</Tab>
		<Tab bind:group={current_tab} name="tab2" value={1}>
			<span hexadecimal_field_button>Hexadecimal Field</span>
		</Tab>
		
		<svelte:fragment slot="panel">
			{#if current_tab === 0}
			<Barcode_Camera />
			{:else if current_tab === 1}
			<Hexadecimal_String_Field />
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>
{/if}