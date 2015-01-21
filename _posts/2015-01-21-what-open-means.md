---
layout: post
title: What open means - a case study
author: Robert Forkel
menu_item: blog
---

Tsammalex, a multilingual lexical database on plants and animals, uses 
[WWF Ecoregions](http://tsammalex.clld.org/ecoregions) as one facet to navigate species.
Thus whenever new species are added to the database, we have to answer the question
which ecoregions are populated by this species?

As it turns out, this question is relatively easy to answer due to Open Source software
and Open Data. The remainder of this post will be a fairly technical description how to
use the Open Source software
[Python](https://www.python.org/),
[fiona](http://toblerity.org/fiona/) and
[shapely](http://toblerity.org/shapely/)
and Open Data to answer this question.

We first download the [shapefile](http://en.wikipedia.org/wiki/Shapefile) containing the
GIS data for the [WWF Terrestrial Ecoregions of the World](http://web.mit.edu/11.951/ecoplan/data/ecoregions/)
([README](http://web.mit.edu/11.951/ecoplan/data/ecoregions/wwf_terr_ecos.htm)):

{% highlight bash %}
curl -O http://web.mit.edu/11.951/ecoplan/data/ecoregions/wwf_terr_ecos.shp
curl -O http://web.mit.edu/11.951/ecoplan/data/ecoregions/wwf_terr_ecos.dbf
curl -O http://web.mit.edu/11.951/ecoplan/data/ecoregions/wwf_terr_ecos.shx
curl -O http://web.mit.edu/11.951/ecoplan/data/ecoregions/wwf_terr_ecos.prj
{% endhighlight %}

Information about observations of species is available from [GBIF.org](http://www.gbif.org) via
their [great API](http://www.gbif.org/developer/summary). In particular we are going
to use the 
[species/match](http://www.gbif.org/developer/species#searching) method to find a GBIF
identifier for a scientific species name and the
[occurrence/search](http://www.gbif.org/developer/occurrence#search) method to retrieve
a list of occurrences for this species.

{% highlight python %}
import requests

def gbif_api(path, **params):
    return requests.get('http://api.gbif.org/v1/' + path, params=params).json()


def occurrences(species):
    # Note: We limit the occurrences to ones observed by humans 
    # and tagged with geo-coordinates.
    kw = dict(
        taxonKey=gbif_api('species/match', name=species)['speciesKey'],
        basisOfRecord='HUMAN_OBSERVATION',
        hasCoordinate='true',
        limit=100)
    return gbif_api('occurrence/search', **kw)['results']
{% endhighlight %}

A single occurrence record serialized as JSON looks as follows:
{% highlight javascript %}
        {
            "basisOfRecord": "HUMAN_OBSERVATION", 
            "catalogNumber": "551402", 
            ...
            "country": "United States", 
            "countryCode": "US", 
            "datasetName": "iNaturalist research-grade observations", 
            ...
            "decimalLatitude": 26.4395, 
            "decimalLongitude": -82.09795, 
            ...
        }
{% endhighlight %}

The ecoregion data in the shapefile when read with fiona is presented as
[records](http://toblerity.org/fiona/manual.html#records), with `properties` looking as
follows:

{% highlight python %}
           "properties": {
                "AREA": 29.8029417004, 
                "BIOME": 14.0, 
                "ECO_ID": 61404.0, 
                "ECO_NAME": "Northern Mesoamerican Pacific mangroves", 
                "ECO_NUM": 4.0, 
                "ECO_SYM": 119.0, 
                "G200_BIOME": 0.0, 
                "G200_NUM": 0.0, 
                "G200_REGIO": null, 
                "G200_STAT": 0.0, 
                "GBL_STAT": 1.0, 
                "OBJECTID": 1, 
                "PERIMETER": 0.219, 
                "REALM": "NT", 
                "Shape_Area": 0.00276856457255, 
                "Shape_Leng": 0.219475413877, 
                "area_km2": 8174, 
                "eco_code": "NT1404"
            }
{% endhighlight %}

Now finding ecoregions in which a species has been observed can be done as follows:

{% highlight python %}
import fiona
from shapely.geometry import shape, Point

def get_ecoregions(species):
    with fiona.collection('wwf_terr_ecos.shp', "r") as source:
        ecoregions = [
            (feature['properties'], shape(feature['geometry']))
            for feature in source if feature['geometry']]

    eco_codes = {}
    for oc in occurrences(species):
        point = Point(oc['decimalLongitude'], oc['decimalLatitude'])
        for props, er in ecoregions:
            eco_code = props['eco_code']
            try:
                if er.contains(point):
                    if eco_code not in eco_codes:
                        eco_codes[eco_code] = props['ECO_NAME']
                        break
            except:
                pass
    return eco_codes
{% endhighlight %}

Putting it all together we get a script
<script src="https://gist.github.com/xrotwang/9f0377cfae9ee94ae31b.js"></script>

which can be run as

{% highlight bash %}
$ python ecoregions_for_species.py "Ursus maritimus"
PA1101 Arctic desert
NA0616 Southern Hudson Bay taiga
NA1113 Kalaallit Nunaat low arctic tundra
NA1112 Kalaallit Nunaat high arctic tundra
{% endhighlight %}

Which looks about right considering that *Ursus maritimus* is also known as *Polar Bear*.