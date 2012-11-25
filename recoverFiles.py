#!/c/Python32/python

# Four lists of blocks
unclassBlocks = []
plainTextBlockss = []
jpegBlocks = []
pdfBlocks = []
wordBlocks = []


def run():
	# Populate first list
	for x in range(899):
		unclassBlocks.append("blockset/BLOCK{0:04}".format(x))


	# read the contents of a block into an array of bytes
	file = open("blockset/BLOCK0000", 'rb')
	data = file.read()
	for x in data:
		print(data[x])
	print()



def first_pass():
	# Looks file signatures in blocks (header/footer)

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


if __name__ == "__main__":
	run()
