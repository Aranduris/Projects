#Finds taxonomic information on the following common names within the NCBI database
library("taxize")
set_entrez_key("8f31f1938108f0e82af1c7406f19d44fac08")
Sys.getenv("ENTREZ_KEY")

name <- c('Sugarcane', 'Corn', 'Rice', 'Wheat', 'Cucumbers', 'Tomatoes', 'Carrots', 'Spinach', 'Papayas', 'Cabbages', 'Soybean', 'Peach', 'Oranges', 'Peppermint', 'Pineapples', 'Strawberries', 'Lettuce', 'Onions', 'Bananas', 'SweetPotatos', 'Apples', 'Cotton', 'Chillies', 'Yams', 'Pears')
uids <- get_uid(commonname)
uids.found <- as.uid(uids[!is.na(uids)])
commonname.found <- commonname[!is.na(uids)]
sciname <- sci2comm(name, db = 'ncbi')
names(sciname) <- commonname.found
sciname