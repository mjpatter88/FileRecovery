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
			print("Known file: {}".format(line[0:len(line)-1]))
		if stage == 2:
			newBlocks.append(line[0:len(line)-1])	# remove \n from end of name
	file.close()
	
	min = 1000000	# pick a number bigger than possible for now
	minBlock = None	# nothing for now

	# loop adding known data to the file and one "guess" block
	for newBlock in newBlocks:
		outFile = open("test.jpg", 'wb')
		# First add in the known correct data
		for block in knownBlocks:
			newFile = open(block, 'rb')
			for byte in newFile:
				outFile.write(byte)
			newFile.close()
		# Then add one possible guess
		print("New file: {}".format(newBlock))
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
		# img.save("test2.jpg")
		
		# Verify top left pixel is what is expected
		# otherwise it's a corrupt image file
		top_left_r = 227	
		top_left_g = 232	
		top_left_b = 235
		if img.getpixel((0,0)) != (227, 232, 235):
			print "Bad File"
			continue
		
		# pixels to compare
		# hardcode until I find a better way
		left_col = 31	# column of pixels to compare to column immediately right of it
		top_row = 0
		bottom_row = 15
		
		difference = 0
		for x in range(top_row, bottom_row+1):
			pix1 = img.getpixel((left_col, x))
			pix2 = img.getpixel((left_col+1, x))
			difference = difference + abs(pix1[0] - pix2[0]) \
			     + abs(pix1[1] - pix2[1]) + abs(pix1[2] - pix2[2])
		
		if difference < min:
			print "New min: {}".format(difference)
			min = difference
			minBlock = newBlock
	
	
	# print results
	print "Next file: {}".format(minBlock)
	# print reminder to add to known list
	
	# write knowns files plus new file to image

	# outFile.close()


if __name__ == "__main__":
	run()
