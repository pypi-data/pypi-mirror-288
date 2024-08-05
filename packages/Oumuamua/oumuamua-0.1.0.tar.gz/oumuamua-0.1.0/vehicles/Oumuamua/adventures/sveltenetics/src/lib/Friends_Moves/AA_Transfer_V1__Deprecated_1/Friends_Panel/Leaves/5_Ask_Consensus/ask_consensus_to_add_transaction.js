
//
import { find_transaction_by_hash } from '$lib/PTO/Transaction/find_by_hash'
//
//
import * as AptosSDK from "@aptos-labs/ts-sdk";
//

import { 
	hexadecimal_UT_to_Aptos_Object 
} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/hexadecimal_UT_to_Aptos_Object' 
import { 
	hexadecimal_Signature_to_Aptos_Object 
} from '$lib/Friends_Moves/AA_Transfer_G1/Screenplays/hexadecimal_Signature_to_Aptos_Object' 

	
export const ask_consensus_to_add_transaction = async ({ freight }) => {
	try {
		//
		freight.ask_consensus.waiting_info = ""
		freight.ask_consensus.exception_info = ""
		freight.ask_consensus.waiting_info = ""
		
		
		console.log ('ask_consensus_to_add_transaction', {
			signature: freight.transaction_signature.Aptos_object,
			UT: freight.unsigned_transaction.Aptos_object,
		})
		
		console.log ({
			UT: freight.unsigned_transaction.hexadecimal_string,
			Signature: freight.transaction_signature.hexadecimal_string
		})
		
		const UT_Aptos_Object = hexadecimal_UT_to_Aptos_Object (
			freight.unsigned_transaction.hexadecimal_string
		)
		const Signature_Aptos_Object = hexadecimal_Signature_to_Aptos_Object (
			freight.transaction_signature.hexadecimal_string
		)
		
		freight.ask_consensus.waiting_info = "waiting for transaction"
		
		
		const aptos = new AptosSDK.Aptos (new AptosSDK.AptosConfig ({		
			fullnode: freight.fields.ICANN_net_path,
			network: AptosSDK.Network.CUSTOM
		}));
		
		
		const committed_transaction = await aptos.transaction.submit.simple ({ 
			transaction: UT_Aptos_Object, 
			senderAuthenticator: Signature_Aptos_Object
		});
		/*const committed_transaction = await aptos.transaction.submit.simple ({ 
			transaction: freight.unsigned_transaction.Aptos_object, 
			senderAuthenticator: freight.transaction_signature.Aptos_object
		});*/
		freight.ask_consensus.transaction_hash = committed_transaction.hash 
		
		console.log ('waiting for transaction', { committed_transaction })
		
		await aptos.waitForTransaction ({ 
			transactionHash: committed_transaction.hash 
		});
		
		console.log ('Maybe the transaction was added.')
		
		const { enhanced, transaction_fiberized } = await find_transaction_by_hash ({
			net_path: freight.fields.ICANN_net_path,
			transaction_hash: committed_transaction.hash
		})
		freight.ask_consensus.transaction_Aptos_object_fiberized = transaction_fiberized;
		
		if (enhanced.success === true) {
			freight.ask_consensus.waiting_info = ""
			freight.ask_consensus.success_info = "The consensus added the transaction to the blockchain."
		}
	}
	catch (exception) {
		console.error (exception)
		freight.ask_consensus.waiting_info = ""
		freight.ask_consensus.exception_info = exception.message;
	}
}


