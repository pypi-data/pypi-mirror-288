


<script>
	
/*
	Friends_Moves:
		@ Friends_Moves
		@ Activities
		@ Adventures
		
		@ Postures
		@ Presences
*/

///
//
import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
//
//
import Layer_Octas_Gifts_Friends from '$lib/Friends_Moves/AA_Transfer_G1/Friends_Panel/Trinket.svelte'
import Layer_Faucet from '$lib/Friends_Moves/Faucet/Trinket.svelte'
import Friends_Move_Coin_Transfer_G1 from '$lib/Friends_Moves/Coin_Transfer_G1/Friends_Move/Trinket.svelte'
//
import { parse_styles } from '$lib/trinkets/styles/parse'
import Panel from '$lib/trinkets/panel/trinket.svelte'
//
//\

const trends = {
	panel: {
		position: 'relative',
		display: 'inline-flex',
		//'width': '33%', 
		'height': '200px',
		'align-items': 'center',
		'justify-content': 'center',
		'flex-direction': 'column'
	},
	anchor: parse_styles ({
		position: 'absolute',
		height: '100%',
		width: '100%',
		
		display: 'flex',
		'align-items': 'center',
		'justify-content': 'center',
		'text-decoration': 'none',
		'text-align': 'center',
		'font-size': '2em'
	})
}

const modal_store = getModalStore ();

const octas_gifts_v1 = () => {
	console.log ('sending from account_1 to account_2')	
	
	modal_store.trigger ({
		type: 'component',
		component: {
			ref: Layer_Octas_Gifts_Friends,
			props: { 
				modal_store
			}
		}
	});
}

const octas_faucet = () => {
	modal_store.trigger ({
		type: 'component',
		component: {
			ref: Layer_Faucet,
			props: { 
				modal_store
			}
		}
	});
}

const open_coin_transfer = () => {
	modal_store.trigger ({
		type: 'component',
		component: {
			ref: Friends_Move_Coin_Transfer_G1,
			props: { 
				modal_store
			}
		}
	});
}

</script>

<style>

@media (max-width: 600px) {
    .latest-block-panel {
		flex-direction: column !important;
	}
}

</style>

<svelte:head>
	<title>Moves</title>
	<meta name="description" content="Aptos Moves" />
</svelte:head>

<section
	quests_address
	style={ parse_styles ({
		position: 'relative',
		display: 'grid',
		'width': '100%',
		'grid-template-columns': 'repeat(auto-fit, minmax(400px, 1fr))',
		'grid-gap': '10px'
	}) }
>
	<Panel 
		styles={ trends.panel }
	>		
		<div class="relative inline-block">
			<button 
				faucet
				
				on:click={ octas_faucet }
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
				style="
					font-size: 1.3em;
					padding: 12px 54px;
					margin-top: 10px;
					
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
				"
			>
				<p>Faucet</p>
				<span 
					class="badge variant-filled-primary"
					style="margin: 0; display: none;"
				>Iteration 1</span>
			</button>
			
		</div>
	</Panel>

	<Panel 
		styles={ trends.panel }
	>		
		<div class="relative inline-block">

			<button 
				octas_gifts__version_1
				
				on:click={ octas_gifts_v1 }
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
				style="
					font-size: 1.3em;
					padding: 12px 54px;
					margin-top: 10px;
					
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
				"
			>
				<p>Aptos Account Transfer</p>
				<span 
					class="badge variant-filled-primary"
					style="margin: 0; display: none;"
				>Iteration 1</span>
			</button>
		</div>

		<div style="height: 12px" />

		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.2em;
			"
		>
			<span>Function</span>
			<span class="badge variant-filled-surface">0x1::aptos_account::transfer</span>
		</span>
	</Panel>
	
	<Panel 
		styles={ trends.panel }
	>		
		<div class="relative inline-block">

			<button 
				octas_gifts__version_1
				
				on:click={ open_coin_transfer }
				type="button" 
				class="btn bg-gradient-to-br variant-gradient-primary-secondary"
				style="
					font-size: 1.3em;
					padding: 12px 54px;
					margin-top: 10px;
					
					display: flex;
					flex-direction: column;
					justify-content: center;
					align-items: center;
				"
			>
				<p>Coin Transfer</p>
				<span 
					class="badge variant-filled-primary"
					style="margin: 0; display: none;"
				>Iteration 1</span>
			</button>
		</div>

		<div style="height: 12px" />

		<span class="badge variant-soft"
			style="
				position: relative;
				font-size: 1.2em;
			"
		>
			<span>Function</span>
			<span class="badge variant-filled-surface">0x1::coin::transfer</span>
		</span>
	</Panel>
</section>

