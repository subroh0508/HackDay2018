console.log('clear!');
var originContents = document.getElementsByClassName('origin-tweet-content');
var irasutoyaContents = document.getElementsByClassName('irasutoya-tweet');

for (var i = 0, originContent; originContent = originContents[i]; i++) {
    originContent.style.display = 'none';
}

for (var i = 0, irasutoyaContent; irasutoyaContent = irasutoyaContents[i]; i++) {
    irasutoyaContent.style.display = 'inline';
}
