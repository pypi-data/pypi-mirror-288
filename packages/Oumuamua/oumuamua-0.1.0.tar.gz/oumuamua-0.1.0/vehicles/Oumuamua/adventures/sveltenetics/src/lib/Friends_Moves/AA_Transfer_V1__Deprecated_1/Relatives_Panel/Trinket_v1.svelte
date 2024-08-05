

<script>


/*
	import AA_Transfer_G1_Relatives_Panel from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Trinket.svelte'
*/

////
///
import { getModalStore } from '@skeletonlabs/skeleton';
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';
import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { onMount, onDestroy } from 'svelte';
//
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';
//
//
import UT_Fields from './Leaves/Unsigned_Transaction_Fields/Trinkets.svelte';
import UT_Signature from './Leaves/UT_Signature.svelte';
import UT_Object from './Leaves/UT_Object.svelte';
import ST_Barcode from './Leaves/ST_Barcode.svelte';
//\
//\\

////
//
//	props
//
//
export let choices;
const { modal_store } = choices;
//
//\\

////
///
//	nested component props
//
let barcode_found = "no"
//
let unsigned_tx = ""
let unsigned_tx_stringified = ""
let unsigned_tx_hexadecimal_string = ""
//
let signed_tx_hexadecimal_string = ""
let signed_transaction_fiberized = ""
//\
//\\

////
//
//	nested component actions
//
const unsigned_transaction_scanned = ({ 
	unsigned_tx_hexadecimal_string: _unsigned_tx_hexadecimal_string,
	unsigned_tx_stringified: _unsigned_tx_stringified,
	unsigned_tx: _unsigned_tx
}) => {
	console.log (
		"Picture and Sign Modal: unsigned_transaction_scanned", 
		{ unsigned_tx_hexadecimal_string }
	)
	
	barcode_found = "yes"
	unsigned_tx = _unsigned_tx
	unsigned_tx_stringified = _unsigned_tx_stringified
	unsigned_tx_hexadecimal_string = _unsigned_tx_hexadecimal_string
}

const action__signed_transaction_created = ({
	signed_transaction_hexadecimal_string: _signed_transaction_hexadecimal_string,
	signed_transaction_fiberized: _signed_transaction_fiberized
}) => {
	signed_tx_hexadecimal_string = _signed_transaction_hexadecimal_string
	signed_transaction_fiberized = _signed_transaction_fiberized
}
//
//\\


let barcode_element = ""
let current_tab = 1;


onMount (async () => {});

const close_the_modal = () => {
	modal_store.close ();
}

const open_tab_1 = () => {
	current_tab = 1;
}
const open_tab_2 = () => {
	current_tab = 2;
}
const open_tab_3 = () => {
	current_tab = 3;
}
const open_tab_4 = () => {
	current_tab = 4;
}

</script>

{#if $modal_store [0] }
<div 
	style="
		position: relative;
		top: 0;
		left: 0;
		padding: 0;
		width: 100vw;
		height: calc(100vh - 36px);
		
		overflow: hidden;
	"
>
	<div
		style="
			display: flex;
			
			position: absolute;
			top: 10px;
			left: 10px;
			height: calc(100% - 20px);
			width: calc(100% - 20px);
			border-radius: 8px;
			
			overflow: hidden;
			
			flex-direction: column;
		"
	>
		<div
			style="
				
				position: absolute;
				top: 0;
				left: 0;
				right: 0;
				bottom: 0;
				width: 100%;
				
				box-sizing: border-box;
				padding: 0 10px 0;
				
				overflow: scroll;
			"
		>
			<div style="height: 2cm" />			
			{#if current_tab === 1}
				<UT_Fields
					barcode_found={ barcode_found }
					unsigned_transaction_scanned={ unsigned_transaction_scanned }
					unsigned_transaction_hexadecimal_string={ unsigned_tx_hexadecimal_string }
				/>
			{:else if current_tab === 2}
				<UT_Object 
					unsigned_tx_stringified={ unsigned_tx_stringified }
					unsigned_tx_hexadecimal_string={ unsigned_tx_hexadecimal_string }
				/>
			{:else if current_tab === 3}
				<UT_Signature 
					unsigned_tx={ unsigned_tx }
					unsigned_tx_hexadecimal_string={ unsigned_tx_hexadecimal_string }
					
					signed_transaction_hexadecimal_string={ signed_tx_hexadecimal_string }
					signed_transaction_fiberized={ signed_transaction_fiberized }
					
					action__signed_transaction_created={ action__signed_transaction_created }
				/>
			{:else if current_tab === 4}
				<ST_Barcode 
					signed_tx_hexadecimal_string={ signed_tx_hexadecimal_string }
				/>
			{/if}
			<div style="height: 5cm" />
		</div>
	
		<div
			style="
			
				position: absolute;
				top: 0;
				left: 0;
				width: 100%;
				height: 100px;
			"
		>
			<div
				style="
					overflow: scroll;
				"
			>
				<TabGroup 
					justify="justify-center"
					active="variant-filled-primary"
					hover="hover:variant-soft-primary"
					flex="flex-1 lg:flex-none"
					rounded=""
					border=""
					class="bg-surface-100-800-token w-full"
				>
					<TabAnchor 
						selected={current_tab === 1}
						on:click="{ open_tab_1 }"
					>
						<span
							health="Signing__UT_Barcode_Camera_button"
						>Unsigned Transaction Fields</span>
					</TabAnchor>
					<TabAnchor 
						selected={current_tab === 2}
						on:click="{ open_tab_2 }"
					>
						<span
							health="Signing__UT_Object_button"
						>Unsigned Transaction</span>
					</TabAnchor>
					<TabAnchor 
						selected={current_tab === 3}
						on:click="{ open_tab_3 }"
					>
						<span
							health="Signing__UT_Signature_button"
						>UT Signature</span>
					</TabAnchor>
					<TabAnchor selected={current_tab === 4}
						on:click="{ open_tab_4 }"
					>
						<span
							health="Signing__ST_Barcode_button"
						>ST Barcode</span>
					</TabAnchor>
				</TabGroup>
			</div>
		</div>
		
		

		<footer class="modal-footer"
			style="
				display: flex;
			
				position: absolute;
				bottom: 0;
				left: 0;
				width: 100%;
				
				height: 70px;
				
				align-items: center;
				justify-content: start;
			"
		>
			<div
				style="
					margin: 0 25px;
				"
			>
				<button class="btn variant-filled" on:click={close_the_modal}>
					Close Modal
				</button>
			</div>
		</footer>
	</div>
</div>
{/if}