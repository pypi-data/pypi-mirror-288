
/*
	import { ask_blocks_by_version } from '$lib/PTO/Blocks/Version'
*/

import { friends_has_stand } from "$lib/stands/friends"

export const ask_blocks_by_version = async () => {
	const warehouse = friends_has_stand.warehouse ()
	const net_path = warehouse.net.path;
	
	const aptosConfig = new AptosConfig ({
		network: net_path
	});
	const aptos = new Aptos (aptosConfig);

	const proceeds = fetch (`${ net_path }/blocks/by_version/__VERSION__`);	
	const enhance = await proceeds.json ()
	
	console.log ({ enhance })

}