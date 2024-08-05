

/*
	throws error if problem
*/

/*
	import { verify_unpacked_amount } from './../fields/amount/verify'
	verify_unpacked_amount ({
		original_amount_string,
		UTP_AO
	})
*/

//
//
import { convert_Uint8Array_to_integer_amount } from '../amount/transform'
//
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
//
import _get from 'lodash/get'
//
//

export const verify_unpacked_amount = ({
	original_amount_string,
	UTP_AO
}) => {
	if (typeof original_amount_string !== "string") {
		throw new Error (JSON.stringify ({
			"note": "The original amount is not a string.",
			"received": original_amount_string,
			"type": typeof original_amount_string
		}, null, 4))
	}
	
	const unpacked_amount_Uint8Array = _get (UTP_AO, [
		'rawTransaction', 'payload', 'entryFunction', 'args', 1, 'value', 'value'
	], '')
	const unpacked_amount_integer = convert_Uint8Array_to_integer_amount ({
		u_int_8_array: unpacked_amount_Uint8Array
	})
	const unpacked_amount_hexadecimal_string = string_from_Uint8Array (unpacked_amount_Uint8Array)
	
	console.log ({ 
		unpacked_amount_hexadecimal_string,
		unpacked_amount_Uint8Array,
		unpacked_amount_integer,
		amount: BigInt (original_amount_string)
	})
	
	
	if (unpacked_amount_integer !== BigInt (original_amount_string)) {
		throw new Error (JSON.stringify ({
			"note": "For some reason the unpacked Octas amount is different from the original Octas amount.",
			"original string": original_amount_string,
			"unpacked string": unpacked_amount_hexadecimal_string,
			"unpacked integer": unpacked_amount_integer,
			"unpacked Uint8Array": unpacked_amount_Uint8Array			
		}, null, 4))
	}
	
	return { 
		unpacked_amount_hexadecimal_string,
		unpacked_amount_Uint8Array 
	}
}

