

/*
	import { 
		hexadecimal_UT_to_Aptos_Object 
	} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/hexadecimal_UT_to_Aptos_Object' 
*/

import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import * as AptosSDK from "@aptos-labs/ts-sdk"

export const hexadecimal_UT_to_Aptos_Object = (unsigned_tx_hexadecimal_string) => {
	const uint = Uint8Array_from_string (unsigned_tx_hexadecimal_string);
	
	console.log ({ uint })
	
	return AptosSDK.SimpleTransaction.deserialize (
		new AptosSDK.Deserializer (uint)
	);
}