import os
import glob

#GIF_FOLDER = os.path.join(os.getcwd(), 'static/gifs')
#gif_files = [file for file in glob.glob(os.path.join(GIF_FOLDER, '*.gif'))]

# print GIF_FOLDER
# print gif_files

gif_files = []

#print gif_files[-2:] # most recent file

#os.chdir("./static/gifs/")
for file in glob.glob("./static/gifs/*.gif"):
    gif_files.append(file)

gif_files.sort(key=os.path.getmtime)

print gif_files[-3:]

print gif_files[-1]
print gif_files[-2]
print gif_files[-3]