import numpy as np
from osgeo import gdal, gdalconst

def ndvi(in_nir_band, in_colour_band, in_rows, in_cols, in_geotransform, out_tiff):

    np_nir = in_nir_band.ReadAsArray(0, 0, in_cols, in_rows)
    np_colour = in_colour_band.ReadAsArray(0, 0, in_cols, in_rows)

    np_nir_as32 = np_nir.astype(np.float32)
    np_colour_as32 = np_colour.astype(np.float32)

    numerator = np.subtract(np_nir_as32, np_colour_as32)
    denominator = np.add(np_nir_as32, np_colour_as32)
    result = np.divide(numerator, denominator)

    ndvi = np.multiply((result + 1), (2**7 - 1))

    geotiff = gdal.GetDriverByName('GTiff')
    output = geotiff.Create(out_tiff, in_cols, in_rows, 1, gdal.GDT_UInt16)
    output.SetGeoTransform(in_geotransform)

    output.GetRasterBand(1).WriteArray(ndvi)

    return None

def ndvi_float(in_nir_band, in_colour_band, in_rows, in_cols, in_geotransform, out_tiff):

    np.seterr(invalid='ignore')

    np_nir = in_nir_band.ReadAsArray(0, 0, in_cols, in_rows)
    np_colour = in_colour_band.ReadAsArray(0, 0, in_cols, in_rows)

    np_nir_as32 = np_nir.astype(np.float32)
    np_colour_as32 = np_colour.astype(np.float32)

    numerator = np.subtract(np_nir_as32, np_colour_as32)
    denominator = np.add(np_nir_as32, np_colour_as32)
    result = np.divide(numerator, denominator)
    result2 = np.nan_to_num(result)

    geotiff = gdal.GetDriverByName('GTiff')
    output = geotiff.Create(out_tiff, in_cols, in_rows, 1, gdal.GDT_Float32)
    output.SetGeoTransform(in_geotransform)

    output.GetRasterBand(1).WriteArray(result2)

    return None

nir_tiff = gdal.Open(r'path to nir image here')
nir_band = nir_tiff.GetRasterBand(1)
colour_tiff = gdal.Open(r'path to colour image here')
colour_band = red_tiff.GetRasterBand(1)
rows, cols, geotransform = nir_tiff.RasterYSize, nir_tiff.RasterXSize, nir_tiff.GetGeoTransform()
out_tiff1 = r'path to output tiff here'
out_tiff2 = r'path to output tiff here'

ndvi(nir_band, colour_band, rows, cols, geotransform, out_tiff)
ndvi_float(nir_band, colour_band, rows, cols, geotransform, out_tiff)

print('done')
