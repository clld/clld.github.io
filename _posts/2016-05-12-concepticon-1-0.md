---
layout: post
title: Concepticon 1.0 released
author: Robert Forkel
menu_item: blog
---

We are happy to announce the release of [Concepticon 1.0](http://concepticon.clld.org),
a resource for the linking of concept lists. Our resource presents an attempt to link the 
large amount of different concept lists which are used in the linguistic literature, 
ranging from Swadesh lists in historical linguistics to naming tests in clinical studies 
and psycholinguistics. 

Our Concepticon links concept labels from different conceptlists 
to concept sets. Each concept set is given a unique identifier, a unique label, and a 
human-readable definition. Concept sets are further structured by defining different 
relations between the concepts.

The resource can be used for various purposes. Serving as a rich reference for new and 
existing databases in diachronic and synchronic linguistics, it allows researchers a 
quick access to studies on semantic change, cross-linguistic polysemies, and semantic 
associations. 

You can search through
[more than 30,000 different concept labels](http://concepticon.clld.org/values) from 
[161 concept lists](http://concepticon.clld.org/contributions), which
are now almost completely mapped to [2,632 concept sets](http://concepticon.clld.org/parameters). We added
metadata, which will be useful when checking concept stability,
including links to Babelnet, Wordnet, and some psycholinguistic norm
databases, and although we know that this is all preliminary and needs
further refinement in the future, we think it is a promising start
towards more transparent data in historical linguistics.

We also regard Concepticon as a major building block in our attempt to specify useful but
simple data formats for cross-linguistic research under [the CLDF label](http://cldf.clld.org/).
Word lists are about the simplest data structure in cross-linguistic research, yet,
comparability was hampered by a lack of shared language and concept catalogs. Addressing the
first with [Glottolog](http://glottolog.org) and the second with our new Concepticon turns
wordlists into simple lists of triples (form, conceptset-ID, glottocode). This interoperability
increases the amount of data available to advanced tasks like automated cognate detection
vastly, thus opening up new venues for research.
