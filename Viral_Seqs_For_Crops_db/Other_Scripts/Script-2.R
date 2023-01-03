#Finds taxonomic information on the following Species names within the ITIS database
library("taxize")
set_entrez_key("8f31f1938108f0e82af1c7406f19d44fac08")
Sys.getenv("ENTREZ_KEY")

species <- c('Saccharum officinarum','Zea mays','Oryza australiensis','Oryza barthii','Oryza cubensis','Oryza glaberrima', 'Oryza latifolia', 'Oryza longistaminata')
uids <- get_uid(species)
uids.found <- as.uid(uids[!is.na(uids)])
species.found <- species[!is.na(uids)]
common.names <- sci2comm(uids.found, db = 'itis')
names(common.names) <- species.found
common.names
