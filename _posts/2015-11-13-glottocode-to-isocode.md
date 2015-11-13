---
layout: post
title: Mapping Glottocodes to ISO 639-3
author: Robert Forkel
menu_item: blog
---

A lot of data about languages marks the associated language either using its Glottocode
(i.e. its identifier according to [Glottolog](http://glottolog.org)) or its 
[ISO 639-3](http://www-01.sil.org/iso639-3/) code. So often, when merging data from various
sources, the issue of mapping between the two code systems comes up.

From the use case of merging data, a one-to-one correspondence would be ideal.
Conceptionally, though, the mapping may be many-to-many, and in addition, a ISO 639-3 code
may map to a [Glottolog (sub)family or dialect](http://glottolog.org/meta/glossary#Languoid), 
not necessarily a Glottolog language. 
So a table listing only the one-to-one correspondences may be deceptive. 

But since such a table is clearly useful, if only to get done with the simple cases, here
is a recipe to create such a mapping dynamically. We use the general information about
[languages in Glottolog in JSON format](http://glottolog.org/resourcemap.json?rsc=language).
This JSON object contains a member *resources* listing all Glottolog languages. The information
about one language looks like
```python
        {
            "id": "aari1239", 
            "identifiers": [
                {
                    "identifier": "aiw", 
                    "type": "iso639-3"
                }, 
                {
                    "identifier": "aar", 
                    "type": "WALS"
                }, 
                {
                    "identifier": "aiw", 
                    "type": "multitree"
                }
            ], 
            "latitude": 5.95034, 
            "longitude": 36.5721, 
            "name": "Aari"
        }
```
Simplifying such an object to
```python
        {
            "glottocode": "aari1239", 
            "isocode": "aiw"
        }
```
is a typical task for the excellent [jq tool](https://stedolan.github.io/jq/). Turning
JSON into csv can be done using 
[csvkit's in2csv command](http://csvkit.readthedocs.org/en/0.9.1/scripts/in2csv.html).
So wrapping up, we can turn Glottolog's information for languages into a csv file of the form
```
glottocode,isocode
aari1239,aiw
aari1240,aay
aari1244,aiz
...
```
with a single command line:
```
curl "http://glottolog.org/resourcemap.json?rsc=language"\
| jq '[.resources[] | {glottocode: .id, isocode: [.identifiers[]] | map(select(.type == "iso639-3"))[0].identifier}] | map(select(.isocode!=null))'\
| in2csv -f json > glottocode2iso.csv
```
