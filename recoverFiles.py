#!/c/Python32/python

import string

# Four lists of blocks
unclassBlocks = []
jpegBlocks = []
pdfBlocks = []
wordBlocks = []


def run():
	# Populate first list with every file block
	for x in range(899):
		unclassBlocks.append("blockset/BLOCK{0:04}".format(x))
	
	first_pass()

	second_pass()

	third_pass()
	print_status()
	return

def first_pass():
	# Pull out the headers/footers that we can find by magic numbers
	# We can't remove as we loop through, so keep list and remove after
	toRemove = []
	# Loop through every unclassified file
	for block in unclassBlocks:
		file = open(block, 'rb')
		data = file.read()
	
		# WORD files (.doc)
		if data[0] == int("0xD0", 16) and data[1] == int("0xCF", 16) \
		   and data[2] == int("0x11", 16) and data[3] == int("0xE0", 16) \
		   and data[4] == int("0xA1", 16) and data[5] == int("0xB1", 16) \
		   and data[6] == int("0x1A", 16) and data[7] == int("E1", 16):
			wordBlocks.append(block)
			toRemove.append(block)
		
		# WORD files (.docx)
		elif data[0] == int("0x50", 16) and data[1] == int("0x4B", 16):
			wordBlocks.append(block)
			toRemove.append(block)

		# PDF files (header)
		elif data[0] == int("0x25", 16) and data[1] == int("0x50", 16) \
		     and data[2] == int("0x44", 16) and data[3] == int("0x46", 16):
			pdfBlocks.append(block)
			toRemove.append(block)
		
		# PDF files (footer)
		elif data[506] == int("0x25", 16) and data[507] == int("0x25", 16) \
		     and data[508] == int("0x45", 16) and data[509] == int("0x4F", 16) \
		     and data[510] == int("0x46", 16):
			pdfBlocks.append(block)
			toRemove.append(block)

		# JPEG files (header)
		elif data[0] == int("0xFF", 16) and data[1] == int("0xD8", 16):
			jpegBlocks.append(block)
			toRemove.append(block)

		# JPEG files (footer)
		elif data[510] == int("0xFF", 16) and data[511] == int("0xD9", 16):
			jpegBlocks.append(block)
			toRemove.append(block)
		file.close()
	
	# remove newly classified blocks
	for block in toRemove:
		unclassBlocks.remove(block)

	print("Pass 1 complete.")
	return

def second_pass():
	# Pull out the pdf blocks that can be found with signatures
	# It would likely be better to use regular expressions to do this, but this way should work too.

	# We can't remove as we loop through, so keep list and remove after
	toRemove = []
	# Loop through every unclassified file
	for block in unclassBlocks:
		file = open(block, 'rb')
		data = file.read()
		
		# There are 512 bytes in each "data" stream data[0] -> data[511]
		for x in range(0, 512):
			# Make sure we have enough bytes for the comparison
			if x < 506:
				# "n..0000" or "n .0000" or "f..0000"
				if (data[x] == int("0x6E", 16) and data[x+1] == int("0x0D", 16)) \
				   or (data[x] == int("0x6E", 16) and data[x+1] == int("0x0A", 16)) \
				   or (data[x] == int("0x66", 16) and data[x+1] == int("0x0D", 16)):
					if data[x+2] == int("0x0A", 16) and data[x+3] == int("0x30", 16) \
					   and data[x+4] == int("0x30", 16) and data[x+5] == int("0x30", 16) \
					   and data[x+6] == int("0x30", 16):
						pdfBlocks.append(block)
						toRemove.append(block)
						break	# once this block has been classified break

			# Look for double brackets
			# None in the pdf of the word document I found online, so I think it's safe to do this
			# at least for this assignment
			if x < 511:
				# just look for either type of double brackets
				if data[x] == int("0x3E", 16) and data[x+1] == int("0x3E", 16):
					# avoid files that I looked and maybe arent' pdfs
					if data[x+2] == int("0x57", 16) and data[x+3] == int("0x8F", 16) \
					   or data[x+2] == int("0x93", 16) and data[x+3] == int("0x17", 16) \
					   or data[x+2] == int("0xBC", 16) and data[x+3] == int("0x60", 16) \
					   or data[x+2] == int("0x5B", 16) and data[x+3] == int("0xCA", 16) \
					   or data[x+2] == int("0xC3", 16) and data[x+3] == int("0xF9", 16):
						break
					pdfBlocks.append(block)
					toRemove.append(block)
					break

				if data[x] == int("0x3C", 16) and data[x+1] == int("0x3C", 16):
					# avoid files that I looked and maybe arent' pdfs
					if data[x+2] == int("0x55", 16) and data[x+3] == int("0xB7", 16) \
					   or data[x+2] == int("0x26", 16) and data[x+3] == int("0x6F", 16) \
					   or data[x+2] == int("0x22", 16) and data[x+3] == int("0xE6", 16) \
					   or data[x+2] == int("0x77", 16) and data[x+3] == int("0x90", 16):
						break
					pdfBlocks.append(block)
					toRemove.append(block)
					break
		file.close()

	# remove newly classified blocks
	for block in toRemove:
		unclassBlocks.remove(block)

	print("Pass 2 complete.")
	return

def third_pass():
	# Pull out the word blocks by looking for plain text and manually finding identifying features

	# We can't remove as we loop through, so keep list and remove after
	toRemove = []
	# Loop through every unclassified file
	for block in unclassBlocks:
		file = open(block, 'rb')
		data = file.read()
		
		# See if over half of the bytes are within ascii printable range
		# If so, this is a text block from a word file
		text = True
		numPrintable = 512
		for byte in data:
			if string.printable.find(chr(byte)) == -1 \
			   and byte != int("0x92", 16) and byte != int("0x93", 16) \
			   and byte != int("0x97", 16) and byte != int("0x96", 16) \
			   and byte != int("0xB2", 16) and byte != int("0x91", 16) \
			   and byte != int("0xFF", 16) and byte != int("0x00", 16):
				# hex 92 is word's single quote, hex 93 is word's double quote
				# hex 96 and 97 are word's hyphens, hex B2 is words squared
				# hex 91 is word's inverse single quote
				# word docs also have chunks of 00's or FF's
				
				numPrintable = numPrintable - 1
		
		# Tried a few different values here, 50% seems pretty good
		if numPrintable > 512*0.50:
			# print(block)
			wordBlocks.append(block)
			toRemove.append(block)
	
	# remove newly classified blocks
	for block in toRemove:
		unclassBlocks.remove(block)

	print("Pass 3 complete.")
	return

def fourth_pass():
	# Do an enthropy analysis to split the remaining files between jpg and pdf
	return

def fifth_pass():
	# Possibly try to order blocks?
	return

def calc_entropy():
	numTimes = []
	numTimes.append(2)
	numTimes.append(5)
	print("test", numTimes[0], numTimes[1])

def print_status():
	print("STATUS: ")
	print("There are {0} unclassified blocks.".format(len(unclassBlocks)))
	print("There are {0} pdf blocks.".format(len(pdfBlocks)))
	if len(pdfBlocks) > 0:
		print(pdfBlocks)
	print("There are {0} word blocks.".format(len(wordBlocks)))
	if len(wordBlocks) > 0:
		print(wordBlocks)
	print("There are {0} jpeg blocks.".format(len(jpegBlocks)))
	if len(jpegBlocks) > 0:
		print(jpegBlocks)
	

if __name__ == "__main__":
	run()
