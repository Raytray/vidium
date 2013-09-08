// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


// The onClicked callback function.

document.addEventListener('DOMContentLoaded', function(){
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
        var tok = token;
    });
});

function onClickHandler(info, tab) {
	var myURL="";
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
		myURL=tabs[0].url;
		chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
			var tok = JSON.stringify(token);
			console.log(tok);
			//STUFF
			
			var userURL = "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token="+tok;
			var userHttp = null;
			userHttp = new XMLHttpRequest();

			userHttp.onreadystatechange = function () {
				if(userHttp.readyState==4){
					//alert(userHttp.responseText);
					var userRes = JSON.parse(userHttp.responseText);
					var userId = userRes.user_id;
					//alert(userId);
				    var tags = prompt("Enter any tags separated by commas. (tag1, tag2)");
				    if (tags.length != 0) {
					tags = tags.split(", ")
					var tag_string = "&tags=" + tags.join("&tags=");
					var getURL = "http://vidium-raytray.rhcloud.com/api/store/?token="+userId+"&url="+myURL+tag_string;
					alert(getURL);
					var xmlHttp = null;
					xmlHttp = new XMLHttpRequest();
					xmlHttp.open( "GET", getURL, false );
					xmlHttp.send( null );
				    }
				    else {
					var tag_string = "";
					var getURL = "http://vidium-raytray.rhcloud.com/api/store/?token="+userId+"&url="+myURL+tag_string;
					alert(getURL);
					var xmlHttp = null;
					xmlHttp = new XMLHttpRequest();
					xmlHttp.open( "GET", getURL, false );
					xmlHttp.send( null );
				    }
				}
			}
			userHttp.open( "GET", userURL, true );
			userHttp.send( null );
			
			//STUFF
			
			
		});
	});
	
};

chrome.contextMenus.onClicked.addListener(onClickHandler);

// Set up context menu tree at install time.
chrome.runtime.onInstalled.addListener(function() {
  // Create one test item for each context type.
  var contexts = ["page"];
  for (var i = 0; i < contexts.length; i++) {
    var context = contexts[i];
    var title = "Add to Vidium";
    var id = chrome.contextMenus.create({"title": title, "contexts":[context],
                                         "id": "context" + context, "documentUrlPatterns":["*://www.youtube.com/*"]
					});
    console.log("'" + context + "' item:" + id);
  }
  
});
