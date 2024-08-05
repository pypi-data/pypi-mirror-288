
// import { make_unsigned_tx } from '$lib/Aptos_Moves/APT_send/unsigned_tx_make'

// var now = new AptosSDK.U64 (Math.floor (Date.now () / 1000))
// var exp = new AptosSDK.U64 (Math.floor (Date.now () / 1000) + 600)

///
//
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
	
	SimpleTransaction,
	
	U64
} from "@aptos-labs/ts-sdk";

import * as AptosSDK from "@aptos-labs/ts-sdk";



							
			

////
///
//
import { make_picture } from '$lib/Aptos_Moves/APT_send/picture_make'
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
//\
//\\



export const make_unsigned_transaction = async ({
	net_path,
	
	from_address_hexadecimal_string,
	to_address_hexadecimal_string,
	amount,
	
	barcode_element,
	modal_store
}) => {
	console.log ('make_unsigned_tx', {
		from_address_hexadecimal_string,
		to_address_hexadecimal_string,
		amount
	})
	
	/*///////////////////////////////////////////////
	let from_private_key_hexadecimal_string = "221E8A39C27416F29FD1C58C1CC1C206DE07FCC8BDA2F9678C792CBC3D1CD82D"
	const account_1 = AptosSDK.Account.fromPrivateKey ({ 
		privateKey: new AptosSDK.Ed25519PrivateKey (
			Uint8Array_from_string (from_private_key_hexadecimal_string)
		), 
		legacy: false 
	});
	const from_address = account_1.accountAddress;
	// console.log (string_from_Uint8Array (from_address.data))
	// 70133EFDD60CF5E0C4506CA928221564BB05DC31D5943BF6633BC0B269504B6D
	///////////////////////////////////////////////*/
	
	
	// const config = new AptosConfig ({ network: APTOS_NETWORK });
	const config = new AptosConfig ({
		nodeUrl: net_path
	})
	const aptos = new Aptos (config);
	
	const from_address = AccountAddress.from (Uint8Array_from_string (from_address_hexadecimal_string));
	const to_address = AccountAddress.from (Uint8Array_from_string (to_address_hexadecimal_string));
	
	console.log ({
		from_address,
		to_address
	})


	// wait this long in seconds
	const duration = 600;
	const expireTimestamp = new U64 (Math.floor (Date.now () / 1000) + duration).value;
	
	console.log ("exp:", expireTimestamp)
	console.log ("now:", Math.floor (Date.now () / 1000))
	
	// https://github.com/aptos-labs/aptos-ts-sdk/blob/cb7e8bb8c6242eca6d488bb361bdd483dc1a421d/examples/typescript-esm/transaction_with_predefined_abi.ts#L199
	// https://github.com/aptos-labs/aptos-ts-sdk/blob/cb7e8bb8c6242eca6d488bb361bdd483dc1a421d/src/transactions/instances/rawTransaction.ts#L46
	const unsigned_tx = await aptos.transaction.build.simple ({
		sender: from_address,
		data: {
			function: "0x1::coin::transfer",
			typeArguments: ["0x1::aptos_coin::AptosCoin"],
			functionArguments: [
				to_address,
				amount
			]
		},
		options: {
			expireTimestamp,
			// maxGasAmount: BigInt (300000) 
		}
	});
	const unsigned_tx_as_bytes = unsigned_tx.bcsToBytes ()
	const unsigned_tx_as_hexadecimal_string = string_from_Uint8Array (unsigned_tx_as_bytes)
	
	console.log ("exp", unsigned_tx.rawTransaction.expiration_timestamp_secs)
	
	// const rawTransaction = unsigned_transaction.rawTransaction;
	
	/*///////////////////////////////////////////////
	const transaction_signature_Aptos_object = aptos.transaction.sign ({ 
		signer: account_1, 
		transaction: unsigned_tx
	});	
	console.log ({
		unsigned_tx,
		transaction_signature_Aptos_object
	})
	const committed_transaction = await aptos.transaction.submit.simple ({ 
		transaction: unsigned_tx, 
		senderAuthenticator: transaction_signature_Aptos_object
	});
	console.log ({ committed_transaction })
	return;
	////////////////////////////////////////////////*/
	
	console.info ({ unsigned_tx, unsigned_tx_as_hexadecimal_string })
	
	/*make_picture ({
		barcode_element,
		hexadecimal_string: unsigned_tx_as_hexadecimal_string,
		size: 500
	})*/
	
	return {
		unsigned_tx,
		unsigned_tx_as_hexadecimal_string
	}
}