
/*
	import { ask_APT_count } from '$lib/PTO/APT/Count'
	const { Octa_count, APT_count } = await ask_APT_count ({ address_hexadecimal_string })
*/

import { Aptos, AptosConfig, AccountAddress, Network } from "@aptos-labs/ts-sdk";
import { friends_has_stand } from "$lib/stands/friends"
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import Fraction from 'fraction.js';

export const ask_APT_count = async ({
	address_hexadecimal_string
}) => {
	const warehouse = friends_has_stand.warehouse ()
	const net_path = warehouse.net.path;
	const net = warehouse.net;

	console.log ({ net_path, network: Network.TESTNET })
	
	const nodeUrl = new URL (net_path);
	
	const aptosConfig = new AptosConfig ({
		// network: Network.MAINNET,
		
		// network: net_path,
		nodeUrl: net_path
	});
	const aptos = new Aptos (aptosConfig);
	
	console.log ({ aptos })
	
	const address_hexadecimal_string_ = "522D906C609A3D23B90F072AD0DC74BF857FB002E211B852CE38AD6761D4C8FD"
	
	const accountAddress = AccountAddress.from (Uint8Array_from_string (address_hexadecimal_string_));
	
	console.log ({ accountAddress })
	
	//
	// getAccountInfo
	//
	const proceeds2 = await aptos.getAccountResource ({
		accountAddress,
		resourceType: "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>",
	});
	
	const proceeds = await fetch (`${ net_path }/accounts/${ address_hexadecimal_string }/resources`)
	const enhanced = await proceeds.json ()
	
	console.log ({ enhanced })
	
	const Octa_count = enhanced.coin.value;
	const APT_count = Fraction (Octa_count).div (100000000).toFraction() 

	return {
		enhanced,
		
		Octa_count,
		APT_count,
		
		net
	}
}



