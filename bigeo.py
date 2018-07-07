# -*- coding: utf-8 -*-

# ----------------------------------------------------------------#                                         
#     _____                                             _____     #
#   || 0100 |\                                       /| 0100 ||   #
#   || 0100_|/ -------  Codes_In_The_Shell  -------- \| 0001 ||   #
#                                                                 #
#-----------------------------------------------------------------#

# ================================= LICENSE ====================================
#
# MIT License
#
# Copyright (c) 2018 Dante Abidin Jr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ================================= LICENSE ====================================

# =========================== DEPENDENCIES / REQUIREMENTS ======================
# pip install fiona         
# pip install shapely
# =========================== DEPENDENCIES / REQUIREMENTS ======================

"""
Bigeo is a python based software developed for automated geospatial processing.
Bigeo comes along with automated processing algorithms that can be run via command line.
See documentation bigeo HOW TOs

Bigeo can also be imported as a third party library.
Refer to bigeo library documentation.

"""

import fiona
import logging
import os
import argparse
from fiona.crs import from_epsg
from shapely.geometry import Point, Polygon, shape, mapping, LineString
from shapely.ops import cascaded_union
import json
import requests
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s :    %(message)s')



####################### BEGIN SECTION FOR CLASSES ##########################

class Reprojector:
    """ Class for reprojecting shp files."""

    def reproject(self, inshpdir, outshpdir, crs):
        """ 
        Function that reprojects shp file crs to a given crs. 

        Reprojected .shp files will be on the outshp \
        directory. Reprojected .shp files will have the same name and all attributes from inshpdir.

        PARAMETER(S):

        : inshpdir : the directory of shp file to be reprojected.

        : outshpdir : the directory of reprojected .shp files. 

        : crs : Projection to use. See fiona crs documentation.

        EXAMPLE(S):

        import bigeo
        reproj = bigeo.Reprojector()
        reproj.reproject("home/path/unprojecteddirectory" , "home/path/projecteddirectory", 'EPSG:4326')

        """

        self.inshpdir = inshpdir

        self.outshpdir = outshpdir

        self.crs = crs

        logging.info('%s %s', "Preparing to reproject files in :", self.inshpdir)

        # Getting all the path of .shp files
        path_of_shp_files= []

        for filename in os.listdir(self.inshpdir):
            if filename.endswith(".shp"): 
                path_of_shp_files.append(os.path.join(self.inshpdir +"/", filename))
                logging.info('%s %s', "shp file found: ", filename)

        # Reading the input .shp files.
        for shpf in path_of_shp_files:

            output_file_name = (os.path.basename(shpf))

            with fiona.open(shpf) as input_shp:

                meta = input_shp.meta
                schema = input_shp.schema

            # Writing the output .shp files
            logging.info('%s %s', "Writing reprojected files to :", self.outshpdir)

            with fiona.open(self.outshpdir + '/' + output_file_name, 'w', crs=self.crs, \
                driver='ESRI Shapefile', schema=schema) as output_shp:

                with fiona.open(shpf) as input_shp:

                    meta = input_shp.meta

                    for f in input_shp:

                        output_shp.write(f)

            logging.info('%s', "Reprojecting done.")


class BoundingBoxCreator():
    """ Class for creating a bounding box from polygon geometries"""

    def getBbox(self, srcfile, outfile):
        """
        Creates a bounding box of polygon.

        Takes a polygon shp file as an input and creates a polygon shp file of bounding boxes 
        for each of the polygon they represent. Bounding boxes will have the attributes of 
        their respective pylogons.

        PARAMETER(S):

        : srcfile : The source polygon shapefile.

        : outfile : The name of the bounding box shapefile to be created. 

        EXAMPLE(S):

        import bigeo
        bb = bigeo.BoundingBoxCreator()
        bb.getBbox('/home/polygon.shp', '/home/boundingbox.shp')

        """

        self.srcfile = srcfile
        self.outfile = outfile

        with fiona.drivers():

            logging.info("Reading file: " + self.srcfile)

            with fiona.open(self.srcfile) as src:
                self.meta = src.meta

                logging.info("Creating output file: " + self.outfile)

                with fiona.open(self.outfile, 'w', **self.meta) as dst:

                    for f in src:

                        logging.info("Creating bounds: " + str(fiona.bounds(f)))

                        bbox = Polygon.from_bounds(fiona.bounds(f)[0], fiona.bounds(f)[1],fiona.bounds(f)[2],fiona.bounds(f)[3])
                        f['geometry'] = mapping(bbox)
                        dst.write(f)

                    logging.info("Done creating bounds for all features. Writing to the specified output file.")


