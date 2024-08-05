

<script>

///
//
import { getModalStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
import { Html5QrcodeScanner, Html5QrcodeScanType, Html5Qrcode } from "html5-qrcode";
import { getToastStore } from '@skeletonlabs/skeleton';			

import Barcode_Camera from './Barcode_Camera.svelte'
import Hexadecimal_String_Field from './Hexadecimal_String_Field.svelte'

//
import { 
	parse_styles 
} from '$lib/trinkets/styles/parse.js';
import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
//
//\

////
///
export let unsigned_transaction_hexadecimal_string;
export let barcode_found;
//
export let unsigned_transaction_scanned;
//\
//\\

const toastStore = getToastStore();


let message = "Waiting for unsigned transaction."
if (barcode_found === "yes") {
	message = "The unsigned transaction was added."
}

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

let current_tab = 0;

</script>


<div>
	<div
		style="
			text-align: center;
			padding: 0 0 1cm;
		"
	>
		<header
			style="
				text-align: center;
				font-size: 2em;
				padding: 1cm 0;
			"
		>Unsigned Transaction Fields</header>
		<p>A picture of the unsigned transaction can be recorded here.</p>
		
		<div style="height: 8px"></div>
		<p>After making the picture, an ask can be sent to the consensus for addition to the blockchain.</p>
	</div>
	
	<aside class="alert variant-filled"
		style="
			display: flex;
			flex-direction: row;
			margin: 12px auto;
			max-width: 500px;
		"
	>
		<div>
			{#if barcode_found !== "yes"}
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
		>{message}</p>
	</aside>
	
	<TabGroup>
		<Tab bind:group={current_tab} name="tab1" value={0}>
			<span>Barcode Camera</span>
		</Tab>
		<Tab bind:group={current_tab} name="tab2" value={1}>
			<span>Hexadecimal Field</span>
		</Tab>
		
		
		<svelte:fragment slot="panel">
			{#if current_tab === 0}
				<Barcode_Camera 
					unsigned_transaction_hexadecimal_string={ unsigned_transaction_hexadecimal_string }
					action__add_UT_hexadecimal_string={ action__add_UT_hexadecimal_string }
				/>
			{:else if current_tab === 1}
				<Hexadecimal_String_Field 
					action__add_UT_hexadecimal_string={ action__add_UT_hexadecimal_string }
				/>
			{/if}
		</svelte:fragment>
	</TabGroup>
</div>