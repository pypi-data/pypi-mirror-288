

//
//	https://github.com/aptos-labs/aptos-ts-sdk/blob/687e00152cc139f406182186fcd05b082dd70639/src/api/aptosConfig.ts
//	https://github.com/search?q=repo%3Aaptos-labs%2Faptos-ts-sdk+fullnode%3A&type=code
//

/*
	const aptos = new Aptos_SDK.Aptos (new Aptos_SDK.AptosConfig ({		
		fullnode: net_path,
		network: Aptos_SDK.Network.CUSTOM
		// client: { provider: custom_client }
	}));
*/


const params_to_query_string = (params) => {
	const params_array = [];
	for (let key in params) {
		if (params [key] === undefined) {
			continue;
		}
		
		params_array.push (
			encodeURIComponent (key) + '=' + encodeURIComponent (params [key])
		)
	}
	return params_array.join ('&');
}

export async function provider (requestOptions) {
	const { params, method, url, headers, body } = requestOptions;
	
	const request = {
		headers: {
			...headers,
			customClient: true,
		},
		body: JSON.stringify (body),
		method
	};

	let path = url;
	console.info ({ path, params })
	
	const params_string = params_to_query_string (params);
	if (params) {
		path = `${ url }?${ params_string }`;
	}
	

	const response = await fetch (path, request);
	const data = await response.json();
	
	console.log ({ path, request, data })
	
	return {
		status: response.status,
		statusText: response.statusText,
		data,
		headers: response.headers,
		config: response,
		request
	};
}
