

<script>

//
//	import Panel from '$lib/trinkets/panel/trinket.svelte'
//
//

/*
<Panel 
	styles={{
		'width': '33%', 
		'height': '200px' 
	}}
></Panel>
*/

import { parse_styles } from '$lib/trinkets/styles/parse.js';

export let styles;

console.log ({ styles })
</script>

<div
	class="card"
	style="{parse_styles ({
		'border-radius': '8px',
		'padding': '8px',
		
		...styles
	})}"
>
	<slot></slot>
</div>


