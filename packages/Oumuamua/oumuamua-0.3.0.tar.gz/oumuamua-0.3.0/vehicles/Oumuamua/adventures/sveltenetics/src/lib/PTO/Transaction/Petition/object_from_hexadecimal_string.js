




/*
	import { 
		build_transaction_petition_object_from_hexadecimal_string 
	} from '$lib/PTO/Transaction/Petition/object_from_hexadecimal_string'
	
	const {
		transaction_petition_object,
		transaction_petition_fiberized
	} = build_transaction_petition_object_from_hexadecimal_string ({
		transaction_petition_hexadecimal_string
	})
*/

import * as Aptos_SDK from "@aptos-labs/ts-sdk";

import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
import { 
	fiberize_transaction_petition_object 
} from '$lib/PTO/Transaction/Petition/Fiberize'
	

export const build_transaction_petition_object_from_hexadecimal_string = ({
	transaction_petition_hexadecimal_string
}) => {
	const transaction_petition_as_bytes = Uint8Array_from_string (
		transaction_petition_hexadecimal_string
	)
	
	const transaction_petition_object = Aptos_SDK.SimpleTransaction.deserialize (
		new Aptos_SDK.Deserializer (
			transaction_petition_as_bytes
		)
	);
	const transaction_petition_fiberized = fiberize_transaction_petition_object ({
		transaction_petition_object
	});
	
	return {
		transaction_petition_object,
		transaction_petition_fiberized
	}
}