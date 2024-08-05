



<script>

import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 


</script>

<svelte:head>
	<title>Relatives, Hints</title>
	<meta name="description" content="About this app" />
</svelte:head>



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
	>Preparing a <b>Keys Beacon</b></header>
	
	<div style="height: 1cm"></div>
	
	<hr />
	
	<div style="height: 0.5cm"></div>

	<p
		style="
			text-align: center;
		"
	>To prepare the <b>Keys Beacon</b>, it needs to be connected to the internet.</p>
	
	<div style="height: 0.5cm"></div>
	
	<p
		style="
			text-align: center;
		"
	>After preparation, the Keys Beacon should never be connected to the internet again<br /> unless the OS drive is wiped.</p>
	
	<div style="height: 0.5cm"></div>
	
	<p
		style="
			text-align: center;Move the docker image <b>oumuamua_v0.1.0.tar</b> that was created on Howl Beacon to the Keys Beacon with a drive, SD Card, Micro SD Card, etc..
		"
	><b>Ubuntu</b> is a good choice for the OS of the Keys Beacon.</p>
	
	<p
		style="
			text-align: center;
		"
	>
		<a 
			class="anchor" 
			href="https://ubuntu.com/download"
			target="_blank"
		>https://ubuntu.com/download</a>
	</p>

	
	<div style="height: 0.5cm"></div>
	
	<hr />

	<div style="height: 0.5cm"></div>

	<header>From Keys Beacon, while connected to the internet</header>

	<div style="height: 0.5cm"></div>

	<div class="card variant-soft p-4">
		<p>
			<span>Install the Docker Engine</span>
			<a 
				class="anchor" 
				href="https://docs.docker.com/engine/install/"
				target="_blank"
			>https://docs.docker.com/engine/install/</a>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>Install any other softwear necessary.</span>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>Disconnect the Keys Beacon from the internet (wifi), bluetooth, NFC, etc..</span>
		</p>
	</div>


	<div style="height: 0.5cm"></div>

	<div class="card variant-soft p-4">
		<p>
			<span>Move the docker image <b>oumuamua_v0.1.0.tar</b> that was created on a <b>Howl Beacon</b> to the <b>Keys Beacon</b> with a drive, SD Card, Micro SD Card, etc..</span>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>Load the docker container from the image.</span>
			<Code_Wall 
				context={ "OS" }
				text={[
					`docker load -i oumuamua_v0.1.0.tar`,
				]} 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>Load the docker container from the image.</span>
			<Code_Wall 
				context={ "OS" }
				text={[
					`docker run -it --name oumuamua_1 oumuamua:v0.1.0 /bin/bash`,
				]} 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>Start Oumuamua.</span>
			<Code_Wall 
				context={ "OS" }
				text={[
					`(cd /habitat && oumuamua ventures on)`,
				]} 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>To stop and remove the container,</span>
			<Code_Wall 
				context={ "OS" }
				text={[
					`docker stop oumuamua_1; docker remove oumuamua_1`
				]} 
			/>
		</p>
	</div>
</div>
