
<script>

import Code_Wall from '$lib/trinkets/Code_Wall/Trinket.svelte' 
let tabSet = 0

</script>

<div 
	style="
		display: flex;
		flex: 0.6;
		justify-content: center;
		flex-direction: column;
		min-height: 100%;
	"
>
	<div style="height: 0.5cm"></div>

	<header
		style="
			text-align: center;
			font-size: 2em;
		"
	>Choice 1</header>

	<div style="height: 0.5cm"></div>

	<header 
		style="
			text-align: center;
		"
	>Creating a custom Docker Image.</header>
	
	<div style="height: 0.5cm"></div>

	<hr />

	<div style="height: 0.5cm"></div>

	<header>From the Howl Beacon</header>

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
			<span>Pull the Ubuntu Image</span>
			<Code_Wall 
				context={ "OS" }
				text={ "docker pull ubuntu" } 
			/>
		</p>
	</div>

	<div style="height: 0.5cm"></div>


	<div class="card variant-soft p-4">
		<p>
			<span>Open a container from the "Ubuntu" image</span>
			<Code_Wall 
				context={ "OS" }
				text={ "docker run --name oamuamua -it ubuntu" } 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>On the "Ubuntu" container, install "python", "pip", and "python venv".</span>
			<Code_Wall 
				context={ "Docker Ubuntu Container" }
				text={
					[ 
						`apt update`,
						`apt install python3-pip -y`,
						`apt install python3.12-venv`	
					].join ('\n')
				} 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>On the "Ubuntu" container, create the Oumuamua venv.</span>
			<Code_Wall 
				context={ "Docker Ubuntu Container" }
				text={
					[ 
						`mkdir /habitat`,
						`cd /habitat`,
						`python3 -m venv v_env`,
						`. v_env/bin/activate`
					].join ('\n')
				} 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">	
		<p>
			<span>On the "Ubuntu" container, install Oumuamua.</span>
		</p>	

		<div style="height: 0.1cm"></div>

		<div>
			<a 
				class="anchor" 
				href="https://pypi.org/project/Oumuamua"
				target="_blank"
			>https://pypi.org/project/Oumuamua</a>
		</div>
		
		<div style="height: 0.2cm"></div>
		
		<p>
			<Code_Wall 
				context={ "Docker Ubuntu Container" }
				text={
					[ 
						`pip install Oumuamua`,
						`echo "essence = {}" > Oumuamua_essence.py`
					].join ('\n')
				} 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<p>
			<span>On the "Ubuntu" container, Exit the "Ubuntu" container</span>
			<Code_Wall 
				context={ "Docker Ubuntu Container" }
				text={
					[ 
						`exit`
					].join ('\n')
				} 
			/>
		</p>
	</div>
	
	<div style="height: 0.5cm"></div>
	
	<div class="card variant-soft p-4">
		<article>
			<p>On the OS, create <b>oumuamua_v0.1.0.tar</b>, the Oumuamua Docker Image.</p>
			<Code_Wall 
				context={ "OS" }
				text={
					[ 
						`docker commit oumuamua oumuamua:v0.1.0`,
						`docker save -o oumuamua_v0.1.0.tar oumuamua:v0.1.0`
					].join ('\n')
				} 
			/>
		</article>
	</div>
</div>

