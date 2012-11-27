#!/c/Python32/python

import string

# Four lists of blocks
unclassBlocks = []
jpegBlocks = []
pdfBlocks = []
wordBlocks = []


def run():
	# Populate first list
	for x in range(899):
		unclassBlocks.append("blockset/BLOCK{0:04}".format(x))
	
	first_pass()
	print_status()
	return

	second_pass()
	print_status()

	# read the contents of a block into an array of bytes
	file = open("blockset/BLOCK0000", 'rb')
	data = file.read()
	for x in data:
		print(data[x])
	print()



def first_pass():
	# We can't remove as we loop through, so keep list and remove after
	toRemove = []
	# Loop through every unclassified file
	for block in unclassBlocks:
		file = open(block, 'rb')
		data = file.read()
	
		# Looks for file signatures in blocks (header/footer)
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

		# PDF files
		elif data[0] == int("0x25", 16) and data[1] == int("0x50", 16) \
		     and data[2] == int("0x44", 16) and data[3] == int("0x46", 16):
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

		# If no sig is found, see if all bytes are within ascii printable range
		# This is a text block from a word file
		text = True
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
				text = False
				print("{:X}".format(int(byte)))
				break
		if text:
			print(block)
			wordBlocks.append(block)
			toRemove.append(block)
		file.close()
	
	# remove newly classified blocks
	for block in toRemove:
		unclassBlocks.remove(block)

	print("Pass 1 complete.")
	return

def second_pass():
	# Analysis based on entropy calculations
	print("Pass 2 complete.")
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
