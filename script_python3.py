from qgis.core import *
from osgeo import gdal
import math
import numpy as np
import os

MARGIN = 0.01

def weightedFunction(x, y, x0, y0, weight):
	# the current weighted Function is a simple sqrt((x-x0)^1 + (y-y0)^2)/w
	return math.sqrt((x - x0) ** 2 + (y - y0) ** 2) / weight

#Get the points vector layer
pointsVector = QgsVectorLayer(sys.argv, 'points', 'ogr')
#Add the vector layer to the map layer registry
QgsProject.instance().addMapLayer(pointsVector)

#get layer extents with a small margin to avoid ignoring points on bounding box's limit
bounding_box = pointsVector.extent()
extent_args = "-te " + str(bounding_box.xMinimum() - MARGIN) \
    + " " + str(bounding_box.yMinimum() - MARGIN) \
    + " " + str(bounding_box.xMaximum() + MARGIN) \
    + " " + str(bounding_box.yMaximum() + MARGIN)

os.system('gdal_rasterize -a z -ts 1000 1000 ' + extent_args + ' -l points "' + sys.argv + '" "./rasterPoints"')


rasterPoints=QgsRasterLayer('./rasterPoints', 'rasterPoints')
QgsProject.instance().addMapLayer(rasterPoints)

dataset = gdal.Open('./rasterPoints')
numpy_array = dataset.ReadAsArray()

width, height = numpy_array.shape
points = []

#get all the weighted points from the raster
print("get the points with their weights from raster")
for row in range(height):
	for col in range(width):
		if(numpy_array[row, col] != 0):
			print(str(numpy_array[row, col]) + " at point : " + str(row) + " , " + str(col))
			points.append([row, col, numpy_array[row,col]])

print("compute the weighted distance grid for each point")

distanceGrid = np.zeros(shape = (height, width))
for row in range(height):
	for col in range(width):
		index = 0
		min_distance = weightedFunction(row, col, points[0][0], points[0][1], points[0][2])
		for i in range(1, (len(points))):
			weightedDistance = weightedFunction(row, col, points[i][0], points[i][1], points[i][2])
			if(weightedDistance < min_distance):
				min_distance = weightedDistance
				index = i
		distanceGrid[row, col] = index

#save the distance grid as an output raster
#output file name ( path to where to save the raster file )
print("save distance grid as raster GTiff")
outFileName = './rasterVoronoi.tiff'
#call the driver for the chosen format from GDAL
driver = gdal.GetDriverByName('GTiff')
#Create the file with dimensions of the input raster ( rasterized points )
output = driver.Create(outFileName, height, width, 1, gdal.GDT_Byte)
#set the Raster transformation of the resulting raster
output.SetGeoTransform(dataset.GetGeoTransform())
#set the projection of the resulting raster
output.SetProjection(dataset.GetProjection())
#insert data to the resulting raster in band 1 from the weighted distance grid
output.GetRasterBand(1).WriteArray(distanceGrid)
#Call the raster output file
rasterVoronoi = QgsRasterLayer('./rasterVoronoi.tiff', 'weighted Raster')
#Add it to the map layer registry ( display it on the map)
QgsProject.instance().addMapLayer(rasterVoronoi)

#polygonize the result raster
print("convert raster to shapefile")
os.system('gdal_polygonize.bat ./rasterVoronoi.tiff ./WeightedVoronoi.shp -b 1 -f "ESRI Shapefile" weighted')
weightedVoronoiVector = QgsVectorLayer('./WeightedVoronoi.shp', 'weighted voronoi', 'ogr')
#load the vector weighted voronoi diagram
QgsProject.instance().addMapLayer(weightedVoronoiVector)
print("End of script")