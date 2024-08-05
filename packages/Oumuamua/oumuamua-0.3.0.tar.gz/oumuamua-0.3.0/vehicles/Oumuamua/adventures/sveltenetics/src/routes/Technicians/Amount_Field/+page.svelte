


<script>

/*	
	import Amount_Field from '$lib/trinkets/Amount_Field/Trinket.svelte'
	
	const on_amount_change = () => {}
	
	<Amount_Field 
		on_change={ on_amount_change }
	/>
*/

import Amount_Field from '$lib/trinkets/Amount_Field/Trinket.svelte'
const on_amount_change = ({ 
	effects,
	actual_amount_of_Octas
}) => {
	if (effects.problems === "") {
		
	}
}

</script>

<div>
	<Amount_Field 
		on_change={ on_amount_change }
	/>
</div>