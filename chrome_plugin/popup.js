var tok;
document.addEventListener('DOMContentLoaded', function(){
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
        tok = JSON.stringify(token);
        //document.getElementById("result_box").innerHTML="syntax correct";
        console.log(tok);
        var getURL = "https://vidium-raytray.rhcloud.com/api/retrieve/?token=106598221661789754226";
        var xmlHttp = null;
        xmlHttp = new XMLHttpRequest();

        xmlHttp.onreadystatechange = function (readyStateEvent) {
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
        xmlHttp.open( "GET", getURL, true );
        xmlHttp.send( null );

    });

});
