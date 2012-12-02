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
			#print("Known file: {}".format(line[0:len(line)-1]))
		if stage == 2:
			newBlocks.append(line[0:len(line)-1])	# remove \n from end of name
	file.close()
	
	x = 0
	while 1:
		# calc new coordinates
		# first make sure file has all known blocks in it
		outFile = open("test.jpg", 'wb')
		# First add in the known correct data
		for block in knownBlocks:
			newFile = open(block, 'rb')
			for byte in newFile:
				outFile.write(byte)
			newFile.close()
		outFile.flush()
		outFile.close()
		time.sleep(1)

		# Take a screenshot and analyze it
		left = 22	
		top = 140	# change these if window moves
		right = 1021
		bottom = 876
		img = ImageGrab.grab((left, top, right, bottom))
		for row in range(0, 735):
			pix = img.getpixel((998, row))
			if (abs(pix[0] - 128) < 5) and (abs(pix[1] - 128) < 5) \
			    and (abs(pix[2] - 128) < 5):
				break

		# starting at the right edge and moving left
		for col in range(998, 0, -1):
			pix = img.getpixel((col, row+5))
			if (abs(pix[0] - 128) > 5) or (abs(pix[1] - 128) > 5) \
			    or(abs(pix[2] - 128) > 15):
				break

		#time.sleep(10)
		print("Row: {}   Col: {}".format(row, col))

		#find next block
		find_next(row, col)
		

		#update list files
		file = open("list.txt", 'w')
		for block in knownBlocks:
			file.write(block)
			file.write("\n")

		file.write("\n")
		
		for block in newBlocks:
			file.write(block)
			file.write("\n")
		file.flush()
		file.close()

		#sleep just in case
		time.sleep(2)

		#for now break after 10
		x = x+1
		if x > 4:
			print("Done")
			break


def find_next(row, col):
	print "running"
	
	# get list of files from the list.txt file
	# files until the first line break are ones already ordered
	#file = open("list.txt", 'r')
	#stage = 1
	#for line in file:
	#	if line[0] == '\n':
	#		stage = 2
	#		continue
	#	if stage == 1:
	#		knownBlocks.append(line[0:len(line)-1])	# remove \n from end of name
	#		print("Known file: {}".format(line[0:len(line)-1]))
	#	if stage == 2:
	#		newBlocks.append(line[0:len(line)-1])	# remove \n from end of name
	#file.close()
	
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
		newFile = open(newBlock, 'rb')
		for byte in newFile:
			outFile.write(byte)
		newFile.close()
		outFile.flush()
		outFile.close()
		# wait long enough for Microsoft Office to update
		# could maybe wait shorter? do this for now
		time.sleep(0.3)
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
			print "{0}: Bad File".format(newBlock)
			continue
		
		# pixels to compare
		# hardcode until I find a better way
		# left_col = 783  # column of pixels to compare to column immediately right of it
		# top_row = 32
		# bottom_row = 47
		left_col = col
		top_row = row
		bottom_row = top_row+15

		# compare three colunms: the border between old and new, 
		# 8 pixels left of the border and 16 pixels left of the border
		difference = 0
		for x in range(top_row, bottom_row+1):
			
			pix1 = img.getpixel((left_col, x))
			pix2 = img.getpixel((left_col+1, x))
			difference = difference + abs(pix1[0] - pix2[0]) \
			     + abs(pix1[1] - pix2[1]) + abs(pix1[2] - pix2[2])
			
			if left_col-8 >= 0:
				pix3 = img.getpixel((left_col-8, x))
				pix4 = img.getpixel((left_col-7, x))
				difference = difference + abs(pix3[0] - pix4[0]) \
				     + abs(pix3[1] - pix4[1]) + abs(pix3[2] - pix4[2])

			if left_col-16 >= 0:
				pix5 = img.getpixel((left_col-16, x))
				pix6 = img.getpixel((left_col-15, x))
				difference = difference + abs(pix5[0] - pix6[0]) \
				     + abs(pix5[1] - pix6[1]) + abs(pix5[2] - pix6[2])
		difference = difference
		# if it's not the top row, we can compare top border too
		topDiff = 0
		if top_row != 0:
			for x in range(left_col+1, 998):
				# print("x:{}   (top_row-1):{}".format(x, top_row-1))
				pixTop = img.getpixel((x, top_row - 1))
				pixBottom = img.getpixel((x, top_row))
				if pixBottom == (128, 128, 128):
					break	# gray area reached
				topDiff = topDiff + abs(pixTop[0] - pixBottom[0]) \
					     + abs(pixTop[1] - pixBottom[1]) \
					     + abs(pixTop[2] - pixBottom[2])
			# Take the average for the top portion so longer sections don't lose
			# aka topDiff/x (really needs to be over distance x ranges
			if (x - (left_col+1)) != 0:
				topDiff = topDiff/(x - (left_col+1))
			difference = difference + topDiff

		print("{0}:{1}".format(newBlock, difference))
		if difference < min:
			print "New min: {}".format(difference)
			min = difference
			minBlock = newBlock
	
	# print results
	print "Next file: {}".format(minBlock)
	
	# write knowns files plus new file to image
	outFile = open("test.jpg", 'wb')
	# First add in the known correct data
	for block in knownBlocks:
		newFile = open(block, 'rb')
		for byte in newFile:
			outFile.write(byte)
		newFile.close()
	# Then add the newly determined next block
	newFile = open(minBlock, 'rb')
	for byte in newFile:
		outFile.write(byte)
	newFile.close()
	outFile.flush()
	outFile.close()

	knownBlocks.append(minBlock)
	newBlocks.remove(minBlock)
	return

if __name__ == "__main__":
	run()
