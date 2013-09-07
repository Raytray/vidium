var tok;
document.addEventListener('DOMContentLoaded', function(){
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
        tok = JSON.stringify(token);
		//document.getElementById("result_box").innerHTML="syntax correct";
        console.log(tok);
		var getURL = "https://vidium-raytray.rhcloud.com/api/retrieve/?token="+tok;
		var xmlHttp = null;
		xmlHttp = new XMLHttpRequest();
		
		xmlHttp.onreadystatechange = function (readyStateEvent) {
		  //if (xmlHttp.readyState == 4) {
			//if (xmlHttp.status == 200) {
			document.getElementById("result_box").innerHTML=xmlHttp.responseText;
			//}
		  //}
		}
		xmlHttp.open( "GET", getURL, true );
		xmlHttp.send( null );
	   
    });

});
