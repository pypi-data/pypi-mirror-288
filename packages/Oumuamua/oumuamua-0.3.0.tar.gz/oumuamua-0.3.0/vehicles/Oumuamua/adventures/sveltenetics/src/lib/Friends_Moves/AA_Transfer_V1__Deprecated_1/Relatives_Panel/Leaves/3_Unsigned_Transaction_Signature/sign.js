




/* 
	import { sign } from '$lib/trinkets/Layer_Picture_and_sign/Screenplays/sign'
	const {
		signed_transaction,
		signed_transaction_hexadecimal_string
	} = await sign ({
		unsigned_tx_hexadecimal_string,
		private_key_hexadecimal_string
	})
*/

/*
	Essentially, this is the full flow:
		[friends] unsigned_tx
		[friends] unsigned_tx_picture
		
		[relatives] scan unsigned_tx_picture
		[relatives] unsigned_tx
		[relatives] signed_tx
		[relatives] signed_tx_picture

		[friends] scan signed_tx_picture
		[friends] signed_tx
		[friends] send signed_tx
*/

/*
<tr>
	<td>
		<span style="font-size: 1.5em;">Net</span>
		<!-- <Net_Choices
			on_change={ on_change }
		/> -->
		<p>This needs to be the same as the 
		<textarea 
			ican_net_address
			
			bind:value={ net_path }
			
			class="textarea"
			style="min-height: 50px; padding: 10px"
			type="text" 
			placeholder=""
		/>
	</td>
</tr>
*/


////
///
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
//
import * as AptosSDK from "@aptos-labs/ts-sdk";
//\
//\\


////
//
//	https://github.com/aptos-labs/aptos-ts-sdk/blob/main/examples/typescript-esm/sponsored_transactions/server_signs_and_submit.ts
//
//
export const sign = async ({
	unsigned_tx_hexadecimal_string,	
	private_key_hexadecimal_string
}) => {
	
	///
	//
	//	This makes the unsigned_tx object from
	//	the unsigned_tx_hexadecimal_string
	//
	const unsigned_transaction_Aptos_object = AptosSDK.SimpleTransaction.deserialize (
		new AptosSDK.Deserializer (
			Uint8Array_from_string (unsigned_tx_hexadecimal_string)
		)
	);
	console.log ({ unsigned_transaction_Aptos_object })
	//\
	
	///
	//	maybe: this makes the account object from the private key hexadecimal
	//
	//
	const account_1 = AptosSDK.Account.fromPrivateKey ({ 
		privateKey: new AptosSDK.Ed25519PrivateKey (
			Uint8Array_from_string (private_key_hexadecimal_string)
		), 
		legacy: false 
	});
	//\
	

	
	const aptos = new AptosSDK.Aptos (new AptosSDK.AptosConfig ({}));
	console.info ({ aptos })
	
	
	
	///
	//
	const signed_transaction = aptos.transaction.sign ({ 
		signer: account_1, 
		transaction: unsigned_transaction_Aptos_object
	});
	const signed_transaction_bytes = signed_transaction.bcsToBytes ();
	const signed_transaction_hexadecimal_string = string_from_Uint8Array (signed_transaction_bytes)

	
	///
	//
	//	Reversal Check
	//
	const deserialized_signed_transaction_bytes = AptosSDK.AccountAuthenticator.deserialize (
		new AptosSDK.Deserializer (
			Uint8Array_from_string (signed_transaction_hexadecimal_string)
		)
	).bcsToBytes ();
	if (signed_transaction_hexadecimal_string != string_from_Uint8Array (deserialized_signed_transaction_bytes)) {
		throw new Error (`
			signed_transaction_hexadecimal_string !=  deserialized_signed_transaction_bytes
			
			signed_transaction_hexadecimal_string is: ${ signed_transaction_hexadecimal_string }
			
			deserialized_signed_transaction_bytes is: ${ deserialized_signed_transaction_bytes } 
		`)		
	}
	//
	//\

	
	
	return {
		signed_transaction,
		signed_transaction_hexadecimal_string
	}
}