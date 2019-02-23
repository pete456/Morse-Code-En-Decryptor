# Morse Code Coverter
Encrypt English to Morse code, or decrypts Morse code to English

## Dependencies
* Python < 3

## Running
chmod u+x main.py [options] [type] file
./main.py
or
python main.py [options] [type] file

[options]
-h: prints this chunck of text.
-f: Uses custom file for morse code. Must be formatted with char,code. Defaults to morsesheet.csv.
-w: Character used to signify a space between words. Defaults to '/'.
-c: Character used to signify a new character. Defaults to a space.

[type]
-m: Converts Morsecode `file` to English.
-e: Converts English `file` to Morse.

## Tech overview
A binary search tree was used in order to convert a morse code character into an english character.