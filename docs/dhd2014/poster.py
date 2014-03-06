# -*- encoding: latin1 -*-

from PIL import Image

from pyx import *

text.set(mode="latex", texdebug='debug.tex')
text.preamble(r"""%
\usepackage[latin1]{inputenc}
\usepackage{type1cm,pifont}
\renewcommand\labelitemi{\ding{51}}
\renewcommand{\familydefault}{\sfdefault}
\newcommand\head[1]{{\fontsize{70}{75}\selectfont\bfseries#1\vspace{5mm}\par}}
\newcommand\subhead[1]{{\fontsize{41}{44}\selectfont\bfseries#1\par}}
\renewcommand\section[1]{{\fontsize{34}{37}\selectfont\bfseries#1\vspace{5mm}\par}}
\renewcommand\subsection[1]{{\fontsize{32}{33}\vspace{4mm}\selectfont\bfseries#1\vspace{0mm}\par}}
\renewcommand\normalsize{\fontsize{30}{32}\selectfont}\normalsize
\leftmargini2em\labelwidth1em\labelsep0.5em\parindent0pt\parskip1ex
""")

paperformat = document.paperformat.A0
margin = 0.8
background = 2.3
padding = 0.8

leftpos = rightpos = paperformat.height - margin - background


def box(t, col, **images):
    global leftpos
    global rightpos
    width = paperformat.width - 2*margin - 2*background
    if col:
        width = 0.5*(width - background)
    t = text.text(0, 0, t, [text.parbox(width-2*padding)], texmessages=[text.texmessage.load])
    c = canvas.canvas()


    xpos = margin + background
    if col == 2:
        xpos += width + background
    if not col:
        ypos = min(leftpos, rightpos)
    elif col == 1:
        ypos = leftpos
    else:
        assert col == 2
        ypos = rightpos
    ypos -= t.height + t.depth + 2*padding

    c.draw(path.rect(xpos, ypos, width, t.height + t.depth + 2*padding), [deco.filled([color.gray.white])])

    for marker, filespec in images.items():
        filename, height, xoffset = filespec
        if height:
            x, y = t.marker(marker)
            c.insert(bitmap.bitmap(x+xpos+padding+xoffset, y+ypos+t.depth+padding, Image.open(filename), height=height))
        else:
            c.insert(bitmap.bitmap(xpos, ypos, Image.open(filename), width=width, height=t.height+t.depth+2*padding))

    c.draw(path.rect(xpos, ypos, width, t.height + t.depth + 2*padding), [deco.stroked])

    c.insert(t, [trafo.translate(xpos+padding, ypos+t.depth+padding)])
    if col < 2:
        leftpos = ypos - background
    if col != 1:
        rightpos = ypos - background

    return c

c = canvas.canvas()

c.draw(path.rect(margin, margin, paperformat.width-2*margin, paperformat.height-2*margin),
       [deco.stroked(), deco.filled([color.rgb(1.0, 0.98, 0.9)])])

#
# header
#
c.insert(box(r"""
\begin{center}
\head{CLLD -- Cross-Linguistic Linked Data}
\subhead{Robert Forkel}
\subhead{Department of Linguistics, Max Planck Institute for Evolutionary Anthropology}
\vspace{-5.55mm}
\end{center}
\PyXMarker{header}
""", 0, header=('header2.jpg', 0, 0)))

#
#
#
c.insert(box(r"""
\section{http://clld.org}
\bf{Help recording the world's language diversity heritage by providing interoperable data publication structures.}
""", 1))

#
#
#
c.insert(box(r"""
\section{Cross-linguistic databases on the web}
While several archives for cross-linguistic data exist (among them the DOBES archive),
published databases, i.e. freely accessible, citable datasets are few and far between.
This is the case despite the fact that many linguists collect lexical or typological
datasets, serving as primary sources for their own publications.

\subsection{CLLD -- The strategy}
Since reuse tends to be the determining factor that keeps resources from vanishing,
we want to bridge the gap between data collection and data reuse by
\begin{itemize}
\item publishing databases thereby incentivizing researchers through recognition;
\item using technology that maximizes exposure of our data in the emerging web of data.
\end{itemize}

\subsection{CLLD -- The implementation}
This twofold strategy is implemented by three service components:
\begin{itemize}
\item infrastructural: Glottolog - a comprehensive language catalog and bibliography,
\item structural: Dictionaria -- a dictionary journal and JCLD -- a journal publishing typological databases,
\item technological: \texttt{clld} - a software platform for implementing linguistic database applications
like Glottolog and the journals, but also to serve standalone datasets like WALS, APiCS,
ASJP, IDS.
\end{itemize}
To maximize resuability
\begin{itemize}
\item we provide the data under Open Data Licenses,
\item and the platform as Open Source software under a free license.
\end{itemize}
""", 1))


