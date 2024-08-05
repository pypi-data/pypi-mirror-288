

import { has_field } from 'procedures/object/has_field'

export const verify_TP_AO = ({
	TP_AO
}) => {
	if (has_field (TP_AO, "rawTransaction") !== true) {
		throw new Error (`The "rawTransaction" was not found in the UT object.`)
	}
	const rawTransaction = TP_AO ["rawTransaction"]
	
	if (has_field (rawTransaction, "sender") !== true) {
		throw new Error (`The "rawTransaction.sender" was not found in the UT object.`)
	}
}