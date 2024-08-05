






<script>

import Panel from '$lib/trinkets/panel/trinket.svelte'

import { AppRail, AppRailTile, AppRailAnchor } from '@skeletonlabs/skeleton';
import { parse_styles } from '$lib/trinkets/styles/parse'

const trends = {
	panel: {
		position: 'relative',
		display: 'inline-flex',
		'width': '33%', 
		'height': '150px',
		'align-items': 'center',
		'justify-content': 'center'
	},
	anchor: parse_styles ({
		position: 'absolute',
		height: '100%',
		width: '100%',
		
		display: 'flex',
		'align-items': 'center',
		'justify-content': 'center',
		'text-decoration': 'none',
		'text-align': 'center',
		'font-size': '2em'
	})
}

</script>

<style>

@media (max-width: 600px) {
    .latest-block-panel {
		flex-direction: column !important;
	}
}
a {
	line-height: 110%;
}

</style>

<svelte:head>
	<title>Technicians, Plays</title>
	<meta name="description" content="Technicians" />
</svelte:head>


<div>
	<div 
		style="padding: 25px 0"
		class="text-column"
	>
		<h1>Technicians</h1>
		
		<div style="height: 20px"></div>
		<p 
			style="text-align: center"
		>This region is for verifying and ensuring the health and continuity of the dapp.</p>
		<p
			style="text-align: center"
		>It's status checks that don't have an impact on the rest of the dapp.</p>
	</div>


	<section
		styles={{
			position: 'relative',
			display: 'grid',
			'width': '100%'
		}}
	>
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Net_Choices_with_Text"
				style="{ trends.anchor }"
			>
				Nets Choices with Text
			</a>
		</Panel>
	
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Amount_Field"
				style="{ trends.anchor }"
			>
				Amount Field
			</a>
		</Panel>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Hone_Focus"
				style="{ trends.anchor }"
			>
				Hone Focus
			</a>
		</Panel>
		
		
		
		<hr 
			class="!border-t-4"
			style="margin: 4px 0 12px"
		>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Address_Qualities"
				style="{ trends.anchor }"
			>
				Address Qualities with Address
			</a>
		</Panel>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Address_Qualities"
				style="{ trends.anchor }"
			>
				Address Qualities
			</a>
		</Panel>
		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Nets_Choices"
				style="{ trends.anchor }"
			>
				Nets Choices
			</a>
		</Panel>
		
		

		
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Consensus_Transactions"
				style="{ trends.anchor }"
			>
				Consensus Transactions
			</a>
		</Panel>
		<Panel 
			styles={ trends.panel }
		>
			<a 
				class="anchor" 
				href="/Technicians/Polytope"
				style="{ trends.anchor }"
			>
				Polytope
			</a>
		</Panel>
	</section>
</div>
