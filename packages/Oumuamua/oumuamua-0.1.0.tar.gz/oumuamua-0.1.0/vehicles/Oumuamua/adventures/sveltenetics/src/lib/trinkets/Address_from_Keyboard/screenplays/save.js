


/*
	


*/

import { dump } from 'js-yaml';
import JSZip from 'jszip'

export const save_keys_directory = ({
	directory_name,
	hexadecimal_public_key,
	hexadecimal_address,
	hexadecimal_private_key
}) => {		
	function downloadYaml(yamlString, fileName) {
		console.log ({ window })
		
		const blob = new Blob([yamlString], { type: 'text/yaml' });
		const url = window.URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = fileName || 'document.yaml';
		document.body.appendChild(a);
		a.click();    
		window.URL.revokeObjectURL(url);
		document.body.removeChild(a);
	}
	
	const name = directory_name
	
	const zip = new JSZip ();
	
	console.log ("save_keys_directory", {
		hexadecimal_public_key,
		hexadecimal_private_key
	});
	
	const keys_dir = zip.folder (name);
	keys_dir.file (
		"Aptos.private.key.yaml",
		dump ({
			"Aptos": {
				"private key": {
					"format": "EEC 25519",
					"hexadecimal": hexadecimal_private_key
				}
			}
		},{
			quotingType: '"'
		})
	);
	
	keys_dir.file (
		"Aptos.public.yaml",
		dump ({
			"Aptos": {
				"address": {
					"hexadecimal": hexadecimal_address
				},
				"public key": {
					"format": "EEC 25519",
					"hexadecimal": hexadecimal_public_key
				}
			}
		},{
			quotingType: '"'
		})
	);
	
	zip.generateAsync({type:"blob"}).then(function(content) {
		const link = document.createElement('a');
		link.href = URL.createObjectURL(content);
		link.download = name + ".zip";
		link.click();
		URL.revokeObjectURL(link.href);
	});
	
	console.log ({ zip })
	
	return;

	// Usage
	downloadYaml (dump ({
		"private key": seed_hexadecimal
	}), 'Aptos.EEC448.private-key.yaml');
	
	downloadYaml (dump ({
		"private key": seed_hexadecimal
	}), 'Aptos.EEC448.public-key.yaml');
}