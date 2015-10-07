*This document is a work in progress*

# Introduction to YeezyScore

Description: This project compares Storm Trident with Spark Streaming. While the two come from differing ends of the processing software universe, these two features in particular are considered 'microbatching' stream processing technologies. 

---
 
Project for Data Engineering Fellowship at Insight Data Science '15C

---

Table of Contents:

1. [Introduction](#Introduction)
2. [Technologies](#Technologies)
3. [Application](#Application)
---
# Introduction

Initially I wanted to create a sneaker analytics related project, but then knowing nothing about software and hearing vague advice of, "pick the right tool for the job" led me on a path of comparing available options. I started with the two most popular choices: Apache Storm and Apache Spark. Further investigation into each led me to find out that both have micro-batching capabilities. This was the basis of comparison.

---

# Technologies

* AWS Platform
* Ingestion
	* Kafka
* Streaming
    * Spark Streaming
    * Storm Trident
* Datastore
    * Cassandra
* Front End
	* [Flask](http://flask.pocoo.org/)
	* [Cubism](http://square.github.io/cubism/)
    * [LeafletJS](http://leafletjs.com)
    * [Highcharts](http://highcharts.com)
* Open Source
    * Pyleus
    * PySpark
    * Python-Driver

# Application

Here's an example of using stream processing software to create a trendwatching dashboard

![](http://de.katychuang.me/static/preview.gif)
