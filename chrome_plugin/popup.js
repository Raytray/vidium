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
            var res = JSON.parse(xmlHttp.responseText);
            document.getElementById("result_box").innerHTML='<table>';

            for(var i=0; i<res.vids.length; i++){
                document.getElementById("result_box").innerHTML+='<tr><td><a href="' + res.vids[i].url + '"><img src="' + res.vids[i].thumb_url + '" width="320"></a></td></tr>';
            }
            document.getElementById("result_box").innerHTML+='</table>';
        }
        xmlHttp.open( "GET", getURL, true );
        xmlHttp.send( null );

    });

});
