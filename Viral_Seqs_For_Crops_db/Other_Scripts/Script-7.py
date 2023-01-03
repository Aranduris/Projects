import csv
import Bio
from Bio import Entrez 
from Bio import SeqIO

Entrez.email = "rkatiyar@ramapo.edu"
Entrez.api_key = "8f31f1938108f0e82af1c7406f19d44fac08"

textfile = open("Virus_ID.txt", "r")
reader = csv.reader(textfile)
all_ID = [row for row in reader]

for i in range(len(all_ID)):
    with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text",id= all_ID[i]) as handle:
        for seq_record in SeqIO.parse(handle, "gb"):
            f = open("CDS_loc.txt", "a")
            f.write(str(all_ID[i]) + "\n")
            for feature in seq_record.features:
                if feature.type == 'CDS':
                    f.write(str(feature.location) + "\n")