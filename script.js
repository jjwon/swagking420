var rgClient = require("rapgenius-js");
var fs = require("fs");


var lyricsSearchCb = function(err, lyricsAndExplanations) {
    if (err) {
      console.log("Error: " + err);
    } else {
      //Printing lyrics with section names
      var lyrics = lyricsAndExplanations.lyrics;
      console.log("Found lyrics for song [title=%s, main-artist=%s, featuring-artists=%s, producing-artists=%s]",
        lyrics.songTitle, lyrics.mainArtist, lyrics.featuringArtists, lyrics.producingArtists);

      fs.appendFileSync(artist + '.txt', lyrics.getFullLyrics(true));
    }
};

var searchCallback = function(err, artist) {
  if (err) {
    console.log("Error: " + err);
  } else {
    var songs = artist.popularSongs.concat(artist.songs);
    for (var i=0; i < songs.length; i++) {
      var link = songs[i].link.replace("rapgenius", "rap.genius")
      rgClient.searchLyricsAndExplanations(link, "rap", lyricsSearchCb);
    }
  }
}

var artist = process.argv[2];
console.log(artist);

rgClient.searchArtist(artist, "rap", searchCallback);
