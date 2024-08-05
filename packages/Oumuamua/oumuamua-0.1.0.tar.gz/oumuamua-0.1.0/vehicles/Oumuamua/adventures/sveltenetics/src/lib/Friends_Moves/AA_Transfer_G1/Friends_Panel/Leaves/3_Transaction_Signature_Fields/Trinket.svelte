

<script>

///
//
import { getModalStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
import * as AptosSDK from "@aptos-labs/ts-sdk";
//
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
import Barcode_Camera from './Barcode_Camera.svelte'
import Hexadecimal_String_Field from './Hexadecimal.svelte'
//\



import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck 
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	freight.current.land = "Transaction_Signature_Fields"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		console.log ("Transaction Signature Fields: Truck_Monitor", { _freight })
		freight = _freight;
		
	})
	
	prepared = "yes"
});
onDestroy (() => {
	Truck_Monitor.stop ()
});

/*
let transaction_signature_found = "no"
let transaction_signature_alert = "waiting for a transaction signature"
onMount (() => {
	if (transaction_signature_hexadecimal_string.length >= 1) {
		transaction_signature_found = "yes"
		transaction_signature_alert = "The signature was built."
	}
})

const action__add_siganture = async ({
	transaction_signature_Aptos_object,
	transaction_signature_hexadecimal_string
}) => {
	transaction_signature_found = "yes"
	transaction_signature_alert = "The signature was built."
	
	await action__signed_move_built ({
		transaction_signature_Aptos_object,
		transaction_signature_hexadecimal_string
	})
}
*/

let current_tab = 0;

</script>

{#if prepared === "yes"}
<div transaction_signature_fields>
	<div
		style="
			text-align: center;
			padding: 0cm 0;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: .5cm 0;
			"
		>Transaction Signature Field</header>
		<div style="height: 0px"></div>
		<p>
			<span>After recording a picture of the signed transaction barcode,</span> 
			<span>an ask can be sent to the consensus for addition to the blockchain.</span>
		</p>
	</div>
	
	<div style="height: 0.5cm" ></div>
	
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
			{#if freight.transaction_signature.verified != "yes" }
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
		>{ freight.transaction_signature.info_text }</p>
	</aside>

	<div style="height: 0.5cm" ></div>

	<TabGroup justify="justify-center">
		<Tab bind:group={current_tab} name="tab1" value={0}>
			<span barcode_camera_button>Barcode Camera</span>
		</Tab>
		<Tab bind:group={current_tab} name="tab2" value={1}>
			<span hexadecimal_button>Hexadecimal</span>
		</Tab>
		<!-- Tab Panels --->
		<svelte:fragment slot="panel">
			{#if current_tab === 0}
				<Barcode_Camera />
			{:else if current_tab === 1}
				<Hexadecimal_String_Field />
			{/if}
		</svelte:fragment>
	</TabGroup>
		
	
	<div style="height: 200px"></div>
</div>
{/if}