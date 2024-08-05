

/*
	import { unpack_TP_AO_from_hexadecimal_string } from '../unpack/from_hexadecimal_string'
*/

/*
	Unpack the Transaction Petition from a hexadecimla string

	Checks:
		Equality [ 
			Unpacked hexadecimal string, 
			Original hexadecimal string 
		]
*/

import { 
	create_TP_AO_from_hexadecimal_string 
} from '../create/AO_from_hexadecimal_string'


export const unpack_TP_AO_from_hexadecimal_string = ({
	TP_hexadecimal_string
}) => {
	const {
		transaction_petition_object: TP_unpacked_object,
		transaction_petition_stringified: TP_unpacked_stringified
	} = create_TP_AO_from_hexadecimal_string ({
		transaction_petition_hexadecimal_string: TP_hexadecimal_string
	})
	const TP_unpacked_bytes = TP_unpacked_object.bcsToBytes ()
	const TP_unpacked_hexadecimal_string = string_from_Uint8Array (
		TP_unpacked_bytes
	)
	
	if (TP_hexadecimal_string !== TP_unpacked_hexadecimal_string) {
		throw new Error (JSON.stringify ({
			"note": "The original transaction petition hexadecimal string is not equal to the unpacked version.",
			TP_hexadecimal_string,
			TP_unpacked_hexadecimal_string
		}, null, 4))
	}
	
	return {
		TP_unpacked_object,
		TP_unpacked_hexadecimal_string
	}
}
