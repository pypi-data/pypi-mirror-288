

<script>


import Polytope from '$lib/trinkets/Polytope/Polytope_Modal.svelte'
import _merge from 'lodash/merge'


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


const on_prepare = () => {
	polytope_modal.advance (({ freight }) => {
		return _merge ({}, freight, {
			showing: 'yes',
			name: 'transfer',
			unfinished: {
				showing: 'no',
			},
			back: {
				has: 'no'
			},
			next: {
				has: 'no'
			},
			panel: {
				text: 'panel'
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
	<div slot="leaves">
		<div>
			<div>leave 1</div>
			
			<button 
				on:click={ on_click }
				
				type="button" 
				class="btn variant-filled"
			>Button</button>
		</div>
	</div>
	
	<div slot="unfinished">
		<div>
			This is unfinished
		</div>
	</div>
</Polytope>