from qgis.core import *
from osgeo import gdal
import math
import numpy as np

pointsVector=QgsVectorLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/points.shp', 'points', 'ogr')
QgsMapLayerRegistry.instance().addMapLayer(pointsVector)

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
			#print numpy_array[row,col]
			points.append([row, col, numpy_array[row,col]])



print "compute the weighted distance grid for each point"
distanceGrids=[]
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

outFileName='./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterVoronoi.tiff'
driver=gdal.GetDriverByName('GTiff')
output=driver.Create(outFileName, height, width, 1, gdal.GDT_Byte)
output.SetGeoTransform(dataset.GetGeoTransform())
output.SetProjection(dataset.GetProjection())
output.GetRasterBand(1).WriteArray(distanceGrid)
rasterVoronoi=QgsRasterLayer('./Desktop/PyQGIS_Tests/Weighted Voronoi/rasterVoronoi.tiff')
QgsMapLayerRegistry.instance().addMapLayer(rasterVoronoi)
#distanceGrids.append(distanceGrid)


#print "all cells with a weighted value"