# ndvi
A python function that uses GDAL and numpy to perform an NDVI calculation given a NIR band and a colour band.

User can specify output as a 32-bit floating point image or a 16-bit unsigned integer image.

Comes with a small clipping of a LANDSAT-8 surface reflectance image of Halifax, Nova Scotia, Canada for demo purposes.  You should be able to demo it right out of the box provided the images are in the same directory as the script itself.

Requires osgeo installation of GDAL and numpy (https://trac.osgeo.org/gdal/wiki/GdalOgrInPython)

More info on NDVI: https://en.wikipedia.org/wiki/Normalized_Difference_Vegetation_Index
