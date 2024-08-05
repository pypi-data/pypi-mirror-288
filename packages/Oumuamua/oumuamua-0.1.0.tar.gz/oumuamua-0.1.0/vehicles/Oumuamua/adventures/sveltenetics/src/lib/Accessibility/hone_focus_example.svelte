
<script>

//

import { onMount } from 'svelte'
import { hone_focus } from '$lib/Accessibility/hone_focus'

let start_of_panel = ""
let end_of_panel = ""
let panel = ""
let escape_to = ""
onMount (() => {
	hone_focus ({
		escape_to_element: escape_to,
		after_escape () { console.log ('escaped') },
		
		panel_element: panel,
		first_element: start_of_panel,
		last_element: end_of_panel
	})
})


</script>

<div>
	<header>Hone Focus</header>
	
	<button 
		outside_button
		type="button" 
		class="btn variant-filled"
		bind:this={ escape_to }
	>Outside</button>
	
	<div style="height: 20px"></div>
	
	<div 
		the_panel
		bind:this={ panel }
		style="
			border: 4px solid black;
			min-height: 500px;
			width: 100%;
			border-radius: 9px;
			padding: 12px;
		"
	>	
		<div tabindex="0" bind:this={ start_of_panel } start_of_panel>Start of Panel</div>
		
		<hr class="!border-t-4" style="margin: 8px 0"/>
		
		<button type="button" class="btn variant-filled">Button</button>	
		
		<hr class="!border-t-4" style="margin: 8px 0"/>
		
		<button type="button" class="btn variant-filled">Button</button>
		
		<hr class="!border-t-4" style="margin: 8px 0"/>
		
		<div tabindex="0" bind:this={ end_of_panel } end_of_panel>End of Panel</div>
	</div>
</div>