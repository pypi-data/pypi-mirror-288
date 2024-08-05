



<script>

//
//	https://schum123.github.io/svelte-loading-spinners/
//


//
import Unfinished from './Trinkets/Unfinished.svelte'
//
import { onMount } from 'svelte'
//
import { Modal, getModalStore } from '@skeletonlabs/skeleton';
import { ConicGradient } from '@skeletonlabs/skeleton';
//
import Eternal_1_Progress from '$lib/trinkets/Progress/Eternal_1/Trinket.svelte'
//
const modal_store = getModalStore ();

$: freight = {
	showing: 'no',
	name: '',
	unfinished: {
		showing: 'no',
	},
	back: {
		has: 'yes',
		text: 'Back',
		permitted: "no",
		go: () => {}
	},
	next: {
		has: 'yes',
		text: 'Unfinished',
		permitted: "no",
		has_alert: "yes",
		go: () => {
			
		}
	},
	panel: {
		text: ''
	},
	close: () => {
		console.info ('close_the_modal')
		modal_store.close ();
	}
}


export let on_prepare;
export const advance = (action) => {
	// @ advance, promote, evolve, adapt
	// @ promote
	// @ progress
	// @ habilitate
	
	const _freight = action ({ freight })
	freight = _freight;
}


const close_the_waiting_modal = () => {
	console.info ('close_the_waiting_modal')
	freight.unfinished.showing = "no"
}

const on_back_pressed = () => {
	freight.back.go ({
		freight
	})
}
const on_next_pressed = () => {
	freight.back.go ({
		freight
	})
}


onMount (() => {
	on_prepare ()
})

let wait_color = document.documentElement.classList.contains ("dark") ? "#000000" : "#FFFFFF";

</script>



<div 
	style="
		position: relative;
		top: 0;
		left: 0;
		padding: 0;
		width: calc(100vw - 36px);
		height: calc(100vh - 36px);
	
		overflow-y: scroll;
	"
>
	<div
		class="bg-surface-50-900-token border border-primary-500/30"
		style="
			display: flex;
			
			position: absolute;
			top: 0;
			left: 0;
			height: 100%;
			width: 100%;
			border-radius: 8px;
			
			overflow: hidden;
			
			flex-direction: column;
		"
	>
		<div
			style="
				display: flex;
				justify-content: center;
				flex-direction: column;
			"
		>
			<header
				style="
					padding: 0.2cm 0;
					text-align: center;
					font-size: 1.2em;
				"
			>{ freight.name }</header>
			<hr class="!border-t-2" />
		</div>
	</div>
	

	<Unfinished 
		showing={ freight.unfinished.showing }
		close={ close_the_waiting_modal }
	>
		<slot name="unfinished"></slot>
	</Unfinished>
	
	{#if freight.showing === "yes" }
	<div
		style="
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			width: 100%;
			
			box-sizing: border-box;
			padding: 0 10px 0;
			
			overflow: scroll;
			
			display: flex;
			flex-direction: column;
			justify-content: space-between;
		"
	>
		<div style="height: 2cm" />	
		<div
			style="
				height: 100%;
				overflow-y: scroll;
			"
		>
			<slot name="leaves"></slot>
		</div>
		<div style="height: 3cm" />
	</div>
	{:else}
	<div
		style="
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			width: 100%;
			
			box-sizing: border-box;
			padding: 0 10px 0;
			
			overflow: scroll;
			
			display: flex;
			justify-content: center;
			align-items: center;
		"
	>
		<div>	
			<div style="height: 2cm" />
			<div
				style="
					height: 1cm;
					width: 1cm;
				"
			>
				<Eternal_1_Progress 
					height={ "60px" }
					width={ "60px" }
					color={ wait_color }
				/>
			</div>
		</div>
	</div>
	{/if}


	<footer
		class="bg-surface-50-900-token border border-primary-500/30"
		style="
			position: absolute;
			bottom: 0;
			left: 0;
			width: 100%;
			height: 70px;
			border-radius: 8px;
			
		"
	>
		<hr class="!border-t-2" />
		
		<div 
			class="modal-footer"
			style="
				display: flex;
				align-items: center;
				justify-content: space-between;
			
				position: absolute;
				bottom: 0;
				left: 0;
				width: 100%;
				padding: 10px;
			"
		>
			<button 
				class="btn variant-filled" 
				on:click={ freight.close }
			>
				Quit
			</button>
			
			<div>{ freight.panel.text }</div>
		
			<div 
				style="
					position: relative;
					display: flex;
					
				"			
			>
				{#if freight.back && freight.back.has === "yes" }
				<button 
					modal-back
				
					disabled={ freight.back.permitted != "yes" }
					on:click={ freight.back.go }
					
					class="btn variant-filled"
				>{ freight.back.text }</button>
				{/if}
				
				<div style="width: 20px"></div>
				
				{#if freight.next && freight.next.has === "yes" }
				<button 
					modal-next
				
					disabled={ freight.next.permitted != "yes" && freight.next.has_alert != "yes" }
					on:click={ freight.next.go }
					
					class="btn variant-filled" 
					style="
						position: relative;
						
					"
				>
					{#if freight.next.permitted != "yes" }
					<span
						style="
							position: absolute;
							top: 0;
							left: 5px;
							height: 40px;
							width: 40px;
							transform: scale(0.6);
						"
					>
						<Eternal_1_Progress 
							height={ "40px" }
							width={ "50px" }
							color={ wait_color }
						/>
					</span>
					{/if}
					<span
						style="
							position: relative;
							margin-left: 40px;
						"
					>
						{ freight.next.text }
					</span>
				</button>
				{/if}
			</div>
		</div>
	</footer>
</div>
