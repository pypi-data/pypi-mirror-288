


<script>

/*
	import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
	<Code_Wall 
		text={} 
		context={}
	/>
*/

import { clipboard } from '@skeletonlabs/skeleton';

export let text = ""
export let context = ""

export let can_clone = "no"

let clone_text = "Clone"
let timeout;
const on_clone = async () => {
	clearTimeout (timeout)
	
	clone_text = "Cloned"
	
	await new Promise (resolve => {
		timeout = setTimeout (() => {
			resolve ()
		}, 1000)
	})
	
	clone_text = "Clone"
}

</script>

<div>
	<div
		style="
			display: grid;
			grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
			grid-template-columns: min-content auto;
			grid-template-columns: min-content repeat(auto-fill, minmax(200px, 1fr));
			gap: 5px;
		"
	>
		{#if context.length >= 1 }
		<pre
			code_wall_context
			class='card'
			style="
				grid-column: 1; 
			
				box-sizing: border-box;
				height: 100%; 
				
				font-size: 1em;
				
				text-align: left;
				white-space: break-spaces;
				word-wrap: break-word;
				
				padding: 0.5cm;
				border-radius: 4px;
				color: inherit;
				
				display: flex;
				align-items: center;
				justify-content: center;
				text-align: center;
			"
		>{ context }</pre>
		{/if}
		
		<pre
			code_wall
			class='card'
			style="
				grid-column: 2; 
			
				box-sizing: border-box;
				height: 100%; 
				font-size: 1em;
				
				text-align: left;
				white-space: break-spaces;
				word-wrap: break-word;
				
				width: 100%;
				
				padding: 0.5cm;
				border-radius: 4px;
				color: inherit;
			"
		>{ text }</pre>
	</div>
	{#if can_clone === "yes" }
	<div
		style="
			text-align: right;
			padding-top: 0.5cm;
		"
	>
		<button 
			on:click={ on_clone }
			disabled={ clone_text === "Cloned" }
			use:clipboard={ text }
			class="btn variant-filled"
			type="button" 
		>{ clone_text }</button>
	</div>
	{/if}
</div>