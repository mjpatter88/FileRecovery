#!/c/Python32/python

# Four lists of blocks
unclassBlocks = []
plainTextBlocks = []
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
	# Looks for file signatures in blocks (header/footer)

	# If no sig is found, see if all bytes are within ascii printable range
	# use string.printable
	pass

def second_pass():
	# Analysis based on entropy calculations
	pass

def calc_entropy():
	numTimes = []
	numTimes.append(2)
	numTimes.append(5)
	print("test", numTimes[0], numTimes[1])

def print_status():
	print("STATUS: ")
	print("There are {0} unclassified blocks.".format(len(unclassBlocks)))
	print("There are {0} plain text blocks.".format(len(plainTextBlocks)))
	print("There are {0} pdf blocks.".format(len(pdfBlocks)))
	print("There are {0} word blocks.".format(len(wordBlocks)))
	print("There are {0} jpeg blocks.".format(len(jpegBlocks)))
	

if __name__ == "__main__":
	run()
