#Gets Sequences from the NCBI- ID
import csv
import Bio
from Bio import SeqIO
from Bio import Entrez

Entrez.email = "rkatiyar@ramapo.edu"
Entrez.api_key = "8f31f1938108f0e82af1c7406f19d44fac08"

textfile = open("ID_only_1.txt", "r")
reader = csv.reader(textfile)
all_ID = [row for row in reader]

for i in range(len(all_ID)):
        handle = Entrez.efetch(db = "nucleotide", id = all_ID[i], rettype = "gb", retmode = "text")
        record = SeqIO.read(handle, "genbank")
        handle.close()
        Sequence = record.seq
        f = open("seq_list.txt", "a") 
        f.write(str(Sequence) + "\n")