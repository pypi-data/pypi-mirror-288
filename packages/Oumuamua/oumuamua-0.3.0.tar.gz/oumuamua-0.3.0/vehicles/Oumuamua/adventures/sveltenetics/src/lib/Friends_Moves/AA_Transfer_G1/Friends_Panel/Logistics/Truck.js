


/*
 

*/

import { build_truck } from '$lib/trucks'
	
// import * as Fraction from 'fraction.js'	
import Fraction from 'fraction.js';
import Big from 'big.js';

const trucks = {}


export const verify_land = () => {
	console.log ('verify land')
	
	const freight = trucks [1].freight;
	const current_land = freight.current.land;
	
	if (current_land === "Transaction_Fields") {
		// console.log (freight.lands.transaction_fields)
		
		//const { next, back } = freight.lands.transaction_fields.verify (freight);
		const next = "yes"
		const back = "no"
		
		trucks [1].freight.lands.Transaction_Fields.next = next
		trucks [1].freight.lands.Transaction_Fields.back = back
		
		trucks [1].freight.current.back = back
		trucks [1].freight.current.next = next
	}
	else if (current_land === "Unsigned_Transaction") {
		trucks [1].freight.current.back = "yes"
		trucks [1].freight.current.next = "yes"
	}
	else if (current_land === "Transaction_Signature_Fields") {
		if (freight.transaction_signature.verified === "yes") {
			trucks [1].freight.current.next = "yes"
		}
		else {
			trucks [1].freight.current.next = "no"
		}
		
		trucks [1].freight.current.back = "yes"
	}
	else if (current_land === "Transaction_Signature") {
		trucks [1].freight.current.back = "yes"
		trucks [1].freight.current.next = "yes"
	}
	else if (current_land === "Ask_Consensus") {
		trucks [1].freight.current.back = "yes"
		trucks [1].freight.current.next = "no, last"
	}
	else {
		trucks [1].freight.current.back = "no"
		trucks [1].freight.current.next = "no"
	}
};

export const delete_unsigned_transaction = () => {
	trucks [1].freight.unsigned_transaction = {
		hexadecimal_string: "",
		Aptos_object: {},
		Aptos_object_fiberized: "",
		
		alerts_info: [],
		
		// freight.unsigned_transaction.exception_text = ""
		exception_text: ""
	}
}



export const refresh_truck = () => {
	trucks [1] = build_truck ({
		freight: {
			unfinished_extravaganza: {
				showing: "no"
			},
			
			current: {
				land: "Transaction_Fields",
				next: "no",
				back: "no"
			},
			
			lands: {
				Transaction_Fields: {
					next: "no",
					back: "no"
				},
				Unsigned_Transaction: {
					next: "no",
					back: "yes"
				},
				Transaction_Signature_Fields: {
					next: "no",
					back: "yes"
				},
				Transaction_Signature: {
					// freight.lands.Transaction_Signature.next
					next: "no",
					back: "yes"
				}
			},
			
			fields: {
				ICANN_net_path: "https://api.devnet.aptoslabs.com/v1",
				net_name: "devnet",
				//
				from_address_hexadecimal_string: "522D906C609A3D23B90F072AD0DC74BF857FB002E211B852CE38AD6761D4C8FD",
				from_address_exception: "",
				from_address_permitted: "no",
				//
				//
				to_address_hexadecimal_string: "26F4F8D7C5526BA7DA453041D3A858CFEA06D911C90C2E40EDA2A7261826858C",
				to_address_exception: "",
				to_address_permitted: "no",
				//
				//
				currency: "APT", // Octas
				//
				amount: 1,
				amount_of_Octas: "1e8",
				amount_of_APT: "1",
				actual_amount_of_Octas: calculate_actual_octas ("1e8"),
				//
				//
				transaction_expiration: "600",
				//
				use_custom_gas_unit_price: "yes",
				gas_unit_price: "100",
				//
				use_custom_max_gas_amount: "yes",
				max_gas_amount: "200000",
				
				problems: {
					from_address_hexadecimal_string: "",
					to_address_hexadecimal_string: "",
					amount: ""
				}
			},
			unsigned_transaction: {
				hexadecimal_string: "",
				//
				//	freight.unsigned_transaction.Aptos_object
				Aptos_object: {},
				Aptos_object_fiberized: "",
				
				//	freight.unsigned_transaction.alerts_info
				alerts_info: [],
				
				// freight.unsigned_transaction.exception_text = ""
				exception_text: ""
			},
			transaction_signature: {
				// freight.transaction_signature.hexadecimal_string
				hexadecimal_string: "",
				//	freight.transaction_signature.Aptos_object
				Aptos_object: {},
				Aptos_object_fiberized: "",
				//
				
				
				//
				// freight.transaction_signature.info_text
				info_text: "waiting for a transaction signature",
				//
				// freight.transaction_signature.verified = "yes"
				verified: "no",
				//
				//
				barcode_land: {},
				//
				// freight.transaction_signature.hexadecimal_land.added = "yes"
				hexadecimal_land: {
					added: "no"
				}
			},
			ask_consensus: {
				transaction_Aptos_object_fiberized: "",
				transaction_hash: "",
				
				//
				// 	while waiting for transaction to process
				//
				//	freight.ask_consensus.waiting_info
				waiting_info: "",
				
				//	freight.ask_consensus.success_info
				success_info: "",
				
				//
				// freight.ask_consensus.exception_info
				exception_info: ""
			}
		}
	})
}

export const destroy_truck = () => {
	delete trucks [1];
}

export const retrieve_truck = () => {
	return trucks [1];
}


const calculate_actual_octas = (original_amount) => {
	let float_amount = parseFloat (original_amount)
	return float_amount.toString ()
}

//
//	const monitor = 
//
//
let latest_amount_of_Octas = "1e8"
let latest_amount = "1"
let latest_currency = "1"
export const monitor_truck = (action) => {	
	
	
	
	return trucks [1].monitor (({ freight }) => {
		
		
		//
		//	This might be deprecated.
		//
		//
		if (
			latest_currency != freight.fields.currency ||
			latest_amount != freight.fields.amount
		) {
			const previous_currency = latest_currency;
			const previous_amount = latest_amount;
			
			latest_currency = freight.fields.currency;
			latest_amount = freight.fields.amount;
			
			//
			//	reset the problem to ""
			//
			//
			freight.fields.problems.amount = ""
		}
		

		//
		//	This modifies the "next" & "back" buttons.
		//
		//
		verify_land ()
		
		action (freight);
	})
}







