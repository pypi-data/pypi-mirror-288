

/*
	Goals:
		Choose both: 
			* chain_id
			* address
	
	https://github.com/aptos-labs/aptos-ts-sdk/blob/687e00152cc139f406182186fcd05b082dd70639/examples/typescript/custom_client.ts#L87
*/

// import { make_unsigned_tx } from '$lib/Aptos_Moves/APT_send/unsigned_tx_make'
// var now = new Aptos_SDK.U64 (Math.floor (Date.now () / 1000))
// var exp = new Aptos_SDK.U64 (Math.floor (Date.now () / 1000) + 600)

////
///
//
import * as Aptos_SDK from "@aptos-labs/ts-sdk";
//
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
import { 
	build_unsigned_tx_from_hexadecimal_string 
} from '$lib/PTO/Transaction/Unsigned/from_hexadecimal_string'
import { request_ledger_info } from '$lib/PTO/General/Ledger_Info.API'
//
//
//\
//\\


import { pick_expiration } from './screenplays/pick_expiration'
import { provider } from './screenplays/provider'


export const make_unsigned_transaction = async ({
	net_path,
	
	from_address_hexadecimal_string,
	to_address_hexadecimal_string,
	amount,
	
	transaction_expiration,
	
	freight
}) => {
	const the_function = "0x1::aptos_account::transfer"
	// const the_function = "0x1::coin::transfer"
	
	const { enhanced } = await request_ledger_info ({ net_path })
	const { chain_id } = enhanced;
	
	//
	//	https://github.com/aptos-labs/aptos-ts-sdk/blob/687e00152cc139f406182186fcd05b082dd70639/src/api/aptosConfig.ts
	//	https://github.com/search?q=repo%3Aaptos-labs%2Faptos-ts-sdk+fullnode%3A&type=code
	//
	const aptos = new Aptos_SDK.Aptos (new Aptos_SDK.AptosConfig ({		
		fullnode: net_path,
		network: Aptos_SDK.Network.CUSTOM
		// client: { provider: custom_client }
	}));

	const from_address = Aptos_SDK.AccountAddress.from (
		Uint8Array_from_string (from_address_hexadecimal_string)
	);
	const to_address = Aptos_SDK.AccountAddress.from (
		Uint8Array_from_string (to_address_hexadecimal_string)
	);

	
	
	
	//
	//	https://github.com/aptos-labs/aptos-ts-sdk/blob/01bf8369f4033996fe5bd20b2172fcad574b1108/src/transactions/types.ts#L100
	//
	//
	const options = {
		expireTimestamp: pick_expiration ({ 
			after_seconds: transaction_expiration 
		})
	}
	if (freight.fields.use_custom_gas_unit_price === "yes") {
		options.gasUnitPrice = BigInt (freight.fields.gas_unit_price);
	}
	if (freight.fields.use_custom_max_gas_amount === "yes") {
		options.maxGasAmount = BigInt (freight.fields.max_gas_amount);
	}
	
	const transaction_petition = await aptos.transaction.build.simple ({
		sender: from_address,
		data: {
			function: the_function,
			typeArguments: [],
			functionArguments: [
				to_address,
				amount
			]
		},
		options
	});
	
	
	/*const unsigned_transaction = new RawTransaction (
		from_address,
		BigInt (sequenceNumber),
		payload,
		BigInt(maxGasAmount),
		BigInt(gasUnitPrice),
		BigInt(expireTimestamp),
		new ChainId(chainId),
	);*/
	
	console.info ({
		transaction_petition
	})
	
	const transaction_petition_as_bytes = transaction_petition.bcsToBytes ()
	const transaction_petition_hexadecimal_string = string_from_Uint8Array (transaction_petition_as_bytes)
	
	////
	///
	// Check if can reverse:
	//
	const {
		unsigned_tx: unsigned_tx_reversed,
		unsigned_tx_stringified: unsigned_tx_stringified_reversed
	} = build_unsigned_tx_from_hexadecimal_string ({
		unsigned_tx_hexadecimal_string: transaction_petition_hexadecimal_string
	})
	const unsigned_tx_reversed_as_bytes = unsigned_tx_reversed.bcsToBytes ()
	const unsigned_tx_reversed_hexadecimal_string = string_from_Uint8Array (unsigned_transaction_as_bytes)
	if (transaction_petition_hexadecimal_string !== unsigned_tx_reversed_hexadecimal_string) {
		throw new Error ("An exception occurred while making the transaction petititon")
	}
	console.info ('reverse check was functional', unsigned_tx_stringified_reversed)
	//
	//\
	//\\
	
	console.info ({ 
		unsigned_transaction, 
		unsigned_transaction_hexadecimal_string,
		"exp": unsigned_transaction.rawTransaction.expiration_timestamp_secs
	})

	return {
		unsigned_tx: unsigned_transaction,
		unsigned_tx_as_hexadecimal_string: unsigned_transaction_hexadecimal_string
	}
}

