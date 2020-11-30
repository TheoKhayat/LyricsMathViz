# Lyrics Math & Viz <3

Using kaggle lyrics data :)

word -> DataMuse API -> PostgreSQL ARRAY/JSONB

{
 word: <str> ,
 syllables: <int>
 rhyming_words: [<words>]
 datamuse_searched: <bool>
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