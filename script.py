from PIL import Image 

def DataGenerator(data): 
		
		# list of binary codes 
		# of given data 
		newd = [] 
		
		for i in data: 
			newd.append(format(ord(i), '08b')) 
		return newd 
		
# Pixels are modified according to the 
# 8-bit binary data and finally returned 
def modPix(pix, data): 
	
	datalist = DataGenerator(data) 
	lendata = len(datalist) 
	imdata = iter(pix) 

	for i in range(lendata): 
		
		# Extracting 3 pixels at a time 
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]] 
									
		# Pixel value should be made 
		# odd for 1 and even for 0 
		for j in range(0, 8): 
			if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
				
				if (pix[j]% 2 != 0): 
					pix[j] -= 1
					
			elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
				pix[j] -= 1
				
		# Eigh^th pixel of every set tells 
		# whether to stop ot read further. 
		# 0 means keep reading; 1 means the 
		# message is over. 
		if (i == lendata - 1): 
			if (pix[-1] % 2 == 0): 
				pix[-1] -= 1
		else: 
			if (pix[-1] % 2 != 0): 
				pix[-1] -= 1

		pix = tuple(pix) 
		yield pix[0:3] 
		yield pix[3:6] 
		yield pix[6:9] 

def encode_enc(newimg, data): 
	w = newimg.size[0] 
	(x, y) = (0, 0) 
	
	for pixel in modPix(newimg.getdata(), data): 
		
		# Putting modified pixels in the new image 
		newimg.putpixel((x, y), pixel) 
		if (x == w - 1): 
			x = 0
			y += 1
		else: 
			x += 1
			

def encode(): 
	img = input("Enter image name with extension:")
	#img = 'download.png' 
	image = Image.open(img, 'r') 
	
	data = input("Enter your secret data: ") 
	if (len(data) == 0): 
		raise ValueError('No data set') 
		
	newimg = image.copy() 
	encode_enc(newimg, data) 
	
	new_img_name = input("Enter new image name with extension: ") 
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper())) 

	#call the decode to get the hidden message from the new image file 
	response = decode()
	print("Message is : ", response)


def decode(): 
	img = input("Enter new image name with extension created earlier :") 
	image = Image.open(img, 'r') 
	
	data = '' 
	imgdata = iter(image.getdata()) 
	
	while (True): 
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]] 
		# string of binary data 
		binstr = '' 
		
		for i in pixels[:8]: 
			if (i % 2 == 0): 
				binstr += '0'
			else: 
				binstr += '1'
				
		data += chr(int(binstr, 2)) 
		if (pixels[-1] % 2 != 0): 
			return data 
			
		
if __name__ == '__main__' : 
	encode() 

