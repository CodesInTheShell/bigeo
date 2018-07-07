
import bigeo
import unittest

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s :    %(message)s')


# class Test_Reprojector(unittest.TestCase):    
    
#     def test_reprojector(self):

#         projector = bigeo.Reprojector()

#         logging.info("Note: Use your own test data for this test.")

#         # Use your own test data here for input and output directories.
#         projector.reproject('/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data', \
#             '/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/outdir', \
#             'EPSG:4326')

# class Test_BoundingBox(unittest.TestCase):    
    
#     def test_boundingbox(self):

#         bb = bigeo.BoundingBoxCreator()

#         logging.info("Note: Use your own test data for this test. Use polygon shapefile.")

#         # Use your own test data here for input and output directories.
#         # Use polygon shapefile.
#         bb.getBbox('/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/polygon.shp', \
#             '/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/outdir/boundingbox.shp')

# class Test_CentroidCreator(unittest.TestCase):    
    
#     def test_getCentroids(self):

#         cc = bigeo.CentroidCreator()

#         logging.info("Note: Use your own test data for this test. Use polygon shapefile.")

#         # Use your own test data here for input and output directories.
#         # Use polygon shapefile.
#         cc.getCentroids('/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/outdir/boundingbox.shp', \
#             '/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/outdir/centroids.shp')

# class Test_RepresentativePointCreator(unittest.TestCase):    
    
#     def test_getRepresentativePoint(self):

#         rp = bigeo.RepresentativePointCreator()

#         logging.info("Note: Use your own test data for this test. Use polygon shapefile.")

#         # Use your own test data here for input and output directories.
#         # Use polygon shapefile.
#         rp.getRepresentativePoint('/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/polygon.shp', \
#             '/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/outdir/reppoints.shp')

# class Test_OpenWeather(unittest.TestCase):    
    
#     def test_getWeather(self):

#         logging.info("Note: Use your own test data for this test.")

#         ow = bigeo.OpenWeather()

#         ow.getWeather('/home/dantex/Documents/DEVELOPMENTS/Test Data/openweather_id.txt', 'BLEH', "/home/dantex/Documents/DEVELOPMENTS/Test Data/output_weather/wx.shp")


class Test_SnapLineToPoints(unittest.TestCase):

    def test_snapLineToPoints(self):

        snapper = bigeo.SnapLineToPoints()

        snapper.snapLineToPoints('/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/point.shp', \
            '/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/unsnap_line.shp', \
            '/home/dantex/Documents/DEVELOPMENTS/Test Data/Basic Test Data/outdir')



if __name__ == '__main__':
    unittest.main()

    