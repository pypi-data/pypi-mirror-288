





/*
{
	"petition": {},
	"changes": [
		[ "path", "BigInt to string" ],
		[ "path", "Uint8Array to string" ], 
	]
}
*/
import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
import { has_field } from 'procedures/object/has_field'

import _cloneDeep from 'lodash/cloneDeep'
import _isEqual from 'lodash/isEqual'


function replaceBigIntWithString_ (obj) {
	const stack = [{ value: obj, path: '' }];
	const result = Array.isArray(obj) ? [] : {};

	while (stack.length) {
		const { value, path } = stack.pop();

		for (const key in value) {
			if (Object.hasOwn(value, key)) {
				const currentPath = path ? `${path}.${key}` : key;
				const item = value[key];

				if (typeof item === 'bigint') {
					console.log(`Path: ${currentPath}, Value: ${item}`);
					result[key] = item.toString();
				} 
				else if (typeof item === 'object' && item !== null) {
					stack.push({ value: item, path: currentPath });

					if (Array.isArray(item)) {
						result[key] = [];
					} 
					else {
						result[key] = {};
					}
				} 
				else {
					result[key] = item;
				}
			}
		}
	}

	return result;
}

const replace_v1 = (bracket) => {
	const fluctuations = []
	
	function replace_contents (obj, path = "") {
		console.info ("\n\nreplace_contents:", path, "\n\n")
		
		if (obj !== null && typeof obj === 'object') {
			for (const key in obj) {
				const this_path = path + "." + key;
				console.log ({ this_path })
				
				let contents = obj [key];
				
				// 
				// if (obj.hasOwnProperty (key)) {
				if (has_field (obj, key)) {
					if (typeof obj[key] === 'bigint') {
						// BigInt to string
						obj [ key ] = obj [ key ].toString ();	

						fluctuations.push ([
							this_path,
							"bigint"
						])
					} 
					else if (obj [key] instanceof Uint8Array) {
						obj [key] = string_from_Uint8Array (obj [key])
					
						fluctuations.push ([
							this_path,
							"Uint8Array"
						])
					
						console.log ({ obj })
					}
					else if (Array.isArray(obj[key])) {
						console.log ("array")
						
						// for (let O = 0; O < 
						
						// Recursively handle arrays
						obj [key] = obj [key].map (item => replace_contents (
							item, 
							path = this_path
						));
					} 
					else if (typeof obj [key] === 'object') {
						const this_path_ = this_path;
						const obj_ = obj;
						
						// Recursively handle nested objects
						replace_contents (
							obj [ key ],
							path = this_path
						);
						
						console.log ("done replacing contents of object", {
							this_path_,
							this_path,
							
							obj_,
							obj
						})
					}
				}
				
				console.log ("%", { obj })
			}
		}
		
		return obj;
	}
	
	const replaced = replace_contents (bracket)
	
	return {
		replaced,
		fluctuations
	}
}


const replace = (outer_bracket) => {
	const fluctuations = []
	const proceeds = {}
	
	function replace_contents (obj, path = "") {
		console.info ("\n\nreplace_contents:", path, obj, "\n\n")
		
		if (obj !== null && typeof obj === 'object') {
			for (const key in obj) {
				const this_path = path + "." + key;
				console.log ({ this_path, obj })
				
				// 
				// if (obj.hasOwnProperty (key)) {
				if (has_field (obj, key)) {
					if (typeof obj [key] === 'bigint') {
						// BigInt to string
						proceeds [ key ] = obj [ key ].toString ();	

						fluctuations.push ([
							this_path,
							"bigint"
						])
					} 
					else if (obj [key] instanceof Uint8Array) {
						proceeds [key] = string_from_Uint8Array (obj [key])
					
						fluctuations.push ([
							this_path,
							"Uint8Array"
						])
					
						console.log ({ obj })
					}
					else if (Array.isArray (obj [key])) {
						console.log ("array")
						
						// for (let O = 0; O < 
						
						// Recursively handle arrays
						proceeds [key] = obj [ key ].map (item => replace_contents (
							item, 
							path = this_path
						));
					} 
					else if (typeof obj [key] === 'object') {
						const this_path_ = this_path;
						const obj_ = _cloneDeep (obj);
						
						// Recursively handle nested objects
						proceeds [key] = replace_contents (
							_cloneDeep (obj [ key ]),
							path = this_path
						);

					}
				}
			}
		}
		
		return obj;
	}
	
	const replaced = replace_contents (outer_bracket)
	
	return {
		proceeds,
		fluctuations
	}
}

const transforms = {
	
}
export const pack = ({ bracket }) => {
	console.log ({ bracket })
	
	const bracket_clone = _cloneDeep (bracket)
	if (_isEqual (bracket_clone, bracket) !== true) {
		throw new Error ("cloning failed.")
	}
	
	const proceeds = replace (bracket_clone)
	
	console.log ({ proceeds })
	
	console.log (JSON.stringify (proceeds, null, 4))
	
	return proceeds;
}


export const unpack = () => {
	
}