
/*
	import { parse_with_commas } from '$lib/taverns/numbers/parse_with_commas'
	parse_with_commas (1234512345)
*/

export const parse_with_commas = (number) => {
    let [ integerPart, decimalPart ] = number.toString().split('.');

	const parse_integer_part = (part) => {
        let result = '';
        let length = part.length;

        for (let i = length - 1; i >= 0; i--) {
            let position_from_end = length - i;
            result = part [i] + result;

            if (position_from_end % 5 === 0 && i !== 0) {
                result = ',' + result;
            }
        }

        return result;
    }


	//
	//	.123456 = .12345,6
	//	.1234567 = .1234567	
	//
	const parse_decimal_part = (part) => {
        if (!part) return '';

        // Add trailing zeros if less than 5 digits
        // part = part.padEnd(5, '0');

        // Format the decimal part with commas every 3 digits from the end
        let result = '';
        let length = part.length;

        for (let i = 0; i <= part.length - 1; i++) {
            let position_from_end = i + 1;

            result = result + part [i];

            if (position_from_end % 5 === 0 && i !== 0) {
                result = result + ',';
            }
        }

        return result;
    }

    // Parse both integer and decimal parts
    let parsed_integer_part = parse_integer_part (integerPart);
    let parsed_decimal_part = parse_decimal_part (decimalPart);
	if (parsed_decimal_part === '') {
		return parsed_integer_part;
	}

    // Combine integer and decimal parts
    return `${ parsed_integer_part }.${ parsed_decimal_part }`;
}

