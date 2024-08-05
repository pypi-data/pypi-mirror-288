




/*
import { 
	create_TP_AO_from_fields
} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/transaction_petition/create/AO_from_fields'
*/


/*
	Goals:
		Choose both: 
			* chain_id
			* address
	
	https://github.com/aptos-labs/aptos-ts-sdk/blob/687e00152cc139f406182186fcd05b082dd70639/examples/typescript/custom_client.ts#L87
*/



////
//
import { pick_expiration } from './../fields/expiration'
import { unpack_TP_AO_from_hexadecimal_string } from '../unpack/from_hexadecimal_string'
import { provider } from './provider'
import { 
	create_TP_AO_from_hexadecimal_string 
} from './AO_from_hexadecimal_string'
import { stringify_TP_AO } from '../stringify'
//
////
//	verifications
//
import { verify_unpacked_amount } from './../fields/amount/verify'
import { verify_TP_AO } from './../verifications/AO'
//
//
import { request_ledger_info } from '$lib/PTO/General/Ledger_Info.API'
//
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'
//
//
import * as Aptos_SDK from "@aptos-labs/ts-sdk";
import _get from 'lodash/get'
//
//\\

import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
import { convert_Uint8Array_to_integer_amount } from '../fields/amount/transform'
		

/*
	fields: {
		ICANN_net_path: "https://api.mainnet.aptoslabs.com/v1",
		//
		from_address_hexadecimal_string: "522D906C609A3D23B90F072AD0DC74BF857FB002E211B852CE38AD6761D4C8FD",
		to_address_hexadecimal_string: "26F4F8D7C5526BA7DA453041D3A858CFEA06D911C90C2E40EDA2A7261826858C",
		//
		amount_of_Octas: "1e8",
		actual_amount_of_Octas: calculate_actual_octas ("1e8"),
		//
		transaction_expiration: "600"
	},
*/
export const create_TP_AO_from_fields = async ({
	net_path,
	
	from_address_hexadecimal_string,
	to_address_hexadecimal_string,
	amount,
		
	options
}) => {
	const { enhanced } = await request_ledger_info ({ net_path })
	
	//
	//	TODO: This should probably be from the address choice
	//
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

	const the_function = "0x1::aptos_account::transfer"
	const sender = from_address;
	const functionArguments = [
		to_address,
		amount
	]
	
	const TP_AO = await aptos.transaction.build.simple ({
		sender: from_address,
		data: {
			function: the_function,
			typeArguments: [],
			functionArguments
		},
		options
	});
	const TP_bytes = TP_AO.bcsToBytes ()
	const TP_hexadecimal_string = string_from_Uint8Array (TP_bytes)
	const TP_stringified = stringify_TP_AO ({ TP_AO })
	
	////
	//
	// 		Unpack:
	//
	//			TODO: check that fiberized objects are equivalent.
	//
	const {
		UTP_AO,
		UTP_bytes,
		UTP_hexadecimal_string,
		UTP_stringified
	} = create_TP_AO_from_hexadecimal_string ({ TP_hexadecimal_string })
	//
	//\\
	
	////
	//
	// 		Verify:
	//			Unpacked Amount
	//
	const { unpacked_amount_hexadecimal_string, unpacked_amount_Uint8Array } = verify_unpacked_amount ({
		original_amount_string: amount,
		UTP_AO
	})
	//
	verify_TP_AO ({
		TP_AO
	})
	//\\
	
	const arg_2nd_conversion = parse_with_commas (
		convert_Uint8Array_to_integer_amount ({
			u_int_8_array: unpacked_amount_Uint8Array 
		})
	)
	
	const info_alerts = [{
		"text": `For the second arg: "${ unpacked_amount_hexadecimal_string }" is equal to "${ arg_2nd_conversion }".`
	}]

	return {
		TP_AO,
		TP_bytes,
		TP_hexadecimal_string,
		TP_stringified,
		
		UTP_AO,
		UTP_bytes,
		UTP_hexadecimal_string,
		UTP_stringified,
		
		info_alerts,
		
		original_amount: amount,
		unpacked_amount_hexadecimal_string
	}
}

