
/*
	import { ask_latest_block_number } from '$lib/PTO/Blocks/Latest'
	await ask_latest_block_number ({ 
		net_path 
	})
*/

// https://github.com/aptos-labs/aptos-developer-discussions/discussions/198
// https://aptos.dev/en/build/indexer/txn-stream

import { Aptos, AptosConfig } from "@aptos-labs/ts-sdk";

export const ask_latest_block_number = async ({
	net_path
}) => {
	const proceeds = await fetch (`${ net_path }`);	
	const enhanced = await proceeds.json ()
	
	return { enhanced, net_path };
}

