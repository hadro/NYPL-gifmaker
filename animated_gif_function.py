#!/usr/bin/python

import requests
import urllib
import os.path
import string
import sys
import shutil
import subprocess
import boto3

client = boto3.client('s3')

def create_gif(uuid, gif_size):
	UUID = uuid
	animated_gif_deriv = gif_size

	#Housekeeping
	base = 'http://api.repo.nypl.org/api/v1/items/'
	auth = 'Token token=4t2gkh9vetsh35av'

	#Make sure it's a valid UUID
	if len(UUID) != 36:
		print "That doesn't look like a UUID -- try again!"
		return (False, "That doesn't look like a UUID -- try again!")
	else:
		print "OK, that ID looks correct, looking it up now..."


	#function to get captures for a given UUID
	def getCaptures(uuid, titles='yes'):
	    url = base + uuid
	    if titles == 'yes':
	        url = url + '?withTitles=yes&per_page=100'
	    call = requests.get(url, headers={'Authorization': auth})
	    return call.json()

	def getItem(uuid):
		url = base + '/mods/' + uuid + '?per_page=100'
		call = requests.get(url, headers={'Authorization': auth}) 
		return call.json()

	def getContainer(uuid):
		url = 'http://api.repo.nypl.org/api/v1/collections/' + uuid + '?per_page=100'
		call = requests.get(url, headers={'Authorization': auth}) 
		return call.json()


	captureResponse = getCaptures(UUID)
	containerResponse = getContainer(UUID)
	itemResponse = getCaptures(UUID)

	isContainer = int(containerResponse['nyplAPI']['response']['numItems'])
	number_of_captures = int(captureResponse['nyplAPI']['response']['numResults'])

	# if number_of_captures > 100:
	# 	return (False, "So sorry, that UUID has more images than we can glue together into a GIF right now! Try another?")
	# #Check to make sure we don't accidentally have a container or a collection UUID here
	# if isContainer > 0 and number_of_captures > 0:
	# 	sys.exit("This is a container, let's bail.")
	#If we're good to go, either get the number of capture IDs, or go to the item UUID and get the # of captures there

	print "OK, this is a usable UUID, let's see what we can do with it..."
	if number_of_captures > 0: 
		print "%s captures total" % (number_of_captures)
		print UUID
	else:
		print "No captures in the API response! Trying to see if this is a capture UUID, not an item UUID..."
		UUID = getItem(UUID)['nyplAPI']['response']['mods']['identifier'][-1]['$']
		itemResponse = getCaptures(UUID)
		number_of_captures = int(itemResponse['nyplAPI']['response']['numResults'])
		print "Correct item UUID is "+UUID
		print "Item UUID has %s captures total" % (number_of_captures)

	#OK, enough checking, let's get the actual captures!
	captures = []
	if number_of_captures >100:
		for i in range(100):
			captureID = itemResponse['nyplAPI']['response']['capture'][i]['imageID']
			captures.append(captureID)
		number_of_captures = 100
	else:
		for i in range(number_of_captures):
			captureID = itemResponse['nyplAPI']['response']['capture'][i]['imageID']
			captures.append(captureID)

	#print captures


	#Grab the item title, and do some cleanup to make it usable as a folder name
	table = string.maketrans("","")
	title = itemResponse['nyplAPI']['response']['capture'][0]['title'].encode('utf-8').translate(table, string.punctuation).replace("  "," ").replace(" ","_")[:65].rstrip('_')+'_'+animated_gif_deriv+'_'+uuid
	print "folder title will be '"+title+"'"

	gif_path = 'static/gifs/'
	title_path = gif_path+title


	#Create folder based on the item title
	if not os.path.isfile(title_path+'.gif'):
	    os.makedirs(title_path)
	else:
		shutil.rmtree(title_path)

	# #Create the two kinds of derivs in the item-title folder
	img_url_base = "http://images.nypl.org/index.php?id="
	derivs = [animated_gif_deriv]

	if not os.path.isfile(title_path+'.gif'):
		for j in derivs:
			for i in range(number_of_captures):
				if not os.path.isfile(title_path+'/'+str(captures[i])+str(j)+'.gif'):
					urllib.urlretrieve(img_url_base+str(captures[i])+'&t='+str(j),title_path+'/'+str(captures[i])+str(j)+'.jpg')
					print captures[i], j, i+1, "of", number_of_captures
					i+=1
				else:
					print "file %s as %s deriv type already exists" % (captures[i], j)
					i+=1
	else:
		return title

	# Call the ImageMagick 'convert' program to string all of the frames
	# together into an animated GIF
	print "Creating animated.gif ..."
	delay = 20
	if not os.path.isfile(title_path+'.gif'):
		cmd = ["convert", "-delay", str(delay), title_path+'/*'+animated_gif_deriv+'.jpg', "-layers", "optimize",  gif_path+'/'+title+'.gif']
		subprocess.call(cmd)
		shutil.rmtree(title_path)
		print "Done creating animated.gif"
		print "Cleaning up now..."
	else:
		shutil.rmtree(title_path)
		return title

	print "You're all set!"
	client.upload_file(title_path.decode('utf-8')+'.gif', 'gifmaker-test', title_path.decode('utf-8')+'.gif')
	return title

if __name__ == '__main__':
	uuid = raw_input("UUID: ")
	gif_size = raw_input("Size: ")
	create_gif(uuid, gif_size)