

//
//	import { string_from_Uint8Array } from '$lib/taverns/hexadecimal/string_from_Uint8Array'
//
//



export const string_from_Uint8Array = (uint8Array) => {	
	return Array.prototype.map.call (uint8Array, x => ('00' + x.toString (16)).slice (-2)).join ('').toUpperCase ()
}