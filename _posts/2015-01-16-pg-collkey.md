---
layout: post
title: Default Unicode Collation using pg_collkey
author: Robert Forkel
menu_item: blog
---


A problem which recently popped up again, and which we eventually found a satisfying solution
for is described as *multilingual sorting* in 
[an article about the Oracle database system](http://www.databasejournal.com/features/oracle/article.php/3792166/Multilingual-linguistic-searching-and-sorting-in-Oracle.htm).

Now that article is about Oracle, but we use the open source database system 
[PostgreSQL](http://www.postgresql.org/),
and somewhat surprisingly (because typically PostgreSQL is a beacon when it comes to supporting
standards), the [state of multilingual sorting](http://russ.garrett.co.uk/2009/01/18/unicode-postgres/) 
(or collation in database lingo) in PostgreSQL is sorry.

But the blog post linked above did hint at a possible solution: Use [`pg_collkey`](http://pgxn.org/dist/pg_collkey/0.5.1/)
to interface with the ICU tools for proper unicode collation support.

Proper unicode collation support in our case means, being able to sort multilingual lexical data
in such a way that all linguistically meaningful characters (clicks, IPA symbols, etc.) are
respected. The algorithm which describes such a collation is called 
[Unicode collation algorithm](http://en.wikipedia.org/wiki/Unicode_collation_algorithm),
and implemented in said ICU tools.

Unfortunately the [status of ICU support in PostgreSQL](https://wiki.postgresql.org/wiki/Todo:ICU) hasn't changed much since 2009.
Thus, the `pg_collkey` workaround is still necessary, and turns out to be somewhat tricky.

So here's a recipe to make `pg_collkey` work under Ubuntu 12.04 with PostgreSQL 9.1 and
Ubuntu 14.04 with PostgreSQL 9.3:

1. Install the distribution packages `postgres-server-dev-9.x` and `libicu-dev`.
2. Download the `pg_collkey` package version 0.5.1 from [here](http://www.public-software-group.org/pg_collkey).
3. Build the software ...

Unfortunately, the Makefile provided in the `pg_collkey` package did not work on our target
systems. To help the compiler find the PostgreSQL header files, we had to feed it the
include directory explicitely - rather than relying on `pg_config`. With this tweak, all went
well on Ubuntu 12.04. We had no such
luck on Ubuntu 14.04, though, because the linker flags returned by

    icu-config --ldflags

didn't work. Re-using the linker flags returned by the same command on Ubuntu 12.04 for
14.04 did the trick, though, so 
[here's a Makefile template](https://github.com/clld/clldfabric/blob/master/clldfabric/templates/pg_collkey_Makefile) 
adapted to our needs (replace `__pg_version__` with 9.1 or 9.3):

<pre>
ICU_CFLAGS = `icu-config --cppflags-searchpath`
PG_INCLUDE_DIR = /usr/include/postgresql/__pg_version__/server
PG_PKG_LIB_DIR = `pg_config --pkglibdir`

collkey_icu.so: collkey_icu.o
        ld -shared -o collkey_icu.so collkey_icu.o -ldl -lm   -L/usr/lib/x86_64-linux-gnu -licui18n -licuuc -licudata  -ldl -lm

collkey_icu.o: collkey_icu.c
        gcc -Wall -fPIC $(ICU_CFLAGS) -I $(PG_INCLUDE_DIR) -o collkey_icu.o -c collkey_icu.c

clean:
        rm -f *.o *.so

install:
        install collkey_icu.so $(PG_PKG_LIB_DIR)
</pre>

Using this makefile, running

    make

and

    make install

did work on both target systems.

Now, creating the collkey functions using the sql file provided in the package should work:

    psql -d <dbname> -f collkey_icu.sql

In the [`clld` package](https://github.com/clld/clld), we wrapped support for `pg_collkey` in two functions:

- [one to create the collkey function using sqlalchemy's DDL support](https://github.com/clld/clld/blob/2c3bb850520ef9ca05894850cc0590571b8f5cc2/clld/db/util.py#L20-37)
- and [one to retrieve a function object](https://github.com/clld/clld/blob/2c3bb850520ef9ca05894850cc0590571b8f5cc2/clld/db/util.py#L40-51), suitable for order by clauses or indexes.

If you want to see the unicode collation algorithm in action, look at the sorting of 
[names of species in Tsammalex](http://tsammalex.clld.org/values) (hint: clicks are sorted after latin letters)!
