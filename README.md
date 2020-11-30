# Lyrics Math & Viz :)

Using kaggle lyrics data & DataMuse API <3

CREATE TABLE artists (
  artist_name VARCHAR PRIMARY KEY,
  kaggle_lyrics TEXT DEFAULT NULL,
  kaggle_lyrics_cleaned TEXT DEFAULT NULL
);

Also:

{
 word: <str> ,
 syllables: <int>
 rhyming_words: [<words>]
}
