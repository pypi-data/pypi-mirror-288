


const numerals = "0123456789"
export const Octas_string_is_permitted = (Octas_string) => {
	if (typeof Octas_string !== "string") {
		return "no"
	}
	
	if (Octas_string.length === 0) {
		return "no"
	}
	
	for (let E = 0; E < Octas_string.length; E++) {		
		if (numerals.includes (Octas_string [E]) !== true) {
			return "no"
		} 
	}
	
	return "yes"
}