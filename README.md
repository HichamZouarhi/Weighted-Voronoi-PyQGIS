This is a python script that takes a set of points as vector layer
and returns a weighted voronoi diagram using pyQGIS

* How it works :
  
  1- convert the vector file to a raster file with a single band to wich the value of the weight is assigned
  
  2- compute for each points the euclidean distance grid
  
  3- apply the weights to the distance, in this script I divide the distance by the weight ( you can change it to a more suited mathematical transformation)
  
  4- assign each pixel to the nearest points considering its weight
  
  5- convert the result raster to a vector layer (shapefile)
  
* How to use it :

  get your vector layer and name the weight attribute z
  
  launch the python console in QGIS and tape the following :
  
      import sys
      sys.argv="Path/to/your/vector/layer"
      execfile("Path/to/this/script.py")
    
NB: the input vector file must be an ESRI shapefile
