

/*
	import { 
		hexadecimal_Signature_to_Aptos_Object 
	} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/hexadecimal_Signature_to_Aptos_Object' 
*/

import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import * as AptosSDK from "@aptos-labs/ts-sdk";

export const hexadecimal_Signature_to_Aptos_Object = (signed_transaction_hexadecimal_string) => {
	return AptosSDK.AccountAuthenticator.deserialize (
		new AptosSDK.Deserializer (
			Uint8Array_from_string (signed_transaction_hexadecimal_string)
		)
	)
}