




/*
	import { 
		build_unsigned_tx_from_hexadecimal_string 
	} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'
	
	const {
		unsigned_tx,
		unsigned_tx_stringified
	} = build_transaction_petition_object_from_hexadecimal_string ({
		unsigned_tx_hexadecimal_string
	})
*/

import * as Aptos_SDK from "@aptos-labs/ts-sdk";

import { stringify_UT } from '$lib/PTO/Transaction/Unsigned/Stringify'
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

export const build_transaction_petition_object_from_hexadecimal_string = ({
	transaction_petition_hexadecimal_string
}) => {
	const transaction_petition = Aptos_SDK.SimpleTransaction.deserialize (
		new Aptos_SDK.Deserializer (
			Uint8Array_from_string (transaction_petition_hexadecimal_string)
		)
	);
	
	// const unsigned_tx_stringified = JSON.stringify (unsigned_tx, bigIntReplacer, 4);
	const unsigned_tx_stringified = stringify_UT ({ unsigned_tx })
	
	return {
		transaction_petition,
		transaction_petition_fiberized
	}
}