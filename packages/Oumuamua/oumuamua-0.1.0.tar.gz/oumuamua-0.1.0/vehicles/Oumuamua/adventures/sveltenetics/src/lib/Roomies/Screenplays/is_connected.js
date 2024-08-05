
/*
	import { the_ledger_ask_loop } from './Screenplays/is_connected'
 
 

*/



import { loop } from '$lib/taverns/loop'
import { request_ledger_info } from '$lib/PTO/General/Ledger_Info.API'

import { ask_for_freight } from '$lib/Roomies/Trucks'
	

let ledger_ask_count = 0;

export const the_ledger_ask_loop_creator = () => {
	return loop ({
		wait: 2000,
		wait_for_response: "yes",
		action: async () => {
			const freight = ask_for_freight ();
			
			const net_path = freight.net_path;
			
			const there_is_a_net_path = typeof net_path === "string" && net_path.length >= 1;
			if (there_is_a_net_path !== true) {
				console.info (`There's not a "net path" for the ledger loop.`)
				return;
			}
			
			ledger_ask_count += 1
			const current_ledger_ask_count = ledger_ask_count;
			
			try {
				const { enhanced } = await request_ledger_info ({ net_path })
				//
				//	If the UI changed, after the ask, this filters
				//	the info that was returned from the ask.
				//
				if (ledger_ask_count == current_ledger_ask_count) {
					freight.net_connected = "yes"
					
					// const { chain_id: _chain_id } = enhanced;
					// chain_id = _chain_id;
					// block_height = enhanced.block_height;
					// epoch = enhanced.epoch;
				}
			}
			catch (exception) {
				freight.net_connected = "no"
			}
			
		}
	})
}