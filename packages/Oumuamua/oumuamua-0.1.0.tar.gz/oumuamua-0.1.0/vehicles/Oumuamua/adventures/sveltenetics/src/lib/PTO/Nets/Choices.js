
/*
	import { ask_for_choices } from '$lib/PTO/Nets/Choices' 
	const net = ask_for_choices ()
*/

/*
	import { ask_for_net_name } from '$lib/PTO/Nets/Choices' 
	const net = await ask_for_net_name ("mainnet")
*/



const nets = {
	"mainnet": {
		"name": "mainnet",
		"path": "https://api.mainnet.aptoslabs.com/v1"
	},
	"testnet": {
		"name": "testnet",
		"path": "https://api.testnet.aptoslabs.com/v1"
	},
	"devnet": {
		"name": "devnet",
		"path": "https://api.devnet.aptoslabs.com/v1"
	},
	"custom": {
		"name": "custom",
		"path": ""
	}
}

export const ask_for_net_name = async (net_name) => {
	return nets [ net_name ]
}

export const ask_for_choices = async () => {
	return nets;
}