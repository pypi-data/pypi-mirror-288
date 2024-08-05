


<script>


//
//	Caution: Deprecated 
//
//	Fresh Version is: "$lib/trinkets/Code_Wall"
//

/*
	import UT_Stringified from '$lib/PTO/Transaction/Unsigned/Stringified.svelte'
	<UT_Stringified 
		unsigned_tx_stringified={ unsigned_tx_stringified }
	/>
*/

export let unsigned_tx_stringified = ""

console.log ({ unsigned_tx_stringified })

</script>


<div>
	<p
		unsigned_transaction_fiberized
		style="
			box-sizing: border-box;
			height: 100%; 
			font-size: 1em;
			white-space: break-spaces;
			word-wrap: break-word;
			text-align: left;
			background: none;
		"
	>
{ unsigned_tx_stringified }
	</p>
</div>