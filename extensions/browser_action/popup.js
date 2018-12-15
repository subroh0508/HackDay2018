console.log('load popup.js');

document.getElementById('clear-tweet').addEventListener('click', event => {
    chrome.tabs.executeScript(null, {
        file: 'browser_action/clear.js',
    });
}, false);

document.getElementById('show-origin').addEventListener('click', event => {
    chrome.tabs.executeScript(null, {
        file: 'browser_action/show.js',
    });
}, false);
