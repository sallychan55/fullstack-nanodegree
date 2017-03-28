var yelpInfo = function(id, callback) {
	var auth = {
		consumerKey: "E7Ei-EnnDNSEgSCPb67ggA",
		consumerSecret: "YtqM1W6gIxQvLEJJVtIgiC4B66A",
		accessToken: "V5hQpYA6D2vQtzlttnCDJ4eZEDW_lnnW",
		accessTokenSecret: "t_pgyw6PZ2ppP6nHHHBfnT7c1Uw",
		serviceProvider: {
			signatureMethod: "HMAC-SHA1"
		}
	};

	var accessor = {
		cunsumerSecret: auth.consumerSecret,
		tokenSecret: auth.accessTokenSecret
	};

	parameters = {
		oauth_consumer_key: auth.consumerKey,
		oauth_token: auth.accessToken,
		oauth_nonce: nonce_generate(),
        oauth_timestamp: Math.floor(Date.now() / 1000),
		oauth_signature_method: "HMAC-SHA1",
		oauth_version: '1.0',
		callback: "cb"
	};

	var yelp_url = 'https://api.yelp.com/v2/business/' + id;

	var encodedSignature = oauthSignature.generate('GET', yelp_url, 
						   	parameters, auth.consumerSecret, auth.accessTokenSecret);
    parameters.oauth_signature = encodedSignature;

	$.ajax({
		"url": yelp_url,
		"data": parameters,
		"cache": true,
		"dataType": "jsonp",
		"success": function(data, textStats, XMLHttpRequest) {
			console.log(data);
			callback(data);
		}
	}).fail(function(e){
		alert("faided to laod Yelp data!");
	});
};

function nonce_generate(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}