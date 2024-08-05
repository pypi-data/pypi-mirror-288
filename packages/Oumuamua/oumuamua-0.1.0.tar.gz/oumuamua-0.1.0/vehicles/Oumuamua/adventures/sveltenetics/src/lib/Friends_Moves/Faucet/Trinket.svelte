

<script>

// import Friends_Move_Coin_Transfer_G1 from '$lib/Friends_Moves/Coin_Transfer_G1/Friends_Move/Trinket.svelte'

import Polytope from '$lib/trinkets/Polytope/Polytope_Modal.svelte'

import _merge from 'lodash/merge'

import Leaf_1 from './Leaf_1.svelte'

const prepare = () => {
	return {
		name: "Transfer",
		next: "yes",
		back: "yes"
	}
}

let polytope_modal;

const on_click = () => {
	polytope_modal.advance (({ freight }) => {
		freight.name = "panel"
		return freight;
	})
}

const on_modal_change = () => {}

let current = 1;
const on_next_pressed = () => {
	console.info ("on_next_pressed")
	
	polytope_modal.advance (({ freight }) => {
		if (freight.next.permitted === "yes") {
			current += 1
		}
		else {
			if (freight.next.has_alert === "yes") {
				freight.unfinished.showing = "yes"
			}
		}
		
		console.info ({ freight })
		
		return freight;		
	})
}

const on_prepare = () => {
	polytope_modal.advance (({ freight }) => {
		return _merge ({}, freight, {
			showing: 'yes',
			name: 'Faucet',
			unfinished: {
				showing: 'no',
			},
			back: {
				has: "no",
				text: 'Back',
				permitted: "no",
				go: () => {
					console.log ('back pressed')
				}
			},
			next: {
				has: "no",
				text: 'Unfinished',
				permitted: "no",
				has_alert: "yes",
				go: () => {
					on_next_pressed ()
				}
			},
			panel: {
				text: ''
			}
		})
		
		// freight.name = "panel"
		// freight.show = "yes"
		return freight;
	})
}

</script>


<Polytope 
	bind:this={ polytope_modal }
	on_change={ on_modal_change }
	on_prepare={ on_prepare }
>
	<div slot="leaves"
		style="
			height: 100%;
			width: 100%;
			
			display: flex;
			justify-content: center;
			align-items: center;
		"
	>
		{#if current === 1}
		<Leaf_1 />
		{/if}
	</div>
	
	<div slot="unfinished">
		<div>
			This is unfinished
		</div>
	</div>
</Polytope>