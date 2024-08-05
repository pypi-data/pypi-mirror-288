



/*
	import { send_coins_from_faucet } from '$lib/PTO/Faucet/send'
	const { tx } = send_coins_from_faucet ({
		amount:
		address:
		URL: 'https://faucet.devnet.aptoslabs.com/mint'
	})
*/

/*
	curl -X POST
'https://faucet.devnet.aptoslabs.com/mint?amount=10000&address=0xd0f523c9e73e6f3d68c16ae883a9febc616e484c4998a72d8899a1009e5a89d6'
*/

export const send_coins_from_faucet = async ({
	amount,
	address,
	URL
}) => {
	const params = new URLSearchParams({
		amount,
		address
	});

	const proceeds = await fetch(`${URL}?${params.toString()}`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		}
	});
	
	const enhance = await proceeds.json ()
	
	return {
		tx: enhance [ 0 ]
	};
	
	/*
	.then(response => {
		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}
		return response.json ();
	})
	.then(data => {
		console.log('Success:', data);
	})
	.catch(error => {
		console.error('Error:', error);
	});
	*/
	
}