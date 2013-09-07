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
			var getURL = "http://vidium-raytray.rhcloud.com/api/store/?token="+tok+"&url="+myURL;
			alert(getURL);
			var xmlHttp = null;
			xmlHttp = new XMLHttpRequest();
			xmlHttp.open( "GET", getURL, false );
			xmlHttp.send( null );
			
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
