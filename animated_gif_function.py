#!/usr/bin/python

import requests
import urllib
import os.path
import string
import configparser
import sys

def create_gif(uuid):
	UUID = uuid

	animated_gif_deriv = "t"

	#Housekeeping

	#create an instance of configparser, then read your config file into it
	config = configparser.ConfigParser()
	config.read('config.cfg')
	#find your DC token in the config file content (by section and name) and assign it to a variable
	token = config.get('DC','token')
	#saving the base url in your config file will make it easier to find next time you want to use it
	
	base = 'http://api.repo.nypl.org/api/v1/items/'
	auth = 'Token token=' + token

	#Make sure it's a valid UUID
	if len(UUID) != 36:
		return "That doesn't look like a UUID -- try again!"
	else:
		print "OK, that ID looks correct, looking it up now..."


	#function to get captures for a given UUID
	def getCaptures(uuid, titles='yes'):
	    url = base + uuid
	    if titles == 'yes':
	        url = url + '?withTitles=yes&per_page=500'
	    call = requests.get(url, headers={'Authorization': auth})
	    return call.json()

	def getItem(uuid):
		url = base + '/mods/' + uuid + '?per_page=500'
		call = requests.get(url, headers={'Authorization': auth}) 
		return call.json()

	def getContainer(uuid):
		url = 'http://api.repo.nypl.org/api/v1/collections/' + uuid + '?per_page=500'
		call = requests.get(url, headers={'Authorization': auth}) 
		return call.json()


	captureResponse = getCaptures(UUID)
	containerResponse = getContainer(UUID)
	itemResponse = getCaptures(UUID)

	isContainer = int(containerResponse['nyplAPI']['response']['numItems'])
	number_of_captures = int(captureResponse['nyplAPI']['response']['numResults'])

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



	for i in range(number_of_captures):
		captureID = itemResponse['nyplAPI']['response']['capture'][i]['imageID']
		captures.append(captureID)

	#print captures


	#Grab the item title, and do some cleanup to make it usable as a folder name
	table = string.maketrans("","")
	title = str(itemResponse['nyplAPI']['response']['capture'][0]['title']).translate(table, string.punctuation).replace("  "," ").replace(" ","_")
	title = title[:65].rstrip('_')+'_'+animated_gif_deriv+'_'+uuid
	print "folder title will be '"+title+"'"

	#Create folder based on the item title
	if not os.path.exists(title):
	    os.makedirs(title)

	# #Create the two kinds of derivs in the item-title folder
	img_url_base = "http://images.nypl.org/index.php?id="
	derivs = [animated_gif_deriv]

	if not os.path.isfile(title+'.gif'):
		for j in derivs:
			for i in range(number_of_captures):
				if not os.path.isfile(title+'/'+str(captures[i])+str(j)+'.gif'):
					urllib.urlretrieve(img_url_base+str(captures[i])+'&t='+str(j),title+'/'+str(captures[i])+str(j)+'.jpg')
					print captures[i], j, i+1, "of", number_of_captures
					i+=1
				else:
					print "file %s as %s deriv type already exists" % (captures[i], j)
					i+=1
	else:
		return "%s.gif already exists!" % (title)

	# Call the ImageMagick 'convert' program to string all of the frames
	# together into an animated GIF
	print "Creating animated.gif ..."
	if not os.path.isfile(title+'.gif'):
		os.system("convert -delay 20 -loop 0 %s/*%s.jpg -coalesce -gravity center %s.gif" % (title, animated_gif_deriv, title)) 
		os.system("rm -rf %s" % (title))
		print "Done creating animated.gif"
		print "Cleaning up now..."
	else:
		os.system("rm -rf %s" % (title))
		print "%s.gif already exists!" % (title)

	print "You're all set!"
	#return send_file(title+'.gif', mimetype='image/gif')
	return title

if __name__ == '__main__':
	uuid =  raw_input('Enter a file UUID: ')
	create_gif(uuid)