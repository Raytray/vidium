document.addEventListener('DOMContentLoaded', function(){
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
        alert(JSON.stringify(token));
    });
});
