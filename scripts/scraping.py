import requests
from bs4 import BeautifulSoup
from six.moves import urllib
url=[]

page = 1
for i in range(16):
    if i<=3:
        kelas='fire'
    elif i<=9:
        kelas ='grass'
    elif i<=15:
        kelas = 'water'

    url += ["http://pokeunlock.com/pokedex/?fwp_type="+kelas+"&fwp_paged=" + str(page)]
    if page==4 and kelas == 'fire':
        page=1
    elif page==6 and kelas == 'grass':
        page=1
    else:
        page+=1
    i+=1
   

i=0
for loop_url in url:	
    r = requests.get(loop_url)
    soup = BeautifulSoup(r.content)

    images = soup.find_all("img")
	
    for img in images:
	temp = img.get('src')
	print (i, temp)
	if temp[:1]=="/":
	    image = "http:" + temp
	else:
	    image = temp
        kelas = loop_url.split('=')[1].split('&')[0]
	    filename=kelas+'.'+str(i)
	    imagefile = open(filename+".png", 'wb')
	    imagefile.write(urllib.request.urlopen(image).read())
	    imagefile.close()	
        if i==70 and kelas=='fire':
            i=0
        elif i==101 and kelas=='grass':
            i=0
        else:
            i+=1
