




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


////
///
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
//
import * as AptosSDK from "@aptos-labs/ts-sdk";
//\
//\\


export async function custom_client (requestOptions) {
	const { params, method, url, headers, body } = requestOptions;
	
	function params_to_query_string (params) {
		const params_array = [];
		for (let key in params) {
			if (params [key] === undefined) {
				continue;
			}
			
			params_array.push (
				encodeURIComponent (key) + '=' + encodeURIComponent (params [key])
			)
		}
		return params_array.join ('&');
	}
	
	const request = {
		headers: {
			...headers,
			customClient: true,
		},
		body: JSON.stringify (body),
		method
	};

	let path = url;
	console.info ({ path, params })
	
	const params_string = params_to_query_string (params);
	if (params) {
		path = `${ url }?${ params_string }`;
	}
	
	console.log ({ path, request })

	const response = await fetch (path, request);
	const data = await response.json ();
	return {
		status: response.status,
		statusText: response.statusText,
		data,
		headers: response.headers,
		config: response,
		request,
	};
}

////
//
//	https://github.com/aptos-labs/aptos-ts-sdk/blob/main/examples/typescript-esm/sponsored_transactions/server_signs_and_submit.ts
//
//
export const sign = async ({
	unsigned_tx_hexadecimal_string,	
	private_key_hexadecimal_string,
	net_path
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
	
	
	// const net_path = "https://api.devnet.aptoslabs.com/v1"
	
	// const config = new AptosSDK.AptosConfig ({})
	// const config = new AptosConfig ({ network: APTOS_NETWORK });
	// const aptos = new AptosSDK.Aptos ();
	
	const aptos = new AptosSDK.Aptos (new AptosSDK.AptosConfig ({
		fullnode: net_path,
		network: AptosSDK.Network.CUSTOM
		
		// network: AptosSDK.Network.MAINNET,
		// client: { provider: custom_client }
	}));
	const config = new AptosSDK.AptosConfig ({		
		fullnode: net_path,
		network: AptosSDK.Network.CUSTOM
	})
	
	console.info ({ aptos })
	
	
	
	
	
	///
	//
	const signed_transaction = aptos.transaction.sign ({ 
		signer: account_1, 
		transaction: unsigned_transaction_Aptos_object
	});
	const signed_transaction_bytes = signed_transaction.bcsToBytes ();
	const signed_transaction_hexadecimal_string = string_from_Uint8Array (signed_transaction_bytes)

	
	/*
	const deserialized_signed_tx = AccountAuthenticator.deserialize (
		new Deserializer (
			Uint8Array_from_string (signed_tx_hexadecimal_string)
		)
	);
	const deserialized_signed_tx_bytes = deserialized_signed_tx.bcsToBytes ();
	console.log (
		"equivalent:", 
		signed_tx_hexadecimal_string == string_from_Uint8Array (deserialized_signed_tx_bytes)
	)  
	*/
	
	
	return {
		signed_transaction,
		signed_transaction_hexadecimal_string
	}
}