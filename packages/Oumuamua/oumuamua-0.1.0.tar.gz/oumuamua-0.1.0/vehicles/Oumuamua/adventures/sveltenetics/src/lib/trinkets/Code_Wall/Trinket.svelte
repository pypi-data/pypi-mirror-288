


<script>

/*
	import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
	<Code_Wall text={} />
*/

import { clipboard } from '@skeletonlabs/skeleton';

export let text = ""
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
	<pre
		code_wall
		class='card'
		style="
			box-sizing: border-box;
			height: 100%; 
			font-size: 1em;
			
			text-align: left;
			white-space: break-spaces;
			word-wrap: break-word;
			
			padding: 0.5cm;
			border-radius: 4px;
			color: inherit;
		"
	>{ text }</pre>
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