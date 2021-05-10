import cv2 as cv
import numpy as np
import sys






#input and load images
debug = "false";
if len(sys.argv) != 4 or len(sys.argv) == 5 :
	if len(sys.argv) == 5 :
		if sys.argv[4] != "debug" :
			sys.exit("Pass 3 arguments, input image name, modifier image name, output name")
		elif sys.argv[4] == "debug":
			debug = "true"
	else :
		sys.exit("Pass 3 arguments, input image name, modifier image name, output name")

input = cv.imread(sys.argv[1])
if input is None : 
	sys.exit("Could not read input")
in_h, in_w, in_c = input.shape

modif = cv.imread(sys.argv[2])
if modif is None :
	sys.exit("Could not read modifier")
mod_h, mod_w, mod_c = modif.shape






#resize images to same res

if debug == "true" :
	print("Initial resolution input: " + str(in_w) + " by " + str(in_h))
	print("Initial resolution modif: " + str(mod_w) + " by " + str(mod_h))

if in_h > mod_h and in_w > mod_w :
	input = cv.resize(input, (mod_w, mod_h))
	final_w = mod_w
	final_h = mod_h
elif mod_h > in_h and mod_w > in_w :
	modif = cv.resize(modif, (in_w, in_h))
	final_w = in_w
	final_h = in_h
else :
	if in_h < mod_h :
		cram_h = in_h
	else :
		cram_h = mod_h
	if in_w < mod_w :
		cram_w = in_w
	else :
		cram_w = mod_w
	input = cv.resize(input, (cram_w, cram_h))
	modif = cv.resize(modif, (cram_w, cram_h))
	final_w = cram_w
	final_h = cram_h

if debug == "true" :
	print("Final resolution: " + str(final_w) + " by " + str(final_h))
	cv.imshow("Raw Input", input)
	cv.waitKey(0)






#brightness detect and modification

bsum_inp = 0
for x in range(0,final_h) :
	for y in range(0,final_w) :
		bsum_inp += input.item(x,y,0)
		bsum_inp += input.item(x,y,1)
		bsum_inp += input.item(x,y,2)
bsum_inp = bsum_inp/3
bsum_inp = int(bsum_inp)

bsum_mod = 0
for x in range(0,final_h) :
	for y in range(0,final_w) :
		bsum_mod += modif.item(x,y,0)
		bsum_mod += modif.item(x,y,1)
		bsum_mod += modif.item(x,y,2)
bsum_mod = bsum_mod/3
bsum_mod = int(bsum_mod)


pxchange = (bsum_inp - bsum_mod) / input.size
pxchange = int(pxchange)

if debug == "true" :
	print("Brightness sum avg input: " + str(bsum_inp))
	print("Brightness sum avg modif: " + str(bsum_mod))
	print("Value change per pixel  : " + str(pxchange))

for x in range(0,final_h) :
	for y in range(0,final_w) :
		if input.item(x,y,0)+pxchange <= 255 and input.item(x,y,0)+pxchange >= 0 :
			input.itemset((x,y,0),input.item(x,y,0)+pxchange)
		elif input.item(x,y,0)+pxchange > 255:
			input.itemset((x,y,0),255)
		else :
			input.itemset((x,y,0),0)

		if input.item(x,y,1)+pxchange <= 255 and input.item(x,y,1)+pxchange >= 0 :
			input.itemset((x,y,1),input.item(x,y,1)+pxchange)
		elif input.item(x,y,1)+pxchange > 255:
			input.itemset((x,y,1),255)
		else :
			input.itemset((x,y,1),0)

		if input.item(x,y,2)+pxchange <= 255 and input.item(x,y,2)+pxchange >= 0 :
			input.itemset((x,y,2),input.item(x,y,2)+pxchange)
		elif input.item(x,y,2)+pxchange > 255:
			input.itemset((x,y,2),255)
		else :
			input.itemset((x,y,2),0)

if debug == "true" :
	cv.imshow("Brightness change applied", input)
	cv.waitKey(0)





#individual color "brightness" / hue?
sum_inp1 = 0
sum_inp2 = 0
sum_inp3 = 0
for x in range(0,final_h) :
	for y in range(0,final_w) :
		sum_inp1 += input.item(x,y,0)
		sum_inp2 += input.item(x,y,1)
		sum_inp3 += input.item(x,y,2)
sum_inp1 = sum_inp1/3
sum_inp2 = sum_inp2/3
sum_inp3 = sum_inp3/3
sum_inp1 = int(sum_inp1)
sum_inp2 = int(sum_inp2)
sum_inp3 = int(sum_inp3)

sum_mod1 = 0
sum_mod2 = 0
sum_mod3 = 0
for x in range(0,final_h) :
	for y in range(0,final_w) :
		sum_mod1 += modif.item(x,y,0)
		sum_mod2 += modif.item(x,y,1)
		sum_mod3 += modif.item(x,y,2)
sum_mod1 = sum_mod1/3
sum_mod2 = sum_mod2/3
sum_mod3 = sum_mod3/3
sum_mod1 = int(sum_mod1)
sum_mod2 = int(sum_mod2)
sum_mod3 = int(sum_mod3)

pxchange1 = (sum_inp1 - sum_mod1) / input.size
pxchange1 = int(pxchange1)*-8
pxchange2 = (sum_inp2 - sum_mod2) / input.size
pxchange2 = int(pxchange2)*-8
pxchange3 = (sum_inp3 - sum_mod3) / input.size
pxchange3 = int(pxchange3)*-8

if debug == "true" :
	print("Channel 1 sum avg input: " + str(sum_inp1))
	print("Channel 1 sum avg modif: " + str(sum_mod1))
	print("Channel 2 sum avg input: " + str(sum_inp2))
	print("Channel 2 sum avg modif: " + str(sum_mod2))
	print("Channel 3 sum avg input: " + str(sum_inp3))
	print("Channel 3 sum avg modif: " + str(sum_mod3))

	print("Value change per pixel channel 1 : " + str(pxchange1))
	print("Value change per pixel channel 2 : " + str(pxchange2))
	print("Value change per pixel channel 3 : " + str(pxchange3))

for x in range(0,final_h) :
	for y in range(0,final_w) :
		if input.item(x,y,0)+pxchange1 <= 255 and input.item(x,y,0)+pxchange1 >= 0 :
			input.itemset((x,y,0),input.item(x,y,0)+pxchange1)
		elif input.item(x,y,0)+pxchange1 > 255:
			input.itemset((x,y,0),255)
		else :
			input.itemset((x,y,0),0)

		if input.item(x,y,1)+pxchange2 <= 255 and input.item(x,y,1)+pxchange2 >= 0 :
			input.itemset((x,y,1),input.item(x,y,1)+pxchange2)
		elif input.item(x,y,1)+pxchange2 > 255:
			input.itemset((x,y,1),255)
		else :
			input.itemset((x,y,1),0)

		if input.item(x,y,2)+pxchange3 <= 255 and input.item(x,y,2)+pxchange3 >= 0 :
			input.itemset((x,y,2),input.item(x,y,2)+pxchange3)
		elif input.item(x,y,2)+pxchange3 > 255:
			input.itemset((x,y,2),255)
		else :
			input.itemset((x,y,2),0)

if debug == "true" :
	cv.imshow("Color change applied", input)
	cv.waitKey(0)





cv.imwrite(sys.argv[3], input)