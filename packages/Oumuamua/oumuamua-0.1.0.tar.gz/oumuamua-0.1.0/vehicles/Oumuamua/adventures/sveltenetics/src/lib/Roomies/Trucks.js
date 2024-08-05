


/*	
//	This is the +layout mount
//	This is the app level storage.
//
import {
	lease_roomies_truck,
	give_back_roomies_truck
} from '$lib/Roomies/Trucks'

onMount (async () => {
	lease_roomies_truck ()
})
onDestroy (async () => {
	give_back_roomies_truck ()
})
*/

/*	
import { onMount, onDestroy } from 'svelte'
import { check_roomies_truck, monitor_roomies_truck } from '$lib/Roomies/Trucks'

let RT_Prepared = "no"
let RT_Monitor;
let RT_Freight;
onMount (async () => {
	const Truck = check_roomies_truck ()
	RT_Freight = Truck.freight; 
	
	RT_Monitor = monitor_roomies_truck ((_freight) => {
		RT_Freight = _freight;
	})
	
	RT_Prepared = "yes"
});

onDestroy (() => {
	RT_Monitor.stop ()
}); 

// RT_Freight.net_path
// RT_Freight.net_name
*/


/*	
	import { ask_for_freight } from '$lib/Roomies/Trucks'
	const freight = ask_for_freight ();
*/

import * as AptosSDK from "@aptos-labs/ts-sdk";
import { build_truck } from '$lib/trucks'
import { the_ledger_ask_loop_creator } from './Screenplays/is_connected'


let the_ledger_ask_loop;


const trucks = {}

export const lease_roomies_truck = () => {
	let net_path = "https://api.mainnet.aptoslabs.com/v1"
	let net_name = "mainnet"
	
	if (typeof localStorage.net_name === "string") {
		net_name = localStorage.net_name	
	}
	if (typeof localStorage.net_path === "string") {
		net_path = localStorage.net_path	
	}
	
	trucks [1] = build_truck ({
		freight: {
			origin_address: "http://localhost:22000",
			
			net_path,
			net_name,
			net_connected: "no",
			
			aptos: new AptosSDK.Aptos (
				new AptosSDK.AptosConfig ({		
					fullnode: net_path,
					network: AptosSDK.Network.CUSTOM
				})
			)
		}
	})
	
	console.log (trucks [1].freight)
	
	the_ledger_ask_loop = the_ledger_ask_loop_creator ();
	the_ledger_ask_loop.play ();
}

export const ask_for_freight = () => {
	return trucks [1].freight;
}
export const give_back_roomies_truck = () => {
	the_ledger_ask_loop.stop ();
	delete trucks [1];
}

export const check_roomies_truck = () => {
	return trucks [1];
}
export const monitor_roomies_truck = (action) => {	
	return trucks [1].monitor (({ freight }) => {
		console.info ('Roomies Truck_Monitor', { freight })
		action (freight);
	})
}







