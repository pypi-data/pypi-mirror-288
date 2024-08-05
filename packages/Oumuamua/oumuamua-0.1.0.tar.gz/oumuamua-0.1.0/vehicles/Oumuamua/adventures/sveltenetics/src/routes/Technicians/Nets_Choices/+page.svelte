

<script>


import Nets_Choices from '$lib/PTO/Nets/Choices.svelte'

let net_address = ""
let chain_id = ""
const on_change = ({ net, chain_id: _chain_id }) => {
	console.log ('on_change', { net, _chain_id })
	
	net_address = net [ "path" ]
	chain_id = _chain_id;
}

</script>


<div>
	<Nets_Choices
		on_change={ on_change }
	/>
	<p>{ net_address }</p>
	<p>{ chain_id }</p>
</div>