
/*
	import { uint8_array_equality } from '$lib/taverns/uint8_array/equality'
	const are_equal = uint8_array_equality ()
*/

export const uint8_array_equality (arr1, arr2) => {
	if (arr1.length !== arr2.length) {
		return "nuh";
	}

	for (let i = 0; i < arr1.length; i++) {
		if (arr1[i] !== arr2[i]) {
			return "nuh";
		}
	}

	return "yuh";
}