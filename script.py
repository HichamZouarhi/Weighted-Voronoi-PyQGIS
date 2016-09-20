from qgis.core import *
from osgeo import gdal
import math
import numpy as np
import os

#Get the points vector layer
pointsVector=QgsVectorLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/points.shp', 'points', 'ogr')
#Add the vector layer to the map layer registry
QgsMapLayerRegistry.instance().addMapLayer(pointsVector)

os.system('gdal_rasterize -a z -ts 1000 1000 -l points "/home/user/Desktop/PyQGIS_Tests/Weighted Voronoi/points.shp" "/home/user/Desktop/PyQGIS_Tests/Weighted Voronoi/rasterPoints"')


rasterPoints=QgsRasterLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterPoints', 'rasterPoints')
QgsMapLayerRegistry.instance().addMapLayer(rasterPoints)

dataset=gdal.Open('./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterPoints')
numpy_array=dataset.ReadAsArray()

width,height=numpy_array.shape
points=[]

#get all the weighted points from the raster
print "get the points with their weights from raster"
for row in range(0,height):
	for col in range(0,width):
		if(numpy_array[row,col]!=0):
			print numpy_array[row,col]
			points.append([row, col, numpy_array[row,col]])



# print "compute the weighted distance grid for each point"

distanceGrid=np.zeros(shape=(height, width))
for row in range(0,height):
	for col in range(0,width):
		index=0
		min=math.sqrt((row-points[0][0])**2+(col-points[0][1])**2)/points[0][2]
		for i in range(1, (len(points)-1)):
			weightedDistance=math.sqrt((row-points[i][0])**2+(col-points[i][1])**2)/points[i][2]
			if(weightedDistance<min):
				min=weightedDistance
				index=i
		distanceGrid[row,col]=index

#save the distance grd as an output raster
#output file name ( path to where to save the raster file )
outFileName='./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterVoronoi.tiff'
#call the driver for the chosen format from GDAL
driver=gdal.GetDriverByName('GTiff')
#Create the file with dimensions of the input raster ( rasterized points )
output=driver.Create(outFileName, height, width, 1, gdal.GDT_Byte)
#set the Raster transformation of the resulting raster
output.SetGeoTransform(dataset.GetGeoTransform())
#set the projection of the resulting raster
output.SetProjection(dataset.GetProjection())
#insert data to the resulting raster in band 1 from the weighted distance grid
output.GetRasterBand(1).WriteArray(distanceGrid)
#Call the raster output file
rasterVoronoi=QgsRasterLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterVoronoi.tiff', 'weighted Raster')
#Add it to the map layer registry ( display it on the map)
QgsMapLayerRegistry.instance().addMapLayer(rasterVoronoi)

#polygonize the result raster
os.system('gdal_polygonize.py "/home/user/Desktop/PyQGIS_Tests/Weighted Voronoi/rasterVoronoi.tiff" -f "ESRI Shapefile" "/home/user/Desktop/PyQGIS_Tests/Weighted Voronoi/shp/WeightedVoronoi/WeightedVoronoi.shp" WeightedVoronoi')

weightedVoronoiVector=QgsVectorLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/shp/WeightedVoronoi/WeightedVoronoi.shp', 'weighted voronoi', 'ogr')
#load the vector weighted voronoi diagram
QgsMapLayerRegistry.instance().addMapLayer(weightedVoronoiVector)
# #print "all cells with a weighted value"