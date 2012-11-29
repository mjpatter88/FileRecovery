#!/c/Python27/python

# In order for this to work properly, open the image in "Microsoft Office". 
# Then take a sceenshot, open it in paint.net, and determine the correct pixel values.
# Need to determine left, top, right, bottom of the whole image (if the window moved) and 
# also the row and column info of where the comparison needs to happen. 
# Maybe automate this if this process actually works?


import Image
import ImageGrab
import time

knownBlocks = []
newBlocks = []

def run():
	print "running"
	
	# get list of files from the list.txt file
	# files until the first line break are ones already ordered
	file = open("list.txt", 'r')
	stage = 1
	for line in file:
		if line[0] == '\n':
			stage = 2
			continue
		if stage == 1:
			knownBlocks.append(line[0:len(line)-1])	# remove \n from end of name
		if stage == 2:
			newBlocks.append(line[0:len(line)-1])	# remove \n from end of name
	file.close()
	# loop adding known data to the file and one "guess" block
	for newBlock in newBlocks:
		outFile = open("test.jpg", 'wb')
		# First add in the known correct data
		for block in knownBlocks:
			print("Known file: {}".format(block))
			newFile = open(block, 'rb')
			for byte in newFile:
				outFile.write(byte)
			newFile.close()
		# Then add one possible guess
		newFile = open(newBlock, 'rb')
		for byte in newFile:
			outFile.write(byte)
		newFile.close()
		outFile.flush()
		outFile.close()
		# wait long enough for Microsoft Office to update
		# could maybe wait shorter? do this for now
		time.sleep(0.1)
		# Take a screenshot and analyze it
		left = 22	
		top = 140	# change these if window moves
		right = 1021
		bottom = 876
		img = ImageGrab.grab((left, top, right, bottom))
		# could optimize  more by only grabbing the pixels i'm comparing?
		# do this if processing becomes an issue
		img.save("test2.jpg")

		left_col = 31	# hardcode until I find a better way
		top_row = 142
		bottom_row = 157

		# for now just do this once, don't loop
		break

	outFile.close()


if __name__ == "__main__":
	run()
