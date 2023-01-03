#extracts list of Viruses from ViDE database
import lxml
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "http://sdb.im.ac.cn/vide/sppindex.htm"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
type(soup)

all_links = soup.find_all("a")
for link in all_links:
       f = open("Virus_names.txt", "a")
       f.write(str(link) + "\n")