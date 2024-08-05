


/*
	import { ask_commit } from './../Screenplays/ask_consensus_to_commit_transaction' 
	const { committed_transaction } = await ask_commit ({
		transaction,
		signed_transaction_hexadecimal_string
	})
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

export const ask_commit = async ({
	transaction,
	signed_transaction_hexadecimal_string
}) => {
	const config = new AptosSDK.AptosConfig ({})
	const aptos = new AptosSDK.Aptos ();
	
	/*
	const deserialized_signed_transaction = AptosSDK.AccountAuthenticator.deserialize (
		new AptosSDK.Deserializer (
			Uint8Array_from_string (
				signed_transaction_hexadecimal_string
			)
		)
	);
	*/
	
	const committed_transaction = await aptos.transaction.submit.simple ({ 
		transaction, 
		senderAuthenticator: deserialized_signed_transaction
	});
	
	console.log (`Committed transaction: ${committed_transaction.hash}`);
	
	return {
		committed_transaction
	}
}



//