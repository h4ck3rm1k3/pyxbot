osmbot
======

An fork of emacen's OSM bot written in Python (no relation to the real Xybot).

scripts/dup_houses.py
=====================
The dup_houses bot allows you to draw buildings over house points and it will transfer the tags to them.
this is good for tracing over buildings where the house numbers are already in place. 
This uses the pure python quadtree library https://github.com/h4ck3rm1k3/quadpy/ to determine the containment, and a simple bbox around the building. Aborts if more than one building is found. 
Also if a building is used by more than one node, it will throw an exception, you will have to resolve that manually.