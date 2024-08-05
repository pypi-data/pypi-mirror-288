



<script>

import { parse_styles } from '$lib/trinkets/styles/parse.js';

import Panel from '$lib/trinkets/panel/trinket.svelte'
import Button from '$lib/trinkets/button/trinket.svelte'


import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import { make_picture } from '$lib/Aptos_Moves/APT_send/picture_make'
	
	
import * as AptosSDK from "@aptos-labs/ts-sdk";
console.log ({ AptosSDK })


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
import { send_coins_from_faucet } from '$lib/aptos_API/faucet'

import { Modal, getModalStore } from '@skeletonlabs/skeleton';
// import { ModalComponent, ModalStore } from '@skeletonlabs/skeleton';
import { dump } from 'js-yaml';

import { accept_and_sign } from '$lib/Aptos_Moves/APT_send/accept_and_sign'

import { getToastStore } from '@skeletonlabs/skeleton';

import { example } from './screenplays/example'

			
const modalStore = getModalStore ();

let from_public_key = "5D7F18BECA985D6CADDCC4CFE422CB542039897F9F884EB0EFF4EE46C2299395"
let from_private_key = "89ABDEC89ABD8F9EADBCF8E9DABCF8ED9ACB2456701235243615234601234560"
let from_address = AccountAddress.from (from_public_key);

console.log ({ from_address })

let to_public_key = "C07144860D0E8D31DF8D574125004C5BB99248AE8897A3B83AF562E0E5A0B34B"
let to_address = AccountAddress.from (to_public_key);

let amount = 100000000
let barcode_element;


const move_faucet = async () => {
	console.log ('sending from account_1 to account_2')
	
	// const toastStore = getToastStore();
	// toastStore.trigger({ message: '' });
	

	//example ()
	
	// https://github.com/aptos-labs/aptos-ts-sdk/blob/main/tests/e2e/helper.ts
	const config = new AptosConfig ({})
	// const config = new AptosConfig({ network: APTOS_NETWORK });
	const aptos = new Aptos ();
	
	
	const account_1 = Account.fromPrivateKey ({ 
		privateKey: new Ed25519PrivateKey (
			Uint8Array_from_string (from_private_key)
		), 
		legacy: false 
	});
	const account_1_address = string_from_Uint8Array (account_1.accountAddress.data)
	console.log ({ account_1_address, account_1 })
	let { tx: tx1 } = await send_coins_from_faucet ({
		amount: 100000000,
		address: account_1_address
	})
	
	
	
	/*
	const account_1 = Account.generate ();
	const account_1_address = string_from_Uint8Array (account_1.accountAddress.data)
	let { tx: tx1 } = await send_coins_from_faucet ({
		amount: 100000000,
		address: account_1_address
	})
	console.info ({
		account_1
	})
	*/
	
	const account_2_address = AccountAddress.from (to_public_key);
	console.info ({ account_2_address })
	
	
	//
	//	https://github.com/aptos-labs/aptos-ts-sdk/blob/main/examples/typescript-esm/sponsored_transactions/server_signs_and_submit.ts
	//
	//
	const transaction = await aptos.transaction.build.simple ({
		sender: account_1.accountAddress,
		data: {
			function: "0x1::coin::transfer",
			typeArguments: ["0x1::aptos_coin::AptosCoin"],
			functionArguments: [
				account_2_address,
				
				50000000
			]
		},
	});
	const rawTransaction = transaction.rawTransaction;
	const transaction_as_bytes = transaction.bcsToBytes ()
	const tx_as_hexadecimal_string = string_from_Uint8Array (transaction_as_bytes)
	
	make_picture ({
		barcode_element,
		tx_as_hexadecimal_string,
		size: 500
	})
	
	const { signed_tx_hexadecimal_string } = await accept_and_sign ({
		unsigned_tx_hexadecimal_string: tx_as_hexadecimal_string,
		private_key_hexadecimal_string: from_private_key
	})
	console.info ({ signed_tx_hexadecimal_string })
	
	const deserialized_signed_tx = AccountAuthenticator.deserialize (
		new Deserializer (
			Uint8Array_from_string (signed_tx_hexadecimal_string)
		)
	);
	// const deserialized_signed_tx_bytes = deserialized_signed_tx.bcsToBytes ();
	console.info ({ deserialized_signed_tx })
	
	const committedTransaction = await aptos.transaction.submit.simple ({ 
		transaction, 
		senderAuthenticator: deserialized_signed_tx
	});
	
	console.log ('sent tx', { committedTransaction })
	
	await aptos.waitForTransaction({ transactionHash: committedTransaction.hash });
	console.log(`Committed transaction: ${committedTransaction.hash}`);
	
	/*
	modalStore.trigger ({
		type: 'component',
		component: { 
			ref: MyCustomComponent 
		}
	});
	*/
	
	return;
	
	//const senderAuthenticator = aptos.transaction.sign ({ 
	//	signer: account_1, 
	//	transaction 
	//});
	
	//console.log ({ senderAuthenticator })

}


</script>

<Panel styles={{ "width": "100%" }}> 
	<header
		style="text-align: center; font-size: 2em"
	>APT Give</header>
	
	<section>		
		<div 
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
			style="height: 40px; background: none; margin-top: 10px"
		>
			<div class="input-group-shim">From Address</div>
			<input 
				bind:value={ from_address }
				type="text" placeholder="" style="text-indent: 10px" 
			/>
		</div>
		
		<div 
			class="input-group input-group-divider grid-cols-[auto_1fr_auto]"
			style="height: 40px; background: none; margin-top: 10px"
		>
			<div class="input-group-shim" width="100px">To Address</div>
			<input 
				bind:value={ to_address }
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
			>Generate Unsigned Move</button>
			
			<div style="width: 10px"></div>
			
			<button 
				style="margin-top: 10px"
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
			>Record the Signed Move</button>
		</div>
		
		<pre><code id="result" bind:this={barcode_element}></code></pre>
	</section>
</Panel>