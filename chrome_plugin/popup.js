var tok;
document.addEventListener('DOMContentLoaded', function(){
    chrome.identity.getAuthToken({ 'interactive': true }, function(token) {
        tok = JSON.stringify(token);
        console.log(tok);
    });
});
