---
layout: post
title: Data curation strategies of CLLD databases
author: Robert Forkel
menu_item: blog
---

Two and a half years into the CLLD project we see two main strategies of coping with 
[the versioning problem](http://clld.org/2014/07/28/citing-clld-databases.html).
In this post I will describe these strategies as exemplified by the [WALS](http://wals.info) 
and [Tsammalex](http://tsammalex.clld.org)
database respectively and investigate their strengths and weaknesses.

Both databases are published by corresponding 
[clld](https://github.com/clld/clld) applications, so data access is pretty much the same.
The main difference in their data curation strategies is in the role, the PostgreSQL
database of this application plays.


The WALS model
--------------

In the case of WALS, the data is curated in this database, i.e. 

- the [PostgreSQL software](http://www.postgresql.org/) is used to ensure integrity of the data 
  and must be used to interact with the data.
- WALS data in plain text formats is derived from this database via code (to export or dump).

Given these constraints, updating and versioning are handled as follows:

- Modification of the data is effected through [migrations](https://en.wikipedia.org/wiki/Schema_migration), 
  i.e. code which acts on the data using SQL. Each 
  [migration script](https://github.com/clld/wals3/tree/master/migrations/versions) constitutes 
  a version of the database.
- Each version of database can be reconstructed by applying the appropriate
  number of migrations to a known state of the database.
- To reconstruct versions of the derived text formats, the relevant code used to create these formats 
  needs to be reconstructed (and versioned) as well.


The Tsammalex model
-------------------

In the spirit of ["data is code"](https://github.com/clld/lanclid2/blob/master/presentations/forkel.pdf)
Tsammalex data is curated as set of 
[csv files](https://en.wikipedia.org/wiki/Comma-separated_values) managed with the version control system 
[git](http://git-scm.com/). This git repository is hosted on [GitHub](https://github.com/clld/tsammalex-data).

The database used by the clld app serving http://tsammalex.clld.org is derived from these
csv files, or more precisely from [releases](https://github.com/clld/tsammalex-data/releases) 
of the git repository storing these files.
Thus, the clld app and its database are purely a publishing mechanism for the data, i.e. they 
provide a user interface and an [API](https://en.wikipedia.org/wiki/Application_programming_interface).


Strengths and weaknesses
------------------------

- **Changes of the database schema:**
  Since - in the WALS model - migration scripts, i.e. modifications of the
  data, are part of the application code, application code and corresponding database 
  version are synchronized automatically;
  whereas the Tsammalex model requires out-of-band mechanisms
  (like naming conventions for data and [application code releases](https://github.com/clld/tsammalex/releases)) 
  to enable synchronization.

- **Errata or intra-edition modification of the database:**
  With the WALS model, errata can be fixed transparently in the published database;
  whereas the Tsammalex model only allows modification of the data in the
  git repository, but requires a new edition (i.e. release) to push these
  modifications to the clld application.

- **Collaboration:**

  - The barrier to entry for collaboration on the data is significantly higher
    for WALS, since it requires proficiency in programming, both in the 
    [python language](https://www.python.org/) and in [SQL](https://en.wikipedia.org/wiki/SQL). 
    It could be argued, though, that collaborating via editing csv
    files kept in git is not particularly easy either. But leaving the issue of editing
    text files aside, the [collaboration workflow with git and GitHub](https://help.github.com/articles/using-pull-requests/) 
    is well documented and becoming standard in the open source world.

  - Since migration scripts are ordered linearly, the WALS model does only allow
    reconstruction of stages in this linear version history. With the Tsammalex
    model, reconstruction of the database for any state of the git data repository
    is possible - including constructing the database and running the clld application on
    top of private forks of the data repository. Thus, Tsammalex trivially provides
    functionality often requested for WALS: How can I compare my own data with WALS?

- **History:** Since the WALS application database keeps a 
  [history of all changes](http://docs.sqlalchemy.org/en/rel_1_0/orm/examples.html#module-examples.versioned_history)
  it is possible to present a [list of changes](http://wals.info/changes) on the WALS website. 
  However, tracing these changes back to corresponding migrations, e.g. to determine authorship,
  requires investigation of the [commit history](https://github.com/clld/wals3/commits/master)
  of the application software. With Tsammalex keeping a 
  [history of changes](https://github.com/clld/tsammalex-data/commits/master) is entirely left
  to git (which was built for exactly this purpose, after all); and considering that collaboration
  is easier and more transparent in the Tsammalex case, the history of changes may also 
  [reveal more information](https://github.com/clld/tsammalex-data/pull/10).

- **Public vs. private:** While with the WALS model preparation of new editions
  happens in private by default (because there is no public curation platform),
  with Tsammalex public is the default. But in the case of Tsammalex, it would
  be easy to fork the data repository into a private repos, modify/add to the
  data, when done, submit a pull request to `clld/tsammalex-data`.

- **Applicability:** Clearly the Tsammalex model is limited to data which can be serialized and
  edited as text files. So it can not be applied to non-textual data or too much data. These
  limitations do not exist for the WALS model (although there are limits to the amount of
  data you should store in a PostgreSQL database).


Conclusion
----------

Considering the advantages and disadvantages of these two data curation models,
it seems clear that both are of value. Thus, the value proposition of the CLLD
platform - a uniform API for cross-linguistic data - makes sense even without
support for data curation within the clld software.
