



#/
#
from Oumuamua._essence import retrieve_essence
from Oumuamua.adventures.sanique.utilities.generate_inventory_paths import generate_inventory_paths
#
#
import sanic
from sanic import Sanic
from sanic_ext import openapi
import sanic.response as sanic_response
from sanic_limiter import Limiter, get_remote_address
#
#
import json
from os.path import exists, dirname, normpath, join
from urllib.parse import unquote
import threading
import time
from fractions import Fraction
#
#\


from Oumuamua.features.pecuniary.APT_to_Octas import convert_APT_to_Octas
from Oumuamua.features.pecuniary.Octas_to_APT import convert_Octas_to_APT



def consent_form (packet):
	return f"""
<html>
<head></head>
<body
	style="
		display: flex;
		justify-content: center;
		align-content: center;
		flex-direction: column;
	
		margin: 0;
		padding: 0;
		
		height: 100vh;
		width: 100vw;
		
		overflow-y: scroll;
		
		background: #49F;
	"
>
	<main
		style="
			margin: 0 auto;
			max-width: 10cm;
			height: fit-content;
			
			padding: 1cm;
			border-radius: 1cm;
			
			background: #FFF;
		"
	>
		<header
			style="
				font-size: 1.4em;
				text-align: center;
			"
		>Consent Form</header>
		
		<div style="height: 12px"></div>
		
		<p>For an action with this trinket to be consensual, the party that plays the action must take full responsibility for the action and thus not hold the trinket builders responsible for the action.</p>
		
		<div style="height: 12px"></div>
		
		<p>Once open, it is the responsibility of the consenting party to protect the web browser from interlopers.</p>
		
		<div style="height: 12px"></div>
		
		<p>This trinket requires saving info to browser local storage.</p>
		
		<div style="height: 12px"></div>
		
		<button
			style="
				
			"
		>Consent</button>
	</main>
</body>	
	"""

def guest_regions (vue_regions_packet):
	essence = retrieve_essence ()
	
	
	##/
	build_path = essence ["sveltnetics"] ["build_path"];
	the_index = build_path + "/index.html"
	the_assets = build_path + "/assets"
	
	front_inventory_paths = generate_inventory_paths (build_path)
	for front_path in front_inventory_paths:
		print ("front_path:", front_path)
		pass;
	##\
		
	
	app = vue_regions_packet ["app"]
	
	guest_addresses = sanic.Blueprint ("guest", url_prefix = "/")
	app.blueprint (guest_addresses)
	
	
	@guest_addresses.route ("/math/APT_to_Octas", methods=["PATCH"])
	async def address_APT_to_Octas (request):
		try:
			data = request.json
			
			AO_conversion = convert_APT_to_Octas ({
				"APT": data ["APT"]
			})
			if (AO_conversion ["victory"] != "yes"):
				return sanic_response.json ({
					"victory": "no",
					"note": AO_conversion ["note"]
				}, status = 600)
				
			return sanic_response.json ({
				"victory": "yes",
				"Octas": AO_conversion ["Octas"]
			}, status = 200)
			
		except Exception as E:
			return sanic_response.json ({
				"victory": "no",
				"note": "An exception occurred: " + str (E)
			}, status = 600)
		
		
	@guest_addresses.route ("/math/Octas_to_APT",methods=["PATCH"])
	async def address_Octas_to_APT (request):
		try:
			data = request.json
			
			OA_conversion = convert_Octas_to_APT ({
				"Octas": data ["Octas"]
			})
			if (OA_conversion ["victory"] != "yes"):
				return sanic_response.json ({
					"victory": "no",
					"note": OA_conversion ["note"]
				}, status = 600)
				
			return sanic_response.json ({
				"victory": "yes",
				"Octas": OA_conversion ["Octas"]
			}, status = 200)
			
		except Exception as E:
			return sanic_response.json ({
				"victory": "no",
				"note": "An exception occurred: " + str (E)
			}, status = 600)
	
	
	
	def check_consent ():	
		return;
	
	@guest_addresses.route ("/")
	async def home (request):
		cookies = request.cookies;
		
		if 'consent' in cookies:
			if cookies ["consent"] == "yes":
				return await sanic_response.file (the_index)
		
		consent_form_HTML = consent_form ({})
		
		return sanic_response.raw (
			consent_form_HTML, 
			content_type = "text/html",
			headers = {}
		)
		

	@guest_addresses.route("/<path:path>")
	async def assets_route (request, path):
		the_path = False
		
		print ()
		print ("path:", the_path)
		
		try:
			the_path = f"{ path }"
			print ("the_path:", the_path)
			
			if (the_path in front_inventory_paths):
				content_type = front_inventory_paths [ the_path ] ["mime"]
				content = front_inventory_paths [ the_path ] ["content"]
				
				print ('found:', the_path)
				print ('content_type:', content_type)
				
				return sanic_response.raw (
					content, 
					content_type = content_type,
					headers = {
						"Custom-Header-1": "custom",
						"Cache-Control": "private, max-age=31536000",
						#"Expires": "0"
					}
				)
				
		except Exception as E:
			print ("E:", E)
		
			return sanic_response.json ({
				"note": "An anomaly occurred while processing.",
				"the_path": the_path
			}, status = 600)
			
		return await sanic_response.file (the_index)


	