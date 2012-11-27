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

I know one type is plain text, so now I need to figure out if the remaining two types are jpg, pdf, or word. Or there could be another option, where the other three types are all included so there are really 4 types of files involved. I emailed the professor and TA this quesiton but they didn't reply, so I'm just going to write a function that tries to identify the headers of each file by the given type's magic numbers, and then see what I find.

I looked up the magic numbers online at http://en.wikipedia.org/wiki/Magic_number_(programming) and found what I needed. Obviously the plain text file doesn't have a magic number, so I'm hoping to identify that by the fact that all bytes will be legal ascii characters in the printable range.

First program:
Read through each of the blocks looking for identifying criteria.
Plain text - look for a block with all values in the printable range.
Word - doc file: hex "D0 CF 11 E0" docx file: hex "50 4B"
Pdf - hex "25 50 44 46"
Jpg - start: hex "FF D8" end: hex "FF D9"
Print out which types of files were found and which blocks contained the identifiable data.

I did this and what I found was interesting. I found headers from all three file types, and then I also found several plain text blocks, or so I thought. However, one block that I knew should be plain text "BLOCK0002" was not getting identified as such. After a little debugging, I realized the culprit was a single-quote that was hex 92. This isn't an ascii character, but instead a different single quote character that word uses. This made me think that what I was identifying as plain text documents might really just be blocks of text from a word file. My previous program informed me that the word documents were of the ".doc" variety, so I opened one of those up in the hex editor and sure enough the text portion appeared like plain text. My current assumption now is that there are only 3 types of files, so maybe the professor's reply to my email was actually wrong?

My plan is to expand my search for "plain text" files to include the characters for both the different single quote and also double quote marks that word uses, and then classify these blocks as word files. Then I'll continue on with the entropy analysis that I was originally planning on using.

I'm first manually finding all the obvious text files so I can verify that I'm identifying them all correctly. As i've been manually looking them over I've been wondering if I can identify all the word blocks by looking for certain signatures. If the entropy analysis doesn't work I may look over the 2003 word format spec to see if each chunk can be identified.

After a little poking around online I found this resource:
http://msdn.microsoft.com/en-us/library/cc313105(v=office.12).aspx
which includes a specification for the word file format. I think I will try using this to take out all the word blocks and possibly order them correctly.



