# Lyrics Math & Viz <3

Using kaggle lyrics data :)

word -> DataMuse API -> PostgreSQL ARRAY/JSONB

{
 word: <str> ,
 syllables: <int>
 rhyming_words: [<words>]
}

=>

CREATE TABLE words (
  word VARCHAR PRIMARY KEY,
  syllables INTEGER DEFAULT NULL,
  rhyming_words VARCHAR[],
  datamuse_searched BOOL DEFAULT FALSE
 );


Artists -> SQLAlchemy -> PostgreSQL
ARTISTS
- artist_name
- songs[]
- words{}

SONGS
- song_name
- artist_name
- raw_lyrics

PUNCTUATION
- symbol_name
- by_artist{artist_name: 