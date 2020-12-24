Python Test Task
Produce a Python script which analyzes all text files in a directory, counts the occurrences of all words across all files, and stores the results in an SQLite database.
The script will:
	•	accept the search directory as a command line argument
	•	perform a word count in all files in the directory (non-recursively: if the directory contains subdirectories, do not descend into them)
	•	count how many times each unique word occurs in all the files
	◦	words are delimited by one of or a combination of the following: [" ", ",", ".", os.linesep, ]
	•	creates or reuses an existing SQLite database in the search directory
	•	stores the word count in the SQLite database in the following format:
__________________
id | word | count
-----------------
 1 | hi   | 3
-----------------
 2 | yo   | 8
__________________

Bonus points for:
	•	adding unit tests where applicable
	•	reading the files concurrently
	•	general readability and reliability
	•	a code comment for each assumption made (e.g., "assuming the word count to be case insensitive", "assuming file sizes below 32GiB" etc)