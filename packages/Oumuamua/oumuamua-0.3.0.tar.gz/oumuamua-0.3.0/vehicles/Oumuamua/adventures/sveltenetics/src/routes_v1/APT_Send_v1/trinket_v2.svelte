



<script>

import { parse_styles } from '$lib/trinkets/styles/parse.js';

import Panel from '$lib/trinkets/panel/trinket.svelte'
import Button from '$lib/trinkets/button/trinket.svelte'


import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import { BrowserQRCodeSvgWriter } from '@zxing/browser';


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

			
const modalStore = getModalStore ();

let from_address = "5D7F18BECA985D6CADDCC4CFE422CB542039897F9F884EB0EFF4EE46C2299395"
let to_address = "C07144860D0E8D31DF8D574125004C5BB99248AE8897A3B83AF562E0E5A0B34B"
let amount = 100000000

let barcode_element;


//
//	https://github.com/aptos-labs/aptos-ts-sdk/blob/main/examples/typescript-esm/sponsored_transactions/server_signs_and_submit.ts
//
//
const accept_and_sign = async ({
	tx_as_hexadecimal_string,
	account_1
}) => {
	const config = new AptosConfig ({})
	// const config = new AptosConfig({ network: APTOS_NETWORK });
	const aptos = new Aptos ();
	
	const serialized_tx = Uint8Array_from_string (tx_as_hexadecimal_string)
	
	const deserializer = new Deserializer (serialized_tx);
	const transaction = SimpleTransaction.deserialize (deserializer);
	
	console.log ({ transaction })
	
	const signed_tx = aptos.transaction.sign ({ 
		signer: account_1, 
		transaction 
	});
	const signed_tx_bytes = signed_tx.bcsToBytes ();
	const signed_tx_hexadecimal_string = string_from_Uint8Array (signed_tx_bytes)
	
	console.log ({ signed_tx })
	console.log ({ signed_tx_bytes })
	console.log ({ signed_tx_hexadecimal_string })
	
	const deserialized_signed_tx = AccountAuthenticator.deserialize (
		new Deserializer (signed_tx_bytes)
	);
	const deserialized_signed_tx_bytes = deserialized_signed_tx.bcsToBytes ();
	
	
	console.log (
		"equivalent:", 
		signed_tx_hexadecimal_string == string_from_Uint8Array (deserialized_signed_tx_bytes)
	)  
	
	return {
		
	}
}


const move_faucet = async () => {
	const codeWriter = new BrowserQRCodeSvgWriter ()
	// const svgElement = codeWriter.writeToDom ('#result', "asdf", 300, 300)
	

	
	// https://github.com/aptos-labs/aptos-ts-sdk/blob/main/tests/e2e/helper.ts
	const config = new AptosConfig({})
	// const config = new AptosConfig({ network: APTOS_NETWORK });
	const aptos = new Aptos ();
	
	const account_1 = Account.generate ();
	const account_1_address = string_from_Uint8Array (account_1.accountAddress.data)
	let { tx: tx1 } = await send_coins_from_faucet ({
		amount: 100000000,
		address: account_1_address
	})
	console.info ({
		account_1
	})
	
	
	const account_2_address = AccountAddress.from (to_address);
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
	
	console.log ({ transaction_as_bytes })
	const svgElement = codeWriter.writeToDom (barcode_element, tx_as_hexadecimal_string, 300, 300)
	
	accept_and_sign ({
		tx_as_hexadecimal_string,
		
		account_1
	})
	
	
	return;
	
	const senderAuthenticator = aptos.transaction.sign ({ 
		signer: account_1, 
		transaction 
	});
	
	console.log ({ senderAuthenticator })
	
	const committedTransaction = await aptos.transaction.submit.simple ({ 
		transaction, 
		senderAuthenticator 
	});
	
	console.log ({ committedTransaction })
}

const move_faucet_2 = async () => {
	if (from_address.length == 0) {
		modalStore.trigger ({
			type: 'alert',
			title: "A from address wasn't choosen.",
			body: '',
			image: '',
			buttonTextCancel: 'close'
		});
		return;
	}
	if (to_address.length == 0) {
		modalStore.trigger ({
			type: 'alert',
			title: "A from address wasn't choosen.",
			body: '',
			image: '',
			buttonTextCancel: 'close'
		});
		return;
	}
	
	
	
	const aptos = new Aptos ();
	
	// const account_1 = Account.generate ();
	// const account_1_address = string_from_Uint8Array (account_1.accountAddress.data)
	
	// const account_2 = Account.generate ();
	// const account_2_address = string_from_Uint8Array (account_2.accountAddress.data)
	
	
	
	const transaction = await aptos.transaction.build.simple({
		sender: from_address,
		data: {
			function: "0x1::coin::transfer",
			typeArguments: ["0x1::aptos_coin::AptosCoin"],
			functionArguments: [
				to_address, 
				amount
			]
		},
	});
	
	
	console.info ({ transaction })
	
	//console.info (dump (transaction.rawTransaction))
	//console.log (JSON.stringify (transaction.rawTransaction, null, 4))
	//return;
	
	const privateKey = new Ed25519PrivateKey (
		"89ABDEC89ABD8F9EADBCF8E9DABCF8ED9ACB2456701235243615234601234560"
	);
	const accountAddress = AccountAddress.from (from_address);
	
	const account_1 = Account.fromPrivateKeyAndAddress({
		privateKey,
		address: accountAddress
	});
	
	console.log ({ account_1 })
	
	const senderAuthenticator = aptos.transaction.sign ({ 
		signer: account_1, 
		transaction 
	});
	const committedTransaction = await aptos.transaction.submit.simple ({ 
		transaction, 
		senderAuthenticator 
	});
}

</script>

<Panel styles={{ "width": "100%" }}> 
	<header
		style="text-align: center; font-size: 2em"
	>APT Give</header>
	
	<pre><code id="result" bind:this={barcode_element}></code></pre>
	
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
			>Move</button>
		</div>
	</section>
</Panel>