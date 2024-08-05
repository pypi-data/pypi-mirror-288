



/*
import { 
	refresh_truck, 
	retrieve_truck, 
	monitor_truck,
	verify_land
} from '$lib/Friends_Moves/AA_Transfer_G1/Relatives_Panel/Logistics/Truck'

let prepared = "no"
let Truck_Monitor;
let freight;
onMount (async () => {
	const Truck = retrieve_truck ()
	freight = Truck.freight; 
	
	freight.current.land = "Transaction_Fields"
	
	Truck_Monitor = monitor_truck ((_freight) => {
		freight = _freight;
		console.log ("Transaction Fields: Truck_Monitor", { freight })
	})
	
	prepared = "yes"
});

onDestroy (() => {
	Truck_Monitor.stop ()
});
*/

/*
import { 
	refresh_truck, 
	destroy_truck
} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'

onMount (async () => {
	refresh_truck ()
})
onDestroy (() => {
	destroy_truck ()
});

*/

/*
	
*/

/*
	const truck_monitor = await monitor_truck ()
*/

/*
	import { 
		retrieve_items, 
		change_item
		panel_checks
	} from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Logistics/Truck'
	const items = await retrieve_items ()
	
	await change_item ("unsigned_transaction.hexadecimal_string", "")
*/

//
//	trucks [1].freight ["unsigned_transaction_fields"] ["ICANN_net_path"] = "another.path"
//	delete trucks [1]
//

import { build_truck } from '$lib/trucks'
	
const trucks = {}

const calculate_actual_octas = (original_amount) => {
	let float_amount = parseFloat (original_amount)
	return float_amount.toString ()
}

export const verify_land = () => {
	console.log ('verify land')
	
	const freight = trucks [1].freight;
	const current_land = freight.current.land;
	
	if (current_land === "Unsigned_Transaction_Fields") {
		console.log ({ added: freight.Unsigned_Transaction_Fields.added })
		
		if (freight.Unsigned_Transaction_Fields.added === "yes") {
			trucks [1].freight.current.next = "yes"
		}
		else {
			trucks [1].freight.current.next = "no"
		}
		
		trucks [1].freight.current.back = "no"
	}
	else if (current_land === "Unsigned_Transaction") {
		trucks [1].freight.current.next = "yes"
		trucks [1].freight.current.back = "yes"
	}
	else if (current_land === "Unsigned_Transaction_Signature") {
		if (freight.Unsigned_Transaction_Signature.signed === "yes") {
			trucks [1].freight.current.next = "yes"
		}
		else {
			trucks [1].freight.current.next = "no"
		}
		
		trucks [1].freight.current.back = "yes"
	}
	else if (current_land === "Transaction_Signature") {
		trucks [1].freight.current.next = "no, last"
		trucks [1].freight.current.back = "yes"
	}
	else {
		trucks [1].freight.current.back = "no"
		trucks [1].freight.current.next = "no"
	}
};

/*verify: (freight) => {
	console.log ('verify transaction_fields')
	
	return {
		next: "yes",
		back: "no"
	}
}*/

export const delete_unsigned_transaction = () => {
	trucks [1].freight.unsigned_transaction = {
		hexadecimal_string: "",
		Aptos_object: {},
		Aptos_object_fiberized: "",
		
		// freight.unsigned_transaction.exception_text = ""
		exception_text: ""
	}
}


let latest_amount_of_Octas = "1e8"
export const refresh_truck = () => {
	trucks [1] = build_truck ({
		freight: {
			unfinished_extravaganza: {
				showing: "no"
			},
			
			current: {
				land: "Unsigned_Transaction_Fields",
				next: "no",
				back: "no"
			},
			
			lands: {
				// Camera + Hexadecimal Field
				Unsigned_Transaction_Fields: {
					next: "yes",
					
					// freight.Unsigned_Transaction_Fields
					back: "no"
				},
				Unsigned_Transaction: {
					next: "no",
					back: "no"
				},
				Unsigned_Transaction_Signature: {
					next: "no",
					back: "yes"
				},
				Transaction_Signature: {
					next: "no",
					back: "yes"
				}
			},
			
			Unsigned_Transaction_Fields: {
				//	freight.Unsigned_Transaction_Fields.hexadecimal_string
				hexadecimal_string: "",
				//
				//	freight.Unsigned_Transaction_Fields.Aptos_object
				Aptos_object: {},
				//
				//	freight.Unsigned_Transaction_Fields.Aptos_object_fiberized
				Aptos_object_fiberized: "",
				
				added: "no",
				info_text: "To proceed, the transaction petition needs to be added.",
				
				
				
				hexadecimal: {
					// freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception_summary = ""
					// freight.Unsigned_Transaction_Fields.hexadecimal.textarea_exception = ""
					textarea_exception: "",
					textarea_exception_summary: "",
					
					// freight.Unsigned_Transaction_Fields.hexadecimal.button_text = "Add"
					button_text: "Add"
				},
				camera: {
					searching: "yes",
					barcode_found: "no",
				}				
			},
			
			Unsigned_Transaction_Signature: {
				//
				//	freight.Unsigned_Transaction_Signature.private_key_hexadecimal_string
				private_key_hexadecimal_string: "",
				
				//
				//	freight.Unsigned_Transaction_Signature.hexadecimal_string
				hexadecimal_string: "",
				//
				//	freight.Unsigned_Transaction_Signature.Aptos_object
				Aptos_object: {},
				//
				//	freight.Unsigned_Transaction_Signature.Aptos_object_fiberized
				Aptos_object_fiberized: "",
				
				//	freight.Unsigned_Transaction_Signature.signed
				signed: "no",
				
				//
				//
				//
				//	freight.Unsigned_Transaction_Signature.info_text
				// info_text: "waiting for a transaction signature",
			},
			
			fields: {}
		}
	})
}

export const destroy_truck = () => {
	delete trucks [1];
}

export const retrieve_truck = () => {
	return trucks [1];
}

//
//	const monitor = 
//
//
export const monitor_truck = (action) => {
	return trucks [1].monitor (({ freight }) => {		
		verify_land ()
		action (freight);
	})
}







