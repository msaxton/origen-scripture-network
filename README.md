# Origen's Scriptural Network

## Project Overview

Origen of Alexandria's homilies are rich tapestries of scritpural citation. These scriptural citations serve many 
purposes in Origen's work, sometimes they are used to prove a point, sometimes they are used to raise a question, and 
sometimes one citation is used to clarify the meaning of another citation. By way of analogy, the citations can be
thought of as *characters* driving the *plot* of the homily. In fact, the richness of Origen's homilies comes from the
ways that these characters interact with one another. Following that analogy, these project will use *network analysis*
as a means of visualizing and analyzing the relationships between scriptural citations in Origen's *Homilies on
Jeremiah*. 

## Description

*Network Analysis* has been used in a number of different fields including the mathematics, sociology, and literature. 
A network can be any structure that contains individual elements, called "nodes" which have relationships, called
"edges," with other individual elements. In this case, the nodes are scriptural citations and the edges are a common
context. For the purposes of this project, I am making two methodological assumptions: First, regarding nodes I am taking a citation to
be a modern chapter of the Bible rather than a chapter and verse. So, for example, if Origen cites Genesis 23:10 I will
take the node to be Genesis 23. I am aware of two disadvantages here: Origen himself was not working with modern
 versification and the verses in a biblical chapter may be very diverse. I am hoping that these disadvantages are
 outweighed by the utility of working on the chapter level. Since this is a work in progress, I may revisit this
 assumption as I move on. The second assumption I am making relates to the edges. What should count as a "common 
 context?" In other words, at what point are two citations in a relationship? For the purposes of this project I
 consider any two or more citations to be in a relationship if they are cited in the same paragraph as defined by the
 critical edition. For this project I am using Klostermann's critical edition which has been made available in xml
 format by the [Open Greek and Latin Project](https://opengreekandlatin.github.io/First1KGreek/).
 

There are three major steps to this project:
 ##### 1. Gather and process data

Critical editions of Origen's homilies have been made available by the 
[Open Greek and Latin Project](https://opengreekandlatin.github.io/First1KGreek/). For this beginning of these project I
will be using data from 
[Origenes, In Jeremiam (Homiliae 1-11), Origenes Werke Volume 3, Klostermann, Hinrichs 1901](https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg2042/tlg021/tlg2042.tlg021.opp-grc1.xml)
and 
[Origenes, In Jeremiam (Homiliae 12-20), Origenes Werke Volume 3, Klostermann, Hinrichs 1901](https://raw.githubusercontent.com/OpenGreekAndLatin/First1KGreek/master/data/tlg2042/tlg021/tlg2042.tlg021.opp-grc1.xml).
Using a python script I will extract the citations from the notes which occur together in the critical edition's 
paragraphs. After extracting the citations each citation will be given a numeric id (for later processing) and will be
grouped with other citations from the same paragraph in the critical edition. This data will then be formatted in a json
file containing a list of nodes (citations) and a list of edges (relationships). Json is a convenient format to use with
d3.js.
 
##### 2. Construct network diagram
I will be using d3.js to visualize the scriptural network from Origen's *Homilies on Jeremiah*. d3.js is a flexible and
open-source data visualization library which is particularly useful for presenting  interactive data visualizations on 
the web.

##### 3. Analysis
Data visualizations are interpretive objects. That is to say, they provide interpretations of data but also need to be
interpreted themselves. After visualizing the scriptural network from Origen's homilies, I will then provide an analysis
of how the citations, as characters, interact with one another and drive the plot of Origen's homilies.