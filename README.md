FileRecovery
============

CprE 536 project to recover files from disk sector blocks lacking an inode.

Basic Idea:
Initialize a list containing all of the original blocks. Also initialize three empty lists, one for each file type.  As I identify each block as a type of file, remove that block from the original list and add it to one of the three file type lists. At the end print out each of the four lists.

Basic steps:
1)First Identify the plain text blocks.
2)Identify the blocks of the pdf/word that can be easily found by headers/footers and any file signatures.
3)Identify the blocks of the jpg that can be easily found by headers/footers and any file signatures.
4)Calculate the entropy of each of the remaining blocks.
5)If possible, look up average entropy values for each file type. Or test with a view files of each type that I have on my local machine.
6a)Compare the entropy of each block to the averages and classify based on comparison.
6b)If values can't be found, take the average of all the calculated entropies. Put blocks with entropy greater than average in one list and blocks with entropy less than average in the other list. Still need to figure out which file type is greater/less.


What I actually did:
First I opened about 10 of the blocks in a hex editor just to get an idea of what they looked like. What I immediately noticed was that one of the three types appeared to be plain text. I emailed the professor about this and he confirmed my thoughts.

I know one type is plain text, so now I need to figure out if the remaining two types are jpg, pdf, or word. I could email the professor about this also, but I'm guessing I can just start writing the toolkit to look for something specific to each of those files.

First program:
Read through each of the blocks looking for identifying criteria.
Plain text - look for a block with all values in the printable range.
Word -
Pdf -
Jpg -
Print out which types of files were found and which blocks contained the identifiable data.
