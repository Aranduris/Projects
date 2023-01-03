#Gets NCBI-ID of all viruses
import csv
import Bio
from Bio import Entrez

Entrez.email = "rkatiyar@ramapo.edu"
textfile = open("10.txt", "r")
reader = csv.reader(textfile)
allRows = [row for row in reader]

for i in range(len(allRows)):
    handle = Entrez.esearch(db = "nucleotide", term = allRows[i], retmax = 1)
    record = Entrez.read(handle)
    handle.close()
    idList = record["IdList"]
    f = open("idrecords10.txt", "a")
    f.write(str(idList)+ "\n")