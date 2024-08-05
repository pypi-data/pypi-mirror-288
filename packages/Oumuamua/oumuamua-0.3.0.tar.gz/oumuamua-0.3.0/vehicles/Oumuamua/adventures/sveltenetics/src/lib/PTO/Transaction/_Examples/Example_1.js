
// import { make_transaction } from './Screenplays/make_transaction'

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
					
			

//
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
//\

//
//	https://github.com/aptos-labs/aptos-ts-sdk/blob/main/examples/typescript-esm/sponsored_transactions/server_signs_and_submit.ts
//
//

/*
	expiration:
	https://aptos-labs.github.io/ts-sdk-doc/types/Types.SubmitTransactionRequest.html#__type.expiration_timestamp_secs
*/
export const make_transaction = async () => {
	console.log ('make_transaction')
	
	const net_path = "https://api.devnet.aptoslabs.com/v1"
	const amount = "100000"
	
	///////////////////////////////////////////////
	const to_address = AccountAddress.from (Uint8Array_from_string (
		"26F4F8D7C5526BA7DA453041D3A858CFEA06D911C90C2E40EDA2A7261826858C"
	));
	///////////////////////////////////////////////
	let from_private_key_hexadecimal_string = "89ABC8DE9FABDE0716253407612534071562348F9AEDBC8F9EADBC0127653425"
	const account_1 = AptosSDK.Account.fromPrivateKey ({ 
		privateKey: new AptosSDK.Ed25519PrivateKey (
			Uint8Array_from_string (from_private_key_hexadecimal_string)
		), 
		legacy: false 
	});
	const from_address = account_1.accountAddress;
	// console.log (string_from_Uint8Array (from_address.data))
	// 70133EFDD60CF5E0C4506CA928221564BB05DC31D5943BF6633BC0B269504B6D
	///////////////////////////////////////////////
	
	const aptos = new AptosSDK.Aptos (new AptosSDK.AptosConfig ({
		nodeUrl: net_path
	}));

	
	console.log ({
		from_address,
		to_address
	})

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

	
	///////////////////////////////////////////////
	const signed_tx = aptos.transaction.sign ({ 
		signer: account_1, 
		transaction: unsigned_tx
	});	
	console.log ({
		unsigned_tx,
		signed_tx
	})
	const committed_transaction = await aptos.transaction.submit.simple ({ 
		transaction: unsigned_tx, 
		senderAuthenticator: signed_tx
	});
	console.log ({ committed_transaction })

}