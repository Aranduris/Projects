# This code is used to obtain common name data based on the scientific name that was provided in the
# Oringal dataset.

library(taxize)
library(dplyr)
library(readr)
library(rentrez)

# API key for Entrez
ENTREZ_KEY='2a83490c755a9ece8ddfbf09015fc2e8b009'
set_entrez_key(ENTREZ_KEY)

# Get data
taxon_name <- read.delim("~/MS_DataScience/Thesis/Project/Data/taxon_name.txt")

# Scientific names
sci_n <- taxon_name$taxname

common_names <- c()

# For every scientific names - get the common name from ncbi
for (i in 1:length(sci_n)){
  common_names[i] <- sci2comm(sci_n[i],df='ncbi')}

taxon_name$comname <- common_names
View(taxon_name)

taxon_name$comname <- as.character(taxon_name$comname)

# Create a new file 
write.csv(taxon_name, file='~/MS_DataScience/Thesis/Project/Data/taxon_name_1.txt', row.names = FALSE, quote = FALSE,fileEncoding = "UTF-8")
