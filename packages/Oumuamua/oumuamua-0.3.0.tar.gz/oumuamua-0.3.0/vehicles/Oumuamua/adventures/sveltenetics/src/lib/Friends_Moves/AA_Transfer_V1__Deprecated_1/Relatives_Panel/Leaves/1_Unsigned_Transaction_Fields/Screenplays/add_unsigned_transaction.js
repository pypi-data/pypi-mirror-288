


//

import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'

export const add_unsigned_transaction = async ({
	unsigned_transaction_hexadecimal_string,
	freight
}) => {
	const {
		unsigned_tx,
		unsigned_tx_stringified
	} = build_unsigned_tx_from_hexadecimal_string ({
		unsigned_tx_hexadecimal_string: unsigned_transaction_hexadecimal_string
	})
	
	freight.Unsigned_Transaction_Fields.Aptos_object = unsigned_tx
	freight.Unsigned_Transaction_Fields.Aptos_object_fiberized = unsigned_tx_stringified
	freight.Unsigned_Transaction_Fields.hexadecimal_string = unsigned_transaction_hexadecimal_string
	
	freight.Unsigned_Transaction_Fields.info_text = "The unsigned transaction was added."
	
	freight.Unsigned_Transaction_Fields.added = "yes"
}




//