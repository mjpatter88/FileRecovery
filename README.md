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
and this one which is simpler and might have all the needed info:
www.openoffice.org/sc/compdocfileformat.pdf
These include a specification for the word file format. I think I will try using this to take out all the word blocks and possibly order them correctly.

Info about word .doc files:
Always start with hex: D0 CF 11 E0 A1 B1 1A E1

After looking over the documentation, word format is extremely complex and not even helpful in this instance. The documents describe how to visually create a word document from a given file, but now how to identify certain bits of the file. I may refer back to this in the future, but for now I'm going to have to continue on the previous track.

TODO: Problem: The end of pdfs gets detected as plain text. I think I'll have to detect these by looking for the specific pattern... otherwise they'll either be identified as plain text or the entropy will show them as plain text as well.

Maybe I can manually look at a few pdfs and a few docs and look for specific magic patterns... hmmm...

pdf's seem to use "<<" and ">>" quite often. I'll use double bracket combinations to identify pdfs. I do realize that a word document could contain double brackets, but I'm not sure if there's any other way around this rare mis-classification?

I could probably look for hex: 0A 3C 3C 20 or hex: 0A 3E 3E 0A or hex: 3C 3C 2F

Based on the headers, it's PDF 1.4, and Word .doc (2003)

Another interesting link:http://crucialsecurityblog.harris.com/tag/entropy/
Average enthropy of a jpeg is very high, close to 8!

At this point I think my approach will be the following:

1)Identify the header files.
2)Pull out pdf files: look for " n..0000" (beginning or end) or the hex above "<<" and ">>" and others. (The word doc doesn't have any double brackets in the text, so I should be safe searching for those."
3)Pull out the plain text files and try to get all the word files out (manually find identifying features.)
4)Do an entropy analysis to split the remaining ones between pdf and jpeg.
5)Maybe try to reorder them? Not sure how yet...
6)Another option would be to put everything in a jpg file and look for which chunks are image... can you do this?

For the word document I could just look up the text online and use that to do the ordering? That's what I'll do for step 3. I couldn't find the word document, but I found the pdf version.

Step 2 turned out to be pretty successful. I'm identifying 82 pdf blocks and I feel pretty good about all of them. I think there are more, but I'll have to find those through entropy analysis. I did have to hardcode in some special cases, because my search for "<<" and ">>" located a few files that I wasn't comfortable labeling as pdf files for sure. The brackets were in the middle of random data and could have just as easily been jpg blocks. I think I'm done with this pass of searching for pdf files based on signatures, at least for now.

Step 3 was also fairly successful. I started by looking files with every character printable. Then I looked through some of the .doc files in a hex editor, and realized many chunks had mostly either 00's, FF's, or printable characters, but clearly not all. I tried looking for a certain percentage of printable characters, and settled on over 50%. I first tried over 75%, but over 50% only found a few more blocks (confirming my assumptions). I manually checked each of the blocks and I feel pretty comfortable about labeling them as word blocks for now.

I do have a few reservations, which tend to make me think that accomplishing this goal with 100% confidence is almost impossible. I was looking through some .pdf files and .doc files I have on my pc, and I realized some blocks of each could be identical. Also pdfs can have jpgs embedded, etc, so really this classification is just a best guess. In theory and easily in practice you could face a 512 byte block that could be valid data for any of the three types of files.

That being said, I think so far my classifications are likely pretty accurate. At this point I'm identifying 82 pdf blocks, 282 word blocks, and the single jpg header block. That leaves 534 blocks unclassified. I'll now move on to doing entropy analysis and see what I find.

From reading a few resources, it seems the average entropy of a jpeg is around 7.6. I'm not sure what the average entropy of a pdf is, but I'm confident it will be lower. I'm hoping if I graph the results I'll be able to see a clear split between the two.

I'm using the following link for the basic formula:
http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html

However, I noticed it needlessly loops through the data n^2 times, so I made the simple optimization required to not do that. The entropy data looks good so far, now to graph the results.

Results are pretty good. There were 3 outliers around 4.0, and upon manual inspection I think those blocks are part of the word file. I'll tweak my algorithm to include them in that section. The rest of the files have entroy above 6 and almost all are near 7.5. This is good, but it also means it will be basically impossible to use this value to differentiate between jpg and pdf blocks.

The three files that need to be part of the word classification: 0027, 0629, 0880. Made a little tweak and now these three are identified as word blocks.

One idea is to take all the remaining files with entropy > 7.4 and concatenate them in a jpg file with the jpg header I already found. Maybe visually I can tell which blocks are part of the picture?

At a good stopping point for now. I still have 531 blocks left to classify, but I'm not exactly sure what to do with them. I am somewhat confident that all or most are either pdf blocks or jpg blocks, but the entropy is very similar in all but a couple. Other than the visual inspection possibility, I'm not real sure where to go from here. Maybe a good night sleep will help.

TODO: In the final report possibly include an "average entropy" stat for each of the sets of blocks I've grouped together. Even if they aren't exactly right I think it will show an impressive different between the three.

TODO: Also I just read online that jpgs tend to have a high number of zeros. Maybe if I ignore those in an entropy calculation I will see more separation? Doubtful but maybe worth a try?

Visual Inspection Attempt:
First step, put the jpg header into a jpg file: "cat BLOCK0785 > test.jpg"
I then opened it with the default image viewer on windows and it was better than expected. I saved the file as "JustHeader.jpg". I found out that the image is 1000 x 737 pixels, and the top left corner is filled in correctly.

Visual inspection might actually work! Although manually doing it will be painful... wonder if I can automate it?

I could automate it well using Python Image Library, but that doesn't support python 3.x. I think it's worth it though, and hopefully it won't be too painful to back port my code to python 2.7

Steps:
1) Download and install python 2.7
2) Change first line to point to that interpreter
3) Fix errors so I get consisten functionality between versions
4) Write code to automate finding next block.
	Idea: 
	Hardcode in the end of the previous block (pixel column/rows) (for now).
	Loop through each block adding it to the jpeg.
	Calculate the total difference in pixel values along that line.
		(After the first row compare with row above as well?)
	Block with least difference wins. (Inspect manually if this works)
	Then attempt to automate for every block needed in the picture.

After downloading and installing 2.7, I found out there would be several non-trivial changes due to the change in python's handling of file-reading. However, my thought is tat I can just write a new script that points to 2.7, put the list of unclassified files in a text document and go from there.






