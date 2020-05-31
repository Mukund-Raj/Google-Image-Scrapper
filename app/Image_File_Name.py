import posixpath

def Image_Name(link):

    #link splitted so that we can get the image name of that link
    imagename = link.split('/')[-1]

    file ,ext = posixpath.splitext(link)

    if ext in ['.png','.jpeg','.jpg']:
        print('yes do have ext')

    else:
        imagename +='.jpg'
        print('do noy have any extension')


    for i in imagename:
        #removing extra not wanted punctuations
        if i in '!@#$?{}[]%^&*()~*/=\"\'\\+;:+,;`':
            imagename = imagename.replace(i,'')

    print(imagename)
    #return the image name that we just get from the link
    return imagename