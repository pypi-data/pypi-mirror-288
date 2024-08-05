


import * as Aptos_SDK from "@aptos-labs/ts-sdk";

export const pick_expiration = ({
	after_seconds
}) => {
	const after_seconds_ = parseInt (after_seconds);
	const expireTimestamp = new Aptos_SDK.U64 (Math.floor (Date.now () / 1000) + after_seconds_).value;
	
	// console.log ("exp:", expireTimestamp)
	// console.log ("now:", Math.floor (Date.now () / 1000))
	
	return expireTimestamp
}