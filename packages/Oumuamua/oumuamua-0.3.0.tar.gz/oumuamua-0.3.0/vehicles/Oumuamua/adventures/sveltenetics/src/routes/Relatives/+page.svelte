
<script>

//
import Building_Docker_Image from './Hints/Building_Docker_Image/Trinket.svelte'
import Docker_Image_Pull from './Hints/Docker_Image_Pull/Trinket.svelte'
//
import Building_Keys_Beacon from './Hints/Building_Keys_Beacon/Trinket.svelte'
//

import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
import { TabGroup, Tab, TabAnchor } from '@skeletonlabs/skeleton';	
	
let tabSet = 0

</script>

<svelte:head>
	<title>Relatives, Hints</title>
	<meta name="description" content="About this app" />
</svelte:head>


<div 
	style="
		display: flex;
		flex: 0.6;
		justify-content: center;
		flex-direction: column;
		min-height: 100%;
	"
>
	<div
		class="card p-4"
		style="
			padding: 1cm;
			width: 100%;
		"
	>
		<header
			style="
				font-size: 2.5em;
				text-align: center;
			"
		>Relatives, Hints</header>
		
		<div style="height: 1cm"></div>
		
		<p style="text-align: center">
			This dapp has a QR code interface for communicating with the consensus.
		</p>
		
		<div style="height: 0.5cm"></div>
		
		<p style="text-align: center">
			Thus, "Relatives" activities should happen on a <b>Keys Beacon</b> with limited connectivity to the ICANN/IANA Lagrange Neural Lattice.
		</p>
	</div>
	
	<div style="height: 1cm"></div>
	
	<div
		class="card p-4"
		style="
			padding: 1cm;
			width: 100%;
		"
	>
		<header
			style="
				font-size: 2.5em;
				text-align: center;
			"
		>Beacons</header>
		
		<div style="height: 0.5cm"></div>

		<p style="text-align: center">
			Beacon is another name for laptop, computer, machine, phone, etc.
		</p>

		<div style="height: 0.5cm"></div>
		
		<div
			class="card variant-soft p-4"
		>
			<header
				style="
					font-size: 1.5em;
					font-weight: bold;
					text-align: center;
				"
			>Howl Beacons</header>

			<div style="height: 0.2cm"></div>
			
			<hr class="!border-t-4" />
			
			<div style="height: 0.2cm"></div>			
			
			<p
				style="
					text-align: center;
				"
			>
				<span><b>Howl Beacons</b> should be connected to the public lattices,<br /></span>
				<span>such as ethernet, wifi, bluetooth, NFC, towers, satellites, etc.</span>
			</p>
			
			<div style="height: 0.25cm"></div>

			<hr class="!border-t-2" />

			<div style="height: 0.25cm"></div>
			
			<p
				style="
					text-align: center;
				"
			>This is where <b>Aptos Moves</b> are formulated.</p>
		</div>

		<div style="height: 0.5cm"></div>

		<div
			class="card variant-soft p-4"
		>
			<header
				style="
					font-size: 1.5em;
					font-weight: bold;
					text-align: center;
				"
			>Keys Beacons</header>

			<div style="height: 0.2cm"></div>
			
			<hr class="!border-t-4" />
			
			<div style="height: 0.2cm"></div>
			
			
			<p
				style="
					text-align: center;
					display: block;
				"
			>A <b>Keys Beacon</b> should not be connected to public lattices, <br/>except with restrictive communications such as:</p>
			
			<div style="height: 0.2cm"></div>
			
			<p
				style="
					text-align: center;
				"
			><b>QR Code Screen</b> to <b>QR Code Scanner</b></p>
			
			<div style="height: 0.25cm"></div>
			
			<hr class="!border-t-2" />

			<div style="height: 0.25cm"></div>

			<p>
				<span
					style="
						display: block;
						text-align: center;
					"
				><b>Keys Beacons</b> might need to be connected to the internet during the preliminary installation.</span>

				<span
					style="
						display: block;
						text-align: center;
					"
				>If this is the mode, OS modifications should happen on a fresh drive, and then the previous drive should be wiped on a <b>Keys Beacon</b>.<span>
			</p>
			
			<div style="height: 0.25cm"></div>

			<hr class="!border-t-2" />
			
			<div style="height: 0.25cm"></div>

			<p
				style="
					text-align: center;
				"
			>This is where <b>Aptos Addresses</b> are found,</p>
			<p
				style="
					text-align: center;
				"
			>and where <b>Aptos Moves</b> are signed.</p>
		</div>
	</div>
	
	<div style="height: 1cm"></div>
	
	<div
		class="card p-4"
		style="
			padding: 1cm;
			width: 100%;
		"
	>
		<header
			style="
				font-size: 2.5em;
				text-align: center;
			"
		>Installation, Docker</header>
		
		
		<div style="height: 1cm"></div>
		
		<p style="text-align: center">
			<b>Docker Containers</b> are operating systems that exist within another OS.
		</p>
		
		<div style="height: 0.5cm"></div>

		<p style="text-align: center">
			<b>Docker Images</b> are the kits that <b>Docker Containers</b> can be created from.
		</p>
	
		<div style="height: 1cm"></div>

		<div
			class="card variant-soft p-4"
			style="
				padding: 1cm;
				width: 100%;
			"
		>
			<div style="height: 0.5cm"></div>
			
			<header
				style="
					text-align: center;
					font-size: 2em;
				"
			>Preparing a Docker Image</header>
			
			<div style="height: 1cm"></div>
		
			<p
				style="
					text-align: center;
				"
			>A docker image with Oumuamua can be sent from<br /> a <b>Howl Beacon</b> to a <b>Keys Beacon</b> with USB storage hardwear.</p>
		
			<div style="height: 0.5cm"></div>
		
			<p
				style="
					text-align: center;
				"
			>Choices indicates various methods of accomplishing this.</p>
		
			<div style="height: 1cm"></div>	
		
			<TabGroup justify="justify-center">
				<Tab bind:group={tabSet} name="tab1" value={0}>
					<span>Choice 1</span>
				</Tab>
				<Tab bind:group={tabSet} name="tab2" value={1}>
					<span>Choice 2</span>
				</Tab>
				
				<svelte:fragment slot="panel">
					{#if tabSet === 0}
						<Building_Docker_Image />
					{:else if tabSet === 1}
						<Docker_Image_Pull />
					{/if}
				</svelte:fragment>
			</TabGroup>
		</div>
	
		<div style="height: 0.5cm"></div>
		
		<Building_Keys_Beacon />
	</div>
	
	<div style="height: 1cm"></div>
	
	<div
		class="card p-4"
		style="
			padding: 1cm;
			width: 100%;
		"
	>
		<h1>Installation, ISO</h1>
		
		<div style="height: 1cm"></div>

		<p style="text-align: center">
			This is not possible at the moment.
		</p>
	</div>
	
	<div style="height: 5cm"></div>
</div>