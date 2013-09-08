var tok;
document.addEventListener('DOMContentLoaded', function(){
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
        tok = JSON.stringify(token);
        //document.getElementById("result_box").innerHTML="syntax correct";
        console.log(tok);
        
		var userURL = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+tok;
		//alert(userURL);
		var userHttp = null;
		userHttp = new XMLHttpRequest();
		
		userHttp.onreadystatechange = function () {
			if(userHttp.readyState==4){
				var userRes = JSON.parse(userHttp.responseText);
				var userId = userRes.user_id;
				//alert(userId);		
				var getURL = "https://vidium-raytray.rhcloud.com/api/retrieve/?token="+userId;
				//alert(getURL);
				var xmlHttp = null;
				xmlHttp = new XMLHttpRequest();

				xmlHttp.onreadystatechange = function () {
					if(xmlHttp.readyState==4){
						
						var res = JSON.parse(xmlHttp.responseText);

						if(res.vids == "User not found"){
							document.getElementById("result_box").innerHTML = "ADD SOME LINKS!";
						}
						else{
							console.log(JSON.stringify(res));
							console.log(res.vids.length);
							document.getElementById("result_box").innerHTML='<table>';

							for(var i=0; i<res.vids.length; i++){ target="_blank"
								document.getElementById("result_box").innerHTML+='<tr><td><a href="' + res.vids[i].url + '" target="_blank"><img src="' + res.vids[i].thumb_url + '" width="300"></a></td></tr>';
							}
							document.getElementById("result_box").innerHTML+='</table>';
						}
					}
				}
				xmlHttp.open( "GET", getURL, true );
				xmlHttp.send( null );
			}
		}
		userHttp.open( "GET", userURL, true );
		userHttp.send( null );
		
    });

});
