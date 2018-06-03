# bigeo
Python based software developed for automated geospatial processing.


Bigeo HOW TO’s
=========================

Set Up
------------------------

Setting up the requirements. It is advisable to create your own virtual environments. With in that env, install the dependencies.

pip install fiona
pip install shapely

Reprojecting All files in a directory
Reprojecting all shapefiles on a given directory.

Syntax:

>>>python “/path_to/bigeo.py” projector –indir “/path_to/input_dir” outdir “/path_to/output_dir” --crs “crs_to_use”

Example:

>>>python “bigeo.py” projector –indir “/home/com/Documents/oldshp” --outdir “/home/com/Documents/newshp” --crs “'EPSG:4326'”


Bounding Box
------------------------
Creates a bounding box of a polygon.

Bounding boxes will have the attributes of their respective pylogons.

Syntax:

>>>python “/path_to/bigeo.py” boundingbox –srcfile “/path_to/polygon.shp” --outfile  “/path_to/output.shp” 

Example:

>>>python “bigeo.py” boundingbox –srcfile “countries_polygon.shp” --outfile  “bound_countries.shp” 


Centroids
------------------------
Creates a point on the center of a polygon.

Points will have the attributes of their respective pylogons.

Syntax:

>>>python “/path_to/bigeo.py” centroid –srcfile “/path_to/polygon.shp” --outfile  “/path_to/centroid.shp” 

Example:

>>>python “bigeo.py” boundingbox –srcfile “countries_polygon.shp” --outfile  “bound_countries.shp” 


Representative Point
------------------------
Creates a point guaranteed to be within a polygon.

Syntax:

>>>python “/path_to/bigeo.py” centroid –srcfile “/path_to/polygon.shp” --outfile  “/path_to/reppoint.shp” 

Example:

>>>python “bigeo.py” boundingbox –srcfile “countries_polygon.shp” --outfile  “rep_point_countries.shp” 


