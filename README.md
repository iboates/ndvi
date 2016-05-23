# ndvi
A python function that uses GDAL and numpy to perform an NDVI calculation given a NIR band and a colour band

Contains two functions: ndvi() and ndvi_float().

ndvi() creates an int16 .tiff file (range between 0 and 255)

ndvi_float() creates a float32 tiff file (range between -1 and 1).