class CentroidCreator():
    """ A class for creating centroids from a polygon shp file. """


    def getCentroids(self, srcfile, outfile):
        """
        Takes a polygon shp file as an input and creates a point shapefile of centroids.

        Points are at the center of its polygon. This point layer will have the attributes from 
        their respective pylogons.

        PARAMETER(S):

        : srcfile : The source polygon shapefile.

        : outfile : The name of the point shapefile to be created.

        EXAMPLE(S):

        import bigeo
        bb = bigeo.CentroidCreator()
        bb.getCentroids('/home/polygon.shp', '/home/boundingbox.shp')

        """

        self.srcfile = srcfile
        self.outfile = outfile

        with fiona.drivers():

            logging.info("Reading file: " + self.srcfile)

            with fiona.open(self.srcfile) as src:
                self.meta = src.meta
                self.meta['schema']['geometry'] = 'Point'

                logging.info("Creating output file: " + self.outfile)

                with fiona.open(self.outfile, 'w', **self.meta) as dst:

                    for f in src:
                        centroid = shape(f['geometry']).centroid
                        f['geometry'] = mapping(centroid)
                        dst.write(f)

                    logging.info("Done creating centroids for all features. Writing to the specified output file.")


class RepresentativePointCreator():
    """ A class for creating Representative Point from a polygon shp file. """


    def getRepresentativePoint(self, srcfile, outfile):
        """
        Takes a polygon shp file as an input and creates a point shapefile of Representative Point.

        Representative Points are point guaranteed to be within a polygon. This point layer will have the attributes from 
        their respective pylogons.

        PARAMETER(S):

        : srcfile : The source polygon shapefile.

        : outfile : The name of the point shapefile to be created.

        EXAMPLE(S):

        import bigeo
        bb = bigeo.RepresentativePointCreator()
        bb.getRepresentativePoint('/home/polygon.shp', '/home/reppoints.shp')

        """

        self.srcfile = srcfile
        self.outfile = outfile

        with fiona.drivers():

            logging.info("Reading file: " + self.srcfile)

            with fiona.open(self.srcfile) as src:
                self.meta = src.meta
                self.meta['schema']['geometry'] = 'Point'

                logging.info("Creating output file: " + self.outfile)

                with fiona.open(self.outfile, 'w', **self.meta) as dst:

                    for f in src:
                        r_points = shape(f['geometry']).representative_point()
                        f['geometry'] = mapping(r_points)
                        dst.write(f)

                    logging.info("Done creating Representative Point for all features. Writing to the specified output file.")


class OpenWeather():
    """ Class for requesting weather data from open weather and creates a shapefile with that data on its location."""

    def getWeather(self, path_ids_file, ow_api, outputshp):
        """
        Requests for the current weather data to openweather.com and generates a shapefile.

        IMPORTANT: This requires api key from openweather. Please register for a free account.
        
        PARAMETER(S):

        : path_ids_file : Path to a file consist of city ids separated by comma with no spaces. (Ex: 1701668,7521309,1724089) See openweather documentation for city ids. 

        : ow_api : Your api key from openweather.

        : outputshp : Output Shapefile.

        EXAMPLE(S):

        import bigeo
        ow = bigeo.OpenWeather()
        ow.getWeather('/home/openweather_id.txt', '462c34bsdgddgded8643643f352a', "/home/output_weather/wx.shp")

        """

        logging.info("Reading file for city ids: " + path_ids_file)

        f = open(path_ids_file,"r")        

        self.api_id = ow_api

        self.ids_txt = f.readline().strip()

        self.outputshp = outputshp

        logging.info("City ids found: " + str(f.readline().strip()))

        logging.info("Requesting using API KEY: " + self.api_id)

        logging.info('Request URL: '+'http://api.openweathermap.org/data/2.5/group?id={ids}&APPID={appid}&units=metric'.format(ids=self.ids_txt, appid=self.api_id))

        self.r = requests.get('http://api.openweathermap.org/data/2.5/group?id={ids}&APPID={appid}&units=metric'.format(ids=self.ids_txt, appid=self.api_id))

        logging.info("Recieved weather response.") 

        wx_json = self.r.json()

        crs = from_epsg(4326)

        schema = {
                'geometry': 'Point',
                'properties': 
                        {
                          'city' :'str', 
                          'humidity': 'int',
                          'pressure': 'int',
                          'temp': 'int',
                          'weather_de': 'str',
                          'wind_dir': 'float',
                          'wind_speed': 'float', 
                        }
                    }

        logging.info("Creating output shapefile: " + self.outputshp)

        with fiona.open(self.outputshp, 'w', crs=crs, schema=schema, driver="ESRI Shapefile") as shpfile:

            for i in wx_json['list']:

                point = {u"type": u"Point", u"coordinates": [i['coord']['lon'], i['coord']['lat']]}
                properties = {
                              'city' : i['name'], 
                              'humidity': i['main']['humidity'],
                              'pressure': i['main']['pressure'],
                              'temp': i['main']['temp'],
                              'weather_de': i['weather'][0]['main'],
                              'wind_dir': i['wind']['deg'],
                              'wind_speed': i['wind']['speed'],
                            }

                shpfile.write({'geometry': point, 'properties': properties})

        logging.info("Writing output shapefile: " + self.outputshp)
        logging.info("Closing file: " + path_ids_file)        
        f.close()


