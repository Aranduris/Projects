#extracts list of host species from VIDE database
import lxml
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://sdb.im.ac.cn/vide/hostlist.htm"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
type(soup)

all_links = soup.find_all("a")
for link in all_links:
   if link.get("href") != None:
       temp = link.get("href")
       str(temp)
       f = open("Host_names.txt", "a")
       f.write(temp + "\n")
else:
    f = open("Host_names.txt", "a")
    f.write("None" + "\n")