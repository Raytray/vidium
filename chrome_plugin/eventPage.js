// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.


// The onClicked callback function.

function onClickHandler(info, tab) {
	var myURL="";
	chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
		myURL=tabs[0].url;
		alert(myURL);
	});
	
};

chrome.contextMenus.onClicked.addListener(onClickHandler);

// Set up context menu tree at install time.
chrome.runtime.onInstalled.addListener(function() {
  // Create one test item for each context type.
  var contexts = ["page"];
  for (var i = 0; i < contexts.length; i++) {
    var context = contexts[i];
    var title = "Vidium";
    var id = chrome.contextMenus.create({"title": title, "contexts":[context],
                                         "id": "context" + context});
    console.log("'" + context + "' item:" + id);
  }
  
});
