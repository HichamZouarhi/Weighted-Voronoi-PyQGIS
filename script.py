from qgis.core import *
from osgeo import gdal

pointsVector=QgsVectorLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/points.shp', 'points', 'ogr')
QgsMapLayerRegistry.instance().addMapLayer(pointsVector)

rasterPoints=QgsRasterLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterPoints', 'rasterPoints')
QgsMapLayerRegistry.instance().addMapLayer(rasterPoints)

dataset=gdal.Open('./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterPoints')
numpy_array=dataset.ReadAsArray()

width,height=numpy_array.shape
points=[]

#get all the weighted points from the raster
for row in range(0,height):
	for col in range(0,width):
		if(numpy_array[row,col]!=0):
			print numpy_array[row,col]
			points.append([row, col, numpy_array[row,col]])

for i in range(0, len(points)):
	print points[i]

#print "all cells with a weighted value"