




/*	
	import { unpack, pack } from './Logistics'
	const a_pack = pack ({ 
		bracket: transaction_petition_1 
	})
	const unpacked = unpack ({ 
		a_pack 
	})
*/

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
import { Uint8Array_from_string } from '$lib/taverns/hexadecimal/Uint8Array_from_string'

import { has_field } from 'procedures/object/has_field'

import _cloneDeep from 'lodash/cloneDeep'
import _isEqual from 'lodash/isEqual'
import _set from 'lodash/set'
import _get from 'lodash/get'


function replace_and_track(obj, path = '') {
	const changedPaths = [];

	function recurse(value, currentPath) {
		if (typeof value === 'bigint') {
			// console.log(`Replaced BigInt at path: ${currentPath}`);
			changedPaths.push ([
				currentPath,
				// currentPath.split ('.').filter (Boolean),
				"bigint"
			]);
			
			
			return value.toString();
		}

		if (value instanceof Uint8Array) {
			// console.log(`Replaced Uint8Array at path: ${currentPath}`);
			changedPaths.push ([
				currentPath,
				// currentPath.split ('.').filter (Boolean),
				"Uint8Array"
			]);
			
			return string_from_Uint8Array (value)
			
			// return Array.from (value);
		}

		if (Array.isArray (value)) {
			return value.map((item, index) => {
				const newPath = `${currentPath}[${index}]`;
				return recurse (item, newPath);
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

		return value;
	}

	const transformedObject = recurse (obj, path);
	return { 
		result: transformedObject, 
		paths: changedPaths 
	};
}

const transforms = {
	
}
export const pack = ({ bracket }) => {
	// console.log ({ bracket })
	
	const bracket_clone = _cloneDeep (bracket)
	if (_isEqual (bracket_clone, bracket) !== true) {
		throw new Error ("cloning failed.")
	}
	
	const proceeds = replace_and_track (bracket_clone)
	
	// console.log ({ proceeds })
	// console.log (JSON.stringify (proceeds, null, 4))
	
	return proceeds;
}


export const unpack = ({ a_pack }) => {
	const a_pack_clone = _cloneDeep (a_pack ["result"])
	
	const { result, paths } = a_pack;
	for (let E = 0; E < paths.length; E++) {
		const the_path = paths [E]
		const var_path = the_path [0]
		const kind = the_path [1]


		
		const content = _get (result, var_path, "")
		// console.log ({ kind, content, var_path })
		
		
		if (kind === "bigint") {
			_set (a_pack_clone, var_path, BigInt (content))
		}
		else if (kind === "Uint8Array") {
			_set (a_pack_clone, var_path, Uint8Array_from_string (content))
		}
		
		//_set (result, 
	}
	
	return a_pack_clone;
}