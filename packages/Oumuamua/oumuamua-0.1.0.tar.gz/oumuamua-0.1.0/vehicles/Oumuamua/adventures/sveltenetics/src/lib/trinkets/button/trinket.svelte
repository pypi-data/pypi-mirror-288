

<script>

//
//	import Button from '$lib/trinkets/button/trinket.svelte'
//
//
import { parse_styles } from '$lib/trinkets/styles/parse.js';

export let styles;




</script>

<style>

button:active {
	box-shadow: 0 0 0 4px white, 0 0 0 8px black;
}


</style>

<button
	style="{parse_styles ({
		'background': 'white',
		'border': '4px solid black',
		'border-radius': '8px',
		'padding': '8px',
		
		...styles
	})}"
>
	<slot></slot>
</button>


