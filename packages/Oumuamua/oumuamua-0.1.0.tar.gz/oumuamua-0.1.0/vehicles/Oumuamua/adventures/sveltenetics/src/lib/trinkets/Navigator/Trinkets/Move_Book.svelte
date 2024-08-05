

<script>
import { goto } from '$app/navigation';
import { parse_styles } from '$lib/trinkets/styles/parse.js';	
import { Aptos, AptosConfig, Network, Account } from "@aptos-labs/ts-sdk";
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import Panel from '$lib/trinkets/panel/trinket.svelte'

import Faucet_Move from '$lib/moves/faucet/trinket.svelte'
import APT_Move from '$lib/moves/APT/trinket.svelte'

import Moves_Picks_Modal from '$lib/trinkets/Moves_Picks_Modal/Trinket.svelte'
import { getModalStore } from '@skeletonlabs/skeleton';

const modalStore = getModalStore ();

let move = "faucet"
const choose_a_move = async () => {
	modalStore.trigger ({
		type: 'component',
		component: {
			ref: Moves_Picks_Modal
		},
		response: (r) => {
			console.log ('response:', r)
			// move = r;
			
			goto ('/friends/moves/' + r);
		}
	});
}

</script>


<div>
	<button type="button" class="btn bg-gradient-to-br variant-gradient-primary-secondary"
		on:click={choose_a_move}
	>Move Book</button>
</div>