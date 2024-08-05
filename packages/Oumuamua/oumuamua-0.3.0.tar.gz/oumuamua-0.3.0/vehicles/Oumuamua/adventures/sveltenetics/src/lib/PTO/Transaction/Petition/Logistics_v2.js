





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


const replace = (outer_bracket) => {
	const fluctuations = []
	const proceeds = {}
	
	const replace_contents = (
		bracket, 
		path = ""
	) => {
		console.log ("replace:", { bracket, path })
		
		const is_bracket = bracket !== null && typeof bracket === 'object'
		if (is_bracket !== true) {
			// isn't a bracket
			return bracket;
		}
		
		for (const key in bracket) {
			if (has_field (bracket, key) !== true) {
				throw new Error ("The bracket doesn't have the key from the loop")
			}
			
			
			
			if (typeof bracket [key] === 'bigint') {
				// BigInt to string
				bracket [ key ] = bracket [ key ].toString ();	
				fluctuations.push ([
					this_path,
					"bigint"
				])
			} 
			else if (bracket [key] instanceof Uint8Array) {
				bracket [key] = string_from_Uint8Array (bracket [key])
			
				fluctuations.push ([
					this_path,
					"Uint8Array"
				])
			
				console.log ({ bracket })
			}
			else if (Array.isArray (bracket [key])) {
				console.log ("array")
				
				// for (let O = 0; O < bracket [key]; O++) {}
				
				// Recursively handle arrays
				bracket [key] = bracket [ key ].map (item => replace_contents (
					item, 
					path = this_path
				));
			} 
			else if (typeof bracket [key] === 'object') {
				console.log ("replace contents of:", key)
				
				
				
				
				let this_path = ""
				if (path === "") {
					this_path = key;
				}
				else {
					this_path = path + "." + key;
				}
				
				console.log ("//// nested object start ////", this_path)
					
				// Recursively handle nested objects
				replace_contents (
					bracket [ key ],
					path = this_path
				);
				
				console.log ("//// nested object end ////", this_path)
			}
		}
		
		return bracket;
	}
	
	const replaced = replace_contents (outer_bracket)
	
	return {
		outer_bracket,
		fluctuations
	}
}

function replaceAndTrack(obj, path = '') {
  const changedPaths = [];

  function recurse(value, currentPath) {
    if (typeof value === 'bigint') {
      console.log(`Replaced BigInt at path: ${currentPath}`);
      changedPaths.push(currentPath.split('.').filter(Boolean));
      return value.toString();
    }

    if (value instanceof Uint8Array) {
      console.log(`Replaced Uint8Array at path: ${currentPath}`);
      changedPaths.push(currentPath.split('.').filter(Boolean));
      return Array.from(value);
    }

    if (Array.isArray(value)) {
      return value.map((item, index) => {
        const newPath = `${currentPath}[${index}]`;
        return recurse(item, newPath);
      });
    }

    if (value !== null && typeof value === 'object') {
      const result = {};
      for (const key in value) {
        if (Object.hasOwn(value, key)) {
          const newPath = currentPath ? `${currentPath}.${key}` : key;
          result[key] = recurse(value[key], newPath);
        }
      }
      return result;
    }

    // Return value unchanged if it's neither BigInt, Uint8Array, object, nor array
    return value;
  }

  const transformedObject = recurse(obj, path);
  return { result: transformedObject, paths: changedPaths };
}

const transforms = {
	
}
export const pack = ({ bracket }) => {
	console.log ({ bracket })
	
	const bracket_clone = _cloneDeep (bracket)
	if (_isEqual (bracket_clone, bracket) !== true) {
		throw new Error ("cloning failed.")
	}
	
	const proceeds = replaceAndTrack (bracket_clone)
	
	console.log ({ proceeds })
	
	console.log (JSON.stringify (proceeds, null, 4))
	
	return proceeds;
}


export const unpack = () => {
	
}