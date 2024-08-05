



<script>


import { parse_styles } from '$lib/trinkets/styles/parse.js';
import Panel from '$lib/trinkets/panel/trinket.svelte'
	
import * as AptosSDK from "@aptos-labs/ts-sdk";
import { 
	Account, 
	AccountAddress,
	AccountAuthenticator,
	
	Aptos, 
	AptosConfig, 
	
	Deserializer,
	
	Ed25519PrivateKey,
	Ed25519PublicKey,
	
	generateRawTransaction,
	generateTransactionPayload,
	
	Network,
	
	SimpleTransaction
} from "@aptos-labs/ts-sdk";

import { Modal, getModalStore } from '@skeletonlabs/skeleton';
import { getToastStore } from '@skeletonlabs/skeleton';
// import { ModalComponent, ModalStore } from '@skeletonlabs/skeleton';


import { accept_and_sign } from '$lib/Aptos_Moves/APT_send/accept_and_sign'
import { make_unsigned_tx } from '$lib/Aptos_Moves/APT_send/unsigned_tx_make'
import Signed_tx_Modal from '$lib/Aptos_Moves/APT_send/signed_tx_modal.svelte'
import Layer_APT_Give from '$lib/Aptos_Moves/APT_send/Layer_APT_Give/Trinket.svelte'
		


			
const modal_store = getModalStore ();


let net_path = ""


import { friends_has_stand } from "$lib/stands/friends"
import { onMount, onDestroy } from 'svelte';

let friends_has_stand_monitor;
onMount(() => {
	friends_has_stand_monitor = friends_has_stand.monitor (({ inaugural, field }) => {
		const warehouse = friends_has_stand.warehouse ()
		net_path = warehouse.net.path
	})
});

onDestroy (() => {
	if (friends_has_stand_monitor) {
		friends_has_stand_monitor.stop ()
	}
});


let from_address_hexadecimal_string = "522D906C609A3D23B90F072AD0DC74BF857FB002E211B852CE38AD6761D4C8FD"
let to_address_hexadecimal_string = "26F4F8D7C5526BA7DA453041D3A858CFEA06D911C90C2E40EDA2A7261826858C"
let amount = 10000000;

let barcode_element;

let the_unsigned_transaction = ""

const ask_commit = async () => {
	modal_store.trigger({
		type: 'component',
		component: {
			ref: Signed_tx_Modal,
			props: { 
				the_unsigned_transaction
			}
		}
	});
}

const move_faucet = async () => {
	console.log ('sending from account_1 to account_2')
	
	const { unsigned_transaction } = await make_unsigned_tx ({
		net_path,
		
		from_address_hexadecimal_string,
		to_address_hexadecimal_string,
		amount,
		barcode_element,
		modal_store
	});
	
	modal_store.trigger ({
		type: 'component',
		component: {
			ref: Layer_APT_Give,
			props: { 
				choices: {
					net_path,
					from_address_hexadecimal_string,
					to_address_hexadecimal_string,
					amount,
					barcode_element,
					modal_store
				}
			}
		}
	});
	
	the_unsigned_transaction = unsigned_transaction
}


</script>

<Panel styles={{ "width": "100%" }}> 
	<header
		style="text-align: center; font-size: 2em"
	>APT Give</header>
	
	<p
		style="text-align: center; font-size: 1em"
	>This is for sending APT from one address to another.</p>
	
	<section>		
		<div 
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
			style="height: 40px; background: none; margin-top: 10px"
		>
			<div class="input-group-shim" width="100px">Net</div>
			<input 
				bind:value={ net_path }
				type="text" 
				placeholder="" style="text-indent: 10px" 
			/>
		</div>
		
		<div 
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
			style="height: 40px; background: none; margin-top: 10px"
		>
			<div class="input-group-shim">From Address</div>
			<input 
				bind:value={ from_address_hexadecimal_string }
				type="text" placeholder="" style="text-indent: 10px" 
			/>
		</div>
		
		<div 
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
			style="height: 40px; background: none; margin-top: 10px"
		>
			<div class="input-group-shim" width="100px">To Address</div>
			<input 
				bind:value={ to_address_hexadecimal_string }
				type="text" placeholder="" style="text-indent: 10px" 
			/>
		</div>
		
		<div 
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
			style="height: 40px; background: none; margin-top: 10px"
		>
			<div class="input-group-shim">Amount of Octas</div>
			<input 
				placeholder="" 
				style="text-indent: 10px" 
				type="number" 
				bind:value={ amount }
			/>
		</div>

		<div
			style="{ parse_styles ({
				'display': 'flex',
				'justify-content': 'right'
			})}"
		>
			<button 
				style="margin-top: 10px"
				on:click={ move_faucet }
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			>Make this Transaction</button>
			
			<div style="width: 10px"></div>
			
			<button 
				on:click={ ask_commit }
				style="margin-top: 10px"
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			>Open the Commit Modal</button>
		</div>
		
		<pre><code id="result" bind:this={barcode_element}></code></pre>
	</section>
</Panel>