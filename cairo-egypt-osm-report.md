
# Case study of Cairo/Egypt [OpenStreetMap](http://www.openstreetmap.org/relation/5466227) xml file.  

Cairo is the capital of Egypt (my country).  
  
The uncompressed map xml-osm file is about 120 mb downloaed from [mapzen openstreetmap extractions](https://mapzen.com/data/metro-extracts/metro/cairo_egypt/)  
  
Most of the entries are from Cairo, but still there is a few from the two cities ( Banha,Giza) which are close to cairo.  
  
Knowing the data from OpenStreetMap  means that no one review the submit which causes lots of messy things.  
We will get to some of these messy data any try to clean them as much as we can.  
  
The xml data consists of 3 major tags ( [node](https://wiki.openstreetmap.org/wiki/Node), [way](https://wiki.openstreetmap.org/wiki/Way), [relation](https://wiki.openstreetmap.org/wiki/Relation) ),click on them for more information and check the [OpenStreetMap Wiki](https://wiki.openstreetmap.org/wiki/Main_Page),  
And 3 children tags [ [tag](https://wiki.openstreetmap.org/wiki/Tags) - member(parent=relation) - nd(parent=way) ]. 

----

## exploring problems in data :  
  
* what I'm concerned about in the cleaning proces is child tag "tag" which is in the form [key:value].  
* there are 239 different keys in the data .  
* 17 of them starts with "addr:..." and they are listed below :

|key|
-------
|addr:street|
|addr:housenumber|
|addr:city|
|addr:country|
|addr:postcode|
|addr:housename|
|addr:interpolation|
|addr:place|
|addr:street|
|addr:city_1|
|addr:suburb|
|addr:unit|
|addr:street|
|addr:province|
|addr:full|
|addr:city|
|addr:street:name|
------------------
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
 cleaning process is done by the python script : cleaning_map.py.
 It checks for all faulty data I mentioned earlier and then decide wether to reject, correct or keep the data as it is and then write the data into a new file  cleaned_data.osm .
 
---


## To CSV :

* next step is to convert the data from xml to csv format, using the schema "schema.py" and the python script "xml_to_csv.py" .    
* the result will be csv files one for each tag name, the columns are the attributes and the data are the values.

----
  
## To SQL :
* to convert the csv files into a SQLite database using the schema "schema.sql" and python script "csv_to_sql"
	
-----
## number of nodes, ways and relations :
```python
select count(nodes.id), count(ways.id), count(relations.id)
from nodes, ways, relations
```
|nodes|ways|relations|
----|-----|-------
|547370|112108|151
--------
## contributions over time :

edits to the map are made from 2008 to 2016 .  
here are 3 graphs for [ nodes, ways, relations ] creation.  
and we can see that the highest number of nodes and ways created on 07-2016 and the highest number of relations are created in 04-2013.  
-----
![nodes](https://docs.google.com/spreadsheets/d/1jjvbSRT1NAvvqnkjTAPzKIAgiJsss4I3wqOAegCLYXM/pubchart?oid=1869514109&format=image) 
![ways](https://docs.google.com/spreadsheets/d/1jjvbSRT1NAvvqnkjTAPzKIAgiJsss4I3wqOAegCLYXM/pubchart?oid=275453333&format=image)
![Relations](https://docs.google.com/spreadsheets/d/1jjvbSRT1NAvvqnkjTAPzKIAgiJsss4I3wqOAegCLYXM/pubchart?oid=379890330&format=image)

----
## Top 10 user : 

```sql
select e.user ,count(*) as num
from ( 
	select user from ways union all 
		select x.user from( 
			select user from relations union all 
				select user from nodes ) x 
	)  e
group by e.user
order by num desc
limit 10
```
----

| user | #of contributes
---- | ----
Salmanjk|	112319
Mohawow|	62067
warneke7|	60456
Triscia|	47106
Allegro34|	37416
DesertMoh|	29434
Rondon237|	28225
Heinz_V|	27355
tellmy@gmx_net|	26213
bauma|		24360

-----
they contributed in 68.97 % of overall contributions.  
the top user "Salmanjk" contributed in 17.03 %  .  

----
## top 10  used tag keys :

```python
select type, key , count(*) as num
from nodes_tags
group by type,key
order by num desc
limit 10
```
---------
type | key | #of occurrences
----|-----|------
regular|	power|	5048
regular|	name|	3116
regular|	start_date|	2933
name|	en|	2135
name|	ar|	1805
regular|	amenity|	1609
regular|	alt_name|	880
regular|	place|	7460
regular|	is_in|	686
regular|	int_name|	651
------
## top 10 used tag keys + values together :

type | key | value | #of occurrences
---|---|-----|-----
regular |	power|	tower|	4939
regular |	start_date	|2015|	2933
regular |	is_in	|Egypt, جمهورية مصر العربية	|571
regular |	place	|village|	491
regular |	amenity	|place_of_worship|	229
regular |	amenity	|restaurant|	218
regular |	barrier	|gate|	210
regular |	amenity	|cafe|	163
regular |	religion|	muslim|	148
regular |	natural|	tree|	140
------
## Most popular cuisines :

```python
SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
having num > 1
ORDER BY num DESC;
```
type | #of occurrences
----|------
regional	|18
italian	|9
american	|7
chicken	|7
pizza	|7
burger	|6
chinese	|4
ice_cream	|4
kebab	|4
Egyptian	|3
asian	|3
lebanese	|3
egyptian	|2
sandwich	|2
sushi	|2
---------------------
## Top 10 appearing amenities :

```python
SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
```
amenity | #of occurrences
----|-----
place_of_worship	|229
restaurant	|218
cafe	|163
fuel	|126
fast_food	|105
bank	|100
pharmacy	|89
hospital	|65
school	|64
embassy	|51
--------------
## Pizza resturants :heart_eyes: :

```python
SELECT nodes_tags.value
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='pizza') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='name'
GROUP BY nodes_tags.value
```
|name|
------
|Pizza Hut|
|Pizza King|
|Vinny's Pizzeria|
|بابا جونس|
|بيزا هت|
|دومينوز يتزا|
|هاردييز|
----------------------------
# Addional ideas :
  
### problem :
most of the messy data (in my opinion) are caused by misanderstanding of the fields, typo, writing in different language, or writing in different syntax ( like street names with different typing but still the same street)  
****
### solution :
I think the site could make some regex verfications for fields like postcode, housenumber and other fields that could be represented by a regular experession. 
  
And for the fields like city,country,streetnames I think that the site should get a list of them from other governmental source, and let the user choose his city,country,streetname from a drop-down list, this way there will be no miss-typing or any other strange data.
  
Also some fields should be united to some one language , just like some fields are meant only for english , and others from a local language, this way we won't have some fields with mixing languages which leads to  some problems.
*******
### implementation ideas/challenges regarding the solution :

Regarding the regex verfications, for example, for some city or country in the world the house number are counted from 00000 to 99999 , or two digit followed by two number so implementing the regex would be easy, but also you will have to make a regex for every country and maybe for some cities alone, which would be exhaustive also it would be some challenging to get range of housenumbers/postcodes for every city/country, It will require some huge search .
  
and For the  city and country it's easy to get lists for them from wikipedia/google-map or any other resource.
But the challenging is to get a list for each street-name, it's hard to get all the streets in some city without missing one, but also It can be handled, you can let the user choose from the street-names you got, and if didn't find his street, he could ask to add his streetname to the list.

******************

### another solution :
Another solution came to my mind, instead of searching for the streets/cities names, the website will start with empty list, then the first user will add his streetname/city , then second user will only add a new city/street name only if he didn't find his city/street on the list.

---------------------------------------------
# Finally :
this project proves that it's very hard to lean on human entered data.  
  
humans always make mistakes which are very hard to predict or deal with.  
  
the best way to take useful information from them is to restrict them to choose from ready-made data,
otherwise they will use their imagination to enter some illogical data.
