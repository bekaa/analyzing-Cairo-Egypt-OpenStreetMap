
# Case study of Cairo/Egypt [OpenStreetMap](https://www.openstreetmap.org) xml file.  

Cairo is the capital of Egypt (my country).  
The uncompressed map xml-osm file is about 120 mb downloaed from [mapzen openstreetmap extractions](https://mapzen.com/data/metro-extracts/metro/cairo_egypt/)  
Most of the entries are from Cairo, but still there is a few from the two cities [ Banha,Giza) which are close to cairo.  
Knowing the data from OpenStreetMap  means that no one review the submit which causes lots of messy things.  
We will get to some of these messy data any try to clean them as much as we can.  

The xml data consists of 3 major tags ( [node](https://wiki.openstreetmap.org/wiki/Node), [way](https://wiki.openstreetmap.org/wiki/Way), [relation](https://wiki.openstreetmap.org/wiki/Relation) ),click on them for more information and check the [OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Main_Page),  
And 3 children tags [ (tag)[https://wiki.openstreetmap.org/wiki/Tags] - member(parent=relation) - nd(parent=way) ].  
## exploration :  
* what I'm concerned about in the cleaning proces is child tag "tag" which is in the form [key:value].  
* there are 239 different keys in the data .  
* 17 of them starts with "addr:..." and they are listed below :
  * addr:street
  * addr:housenumber
  * addr:city
  * addr:country
  * addr:postcode
  * addr:housename
  * addr:interpolation
  * addr:place
  * addr:street
  * addr:city_1
  * addr:suburb
  * addr:unit
  * addr:street
  * addr:province
  * addr:full
  * addr:city
  * addr:street:name
 * address data should be clean for future analysis, so I'll look at each of them and clean the dirty ones.  
 * I wrote a python script to print out all the values for each key in distinct file. the script named "explore_key_and_values.py" in the repo.  
 * After look in each file of them I noticed some unexpected data in some files :
 	* addr:country :  
  	* expected : all the values should have the value "Egypt" or something similar.
  	* BUT if found all the values between "EG" (the know symbol for egypt) and "ET" this also refers to egypt but it's not known.
  	* solution : change all "ET" values to "EG". 
	* addr:city :
		* expected : all values should be in [ Cairo, Banha, Giza]
		* BUT many values either streets in the city or the city name in different typing and even in different language (local language).
		* Solution : to make 3 lists, one for each city and the lists will contain it's alternative names and streets mentioned in that key.
	* addr:street :
		* expected : streets names :grin: .
		* BUT that's the most messy portion of the data :no_mouth: ,  the same street can be found in more than 20 different shapes in different languaes.
		* Solution : is to make lists for each street with all alternative names for it, and if I started doing that I'll last forever doing it :joy: , so I believe there is no way to fix this :disappointed: .
	* addr:housenumber :
		* expected : normal house numbers :smiley:
		* BUT many values are far away from normal :joy: , if found the following :
			* some people enters their mobile phone numbers instead :flushed:
			* some enters their street names.
			* others enters some large number in legnth which doesn't make sense.
			* some others enters floating point values like [02.35699066]
			* some values have special characters.
			* and some are in a list form.
		* solution : is to choose which values to reject, which to correct and which to keep.
	* addr:postcode :
		* expected : postcodes , really I expect postcode not phone numbers ! :joy:
		* But instead I found some phone number and street names.
		* Solution : is to reject these values.


----

## Cleaning : 
	
    
 
