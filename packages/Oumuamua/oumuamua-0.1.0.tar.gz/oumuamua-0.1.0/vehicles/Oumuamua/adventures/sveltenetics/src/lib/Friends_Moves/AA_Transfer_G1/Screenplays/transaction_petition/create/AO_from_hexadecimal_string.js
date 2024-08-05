



/*
	// Relatives

	import { 
		create_TP_AO_from_hexadecimal_string 
	} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/transaction_petition/create/from_hexadecimal_string'
*/



/*
	import { 
		create_TP_AO_from_hexadecimal_string 
	} from '../create/from_hexadecimal_string'
	
	const {
		UTP_AO,
		UTP_bytes,
		UTP_hexadecimal_string,
		UTP_stringified
	} = create_TP_AO_from_hexadecimal_string ({ TP_hexadecimal_string })
*/

import * as Aptos_SDK from "@aptos-labs/ts-sdk";

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import { stringify_TP_AO } from '../stringify'
	

export const create_TP_AO_from_hexadecimal_string = ({
	TP_hexadecimal_string
}) => {
	const UTP_bytes = Uint8Array_from_string (TP_hexadecimal_string)
	const UTP_AO = Aptos_SDK.SimpleTransaction.deserialize (
		new Aptos_SDK.Deserializer (
			UTP_bytes
		)
	);
	const UTP_stringified = stringify_TP_AO ({ TP_AO: UTP_AO })
	
	const UTP_hexadecimal_string = string_from_Uint8Array (UTP_bytes)
	
	return {
		UTP_AO,
		UTP_bytes,
		UTP_hexadecimal_string,
		UTP_stringified
	}
}