#c.insert(box(r"""
#\section{The \texttt{clld} software}
#The \texttt{clld} package available at https://github.com/clld/clld provides
#\begin{itemize}
#\item a data model,
#\item an API based on Linked Data principles,
#\item a reference implementation of a data browser.
#\end{itemize}
#""", 1))

c.insert(box(r"""
\subsection{The \texttt{clld} data model}
\vspace{15.5cm}
\PyXMarker{cllderd}

The WOLD incarnation of this data model:

\vspace{8.5cm}
\PyXMarker{wolderd}
""", 1, cllderd=('clld_erd.png', 15.5, 0), wolderd=('wold_erd.png', 8.5, 0)))

#c.insert(box(r"""
#\subsection{The WOLD incarnation of the data model}
#\vspace{8.5cm}
#\PyXMarker{wolderd}
#""", 1, wolderd=('wold_erd.png', 8.5, 0)))

#
#
#
c.insert(box(r"""
\section{Linked Data - the \texttt{clld} API}
\begin{itemize}
\item Defines a unified data access protocol for the web.
\item Well-suited for distributed data providers
%\begin{itemize}
%\item identifiers are URLs which are globally unique,
%\item RDF and OWL provide the vocabulary to merge resources.
%\end{itemize}
\item Provides an easy to implement lowest level of service in a graceful degradation scenario
\end{itemize}

\subsection{Emerging API between data publications and tools}
Linked Data does already provide a data access protocol, i.e. the first part of an API to
be used by tools which analyze, visualize or otherwise reuse data.

\textit{Linked Data Explorer accessing Glottolog Linked Data serialized as RDF/XML.}

\vspace{14cm}
\PyXMarker{rdf}

\textit{The map-making software Tilemill accessing APiCS data in GeoJSON format.}

\vspace{14cm}
\PyXMarker{geojson}

\subsection{Graceful degradation of service}
Providing access to datasets following Linked Data principles can be rather easy, e.g.
by serving static files from an HTTP server. On the other hand we argue that this level
of data access can and should be sufficient to establish an API, i.e. to sustain an
infrastructure of tools on top of the data.
Thus, we use this emerging API as definition of a minimal level of service which is easy
to uphold.

Since maintaining the minimal level of service is rather easy, providing sustainable
services becomes much more likely because scenarios like transfer of ownership become
feasible.
""", 2, rdf=('rdf.png', 14, 0.5), geojson=('geojson.png', 14, 0.5)))


c.insert(box(r"""
\subsection{The data browser}

Viewing a valueset of APiCS Online:

\vspace{12.5cm}
\PyXMarker{valueset}

Viewing a Dictionaria word:

\vspace{13.5cm}
\PyXMarker{unit}

""", 2, valueset=('valueset.png', 12.5, 0), unit=('unit.png', 13.5, 0)))


#
# TODO: graceful degradation of service: Linked Data defineds the API, the API survives, separation of API and visualization may help visualizations to survive, too!
#



c.text(paperformat.width-margin-background, 3, r"\fontsize{16}{18}\selectfont Printed at Universit\"atsrechenzentrum Leipzig", [text.halign.right])

c.writeEPSfile("poster_a4", paperformat=document.paperformat.A4, fittosize=1)
c.writePDFfile("poster_a4", paperformat=document.paperformat.A4, fittosize=1)
c.writeEPSfile("poster_a0", paperformat=document.paperformat.A0)
c.writePDFfile("poster_a0", paperformat=document.paperformat.A0)

# print unit.tocm(leftpos), unit.tocm(rightpos)