class SnapLineToPoints():
    """ Class to snap lines to points. """

    # object.convex_hull

    def snapLineToPoints(self, pointshp, lineshp, outshpdir):
        """
        Function to snap lines to points.
        """
        pass


# TODO
class DuplicatesRemover():
    # Class to remove duplicates in shapefiles
    # Might just use set() function of python
    pass

# TODO
class PolygonOverlapsRemover():
    # Class to remove overlaps in polygons
    pass

# TODO
class BufferCreator():
    # Class to create a fixed distance buffer
    pass

# TODO
class InvalidGeomRemover():
    # Class to check for invalid geometries
    # might use shapely is_valid and validation.explain_validity(object)
    # buffer(0) will remove invalid geoms. Be cautious as tiny polygons might be created
    pass

# TODO
class MultipartToSinglepart():
    # Convert multipart to singlepart
    pass

# TODO
class FieldTypeRemover():
    # Removes unnecessary fields accordin to type. (ex. DATE TYPE FIELD)
    pass

# TODO


####################### END SECTION FOR CLASSES ##########################



####################### BEGIN SECTION FOR HELPER FUNCTIONS ##########################

def getSchema(path):
    """
    Get the schema of a shapefile.

    PARAMETER(S)

    : path : Path to the .shp file where to copy the schema.

    RETURN(S)

    : schema :  The schema from source .shp

    """

    path = path

    with fiona.open(path) as shpfile:

        schema = shpfile.schema.copy()

        return schema

def getCrs(path):
    """
    Gets the crs of the given .shp file.
    
    PARAMETER(S)

    : path : Path to the .shp file where to copy the crs.

    RETURN(S)

    : crs :  The crs from source .shp

    """

    path = path

    with fiona.open(path) as shpfile:

        crs = shpfile.crs

        return crs

####################### END SECTION FOR HELPER FUNCTIONS ##########################

#################### BEGIN SECTION FOR RUNNING PROCESSING FUNCTIONS ###################

def __run_reprojection():

    logging.info("Running reprojection algorithm.")

    projector = Reprojector()

    projector.reproject(args.indir, args.outdir, args.crs)

def __run_boundingbox():

    logging.info("Running bounding box algorithm.")

    bb = BoundingBoxCreator()

    bb.getBbox(args.srcfile, args.outfile)

def __run_centroids():

    logging.info("Running centroids algorithm.")

    cc = CentroidCreator()

    cc.getCentroids(args.srcfile, args.outfile)

def __run_representativepoint():

    logging.info("Running representative point algorithm.")

    rp = RepresentativePointCreator()

    rp.getRepresentativePoint(args.srcfile, args.outfile)

def __run_openweather():

    logging.info("Running openweather algorithm.")

    ow = OpenWeather()

    ow.getWeather(args.path_ids_file, args.ow_api, args.outfile)



#################### END SECTION FOR RUNNING PROCESSING FUNCTIONS #####################


#################### BEGIN MAIN #####################


def main(algo):

    if algo == 'reprojector':
        __run_reprojection()

    elif algo == 'boundingbox':
        __run_boundingbox()

    elif algo == 'centroids':
        __run_centroids()

    elif algo == 'representativepoint':
        __run_representativepoint()

    elif algo == 'openweather':
        __run_openweather()

    else:
        logging.error('Unkown algorithm: ' + algo)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("algo_processor", help="The processing algorithm to use.")

    parser.add_argument("--indir", help="Directory of shapefiles to reproject.")

    parser.add_argument("--outdir", help="Directory to store the reprojected shapefiles.")

    parser.add_argument("--crs", help="CRS string to use. See fiona documentation for crs available")

    parser.add_argument("--srcfile", help="Source shapefile.")

    parser.add_argument("--outfile", help="Output shapefile.")

    parser.add_argument("--path_ids_file", help="Open weather city ids text file.")

    parser.add_argument("--ow_api", help="Your open weather API key.")


    args = parser.parse_args()

    algo = args.algo_processor
    
    main(algo)

#################### END MAIN #####################

