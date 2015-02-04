---
layout: post
title: The Open Source analogy for research data curation
author: Robert Forkel
menu_item: blog
---

We are obviously 
<a href="http://digitalhumanities.org/answers/topic/what-are-the-best-practices-for-data-curation-in-github"><i class="icon-share">&nbsp;</i>not the first ones</a>
to have come up with the idea of 
<a href="http://cameronneylon.net/blog/fork-merge-and-crowd-sourcing-data-curation/"><i class="icon-share">&nbsp;</i>using GitHub for collaborative data curation</a>.


What GitHub and the pull request have done for open source software development is simply
too good to lose out on when it comes to research data curation: They created a global community around a:

- <a href="http://git-scm.com/"><i class="icon-share">&nbsp;</i>tool</a> and
- <a href="https://gun.io/blog/how-to-github-fork-branch-and-pull-request/"><i class="icon-share">&nbsp;</i>workflow</a> 

which lowers the level of expertise for potential contributors to what seems the optimal threshold
to divide signal from noise.

Now, knowing how to use a version control system may not quite be the optimal threshold when trying to
stipulate researchers to contribute to collaborative curation projects. But it should be safe to say
<a href="http://blogs.biomedcentral.com/bmcblog/2013/02/28/version-control-for-scientific-research/"><i class="icon-share">&nbsp;</i>it's on its way</a> 
into the curriculum.

So what is our take on using GitHub for collaborative data curation?
First of all, we see it as a way to formalize procedures which have been part of data curation
at all times:

- git provides a formal protocol for merging changes, thus it's the cornerstone of collaboration.
- A byproduct of this protocol is the ability to identify and re-create different states of the data, thereby providing support for versioned data.
- The pull request is a protocol for reviewed data updates.
- The fork can be used to formalize the concept of maintenance transfer.
- And releases can be seen as the equivalent of publications.

Note: While some advantages of using git hinge on using line-based text formats for the data, 
preferably not cluttered with markup 
(<a href="http://en.wikipedia.org/wiki/Comma-separated_values"><i class="icon-share">&nbsp;</i>csv</a> , 
<a href="http://en.wikipedia.org/wiki/BibTeX"><i class="icon-share">&nbsp;</i>BibTeX</a> , 
<a href="http://en.wikipedia.org/wiki/JSON"><i class="icon-share">&nbsp;</i>JSON</a> if pretty printed), most of the
points hold for binary data as well. But again, missing out on 
<a href="https://github.com/clld/tsammalex-data/blob/master/.gitattributes"><i class="icon-share">&nbsp;</i>the level of support</a>
provided by a mature system such as git would seem foolish.

But you can go further:

- For the Tsammalex data we used GitHub's 
  <a href="https://help.github.com/articles/about-webhooks/"><i class="icon-share">&nbsp;</i>Webhooks</a> system,
  namely the integration with <a href="https://travis-ci.org/"><i class="icon-share">&nbsp;</i>Travis CI</a>
  to implement 
  <a href="https://travis-ci.org/clld/tsammalex-data"><i class="icon-share">&nbsp;</i>data integrity checks</a>
  which are run upon pushing new data, providing a comfortable mechanism to make sure only data releases
  passing these tests are deployed to the 
  <a href="http://tsammalex.clld.org"><i class="icon-share">&nbsp;</i>Tsammalex website</a>.
- Of course issue trackers which come with most hosted version control systems make a good list of errata.
- GitHub adds more and more data visualization functionality (e.g. 
  <a href="https://help.github.com/articles/mapping-geojson-files-on-github/"><i class="icon-share">&nbsp;</i>rendering maps displaying GeoJSON data</a> in a repository.), thereby turning the data repository itself
  into a basic data browser.
- And again the webhook system allows integration with a service like 
  <a href="https://zenodo.org"><i class="icon-share">&nbsp;</i>Zenodo</a>, which provides
  <a href="https://guides.github.com/activities/citable-code/"><i class="icon-share">&nbsp;</i>backup, archiving and a DOI</a> for releases of a GitHub repository.

So considering all this and trying to eat our own dogfood, we are happy to make 
<a href="http://glottolog.org"><i class="icon-share">&nbsp;</i>Glottolog</a>
(our flagship when it comes to integrating data from multiple sources) available
for this type collaboration: 
<a href="https://github.com/clld/glottolog-data"><i class="icon-share">&nbsp;</i>clld/glottolog-data</a>.