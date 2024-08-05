
/*
	import { find_transaction_by_hash } from '$lib/PTO/Transaction/find_by_hash'
	const { enhanced, transaction_fiberized } = await find_transaction_by_hash ({
		net_path: "",
		transaction_hash: ""
	})
*/

// enhanced.success

/*
	curl --request GET \
	--url https://api.mainnet.aptoslabs.com/v1/transactions/by_hash/__TXN_HASH__
*/

import { fiberize_transaction } from '$lib/PTO/Transaction/Fiberize'
	
export const find_transaction_by_hash = async ({
	net_path,
	transaction_hash
}) => {
	const URL = `${ net_path }/transactions/by_hash/${ transaction_hash }`
	
	const proceeds = await fetch (URL);
	const enhanced = await proceeds.json ()
	
	const transaction_fiberized = fiberize_transaction ({ transaction: enhanced })
	
	return {
		enhanced,
		transaction_fiberized
	};
}