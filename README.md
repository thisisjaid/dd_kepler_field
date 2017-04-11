# dd_kepler_field
A small collection of scripts to determine if members of a DD user collection are also targets or items within the exoplanet survey catalogs, primarily Kepler Input Catalog and K2/EPIC.

# Components

## get_collection_objects
This is a small Bash shell script, just because I was too lazy to code all of this in Python and it was just quicker to do it this way. The job of this script is to query the Zooniverse/DD API to get the objects from a collection and their WISE ID and output it to a txt file data/dd_to_wise_ids_COLLECTIONID.txt (one per collection).

### Dependencies

* bash 
* jq (linux software package)

Only tested on a Linux system (Ubuntu 16.04)

## vizierget.py
This is the main Python script that queries Vizier for catalog data, using the J2000 format WISE ID obtained from the Zooniverse API. The way it works at the moment is we make a query to get the object coordinates and 2MASS key id from AllWISE, then query the Kepler Input Catalog to get the KIC ID and the 2MASS key id, we check that the two 2MASS key ids match for identity verification and finally we query the EPIC catalog with the same initial J2000 ID to check for membership and get the EPIC ID.

### Dependencies

* Python3 (linux software package)
* astroquery (pip package)
* astropy (pip package)

# Usage

* Add the target collection IDs to dd_target_collections.txt
* Run get_collection_objects 
`bash get_collection_objects`
* Run python3 vizierget.py

# Other notes

There is a 1 second delay between each Vizier query so as not to hammer the API too hard (not sure if they have a request limit, but best to be nice)
