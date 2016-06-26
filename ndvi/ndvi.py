import numpy as np
from numpy import nan_to_num, subtract, add, divide, multiply
from osgeo import gdal, gdalconst
from gdal import GetDriverByName

def ndvi(in_nir_band, in_colour_band, in_rows, in_cols, in_geotransform, out_tiff, data_type=gdal.GDT_Float32):

    """
    Performs an NDVI calculation given two input bands, as well as other information that can be retrieved from the
    original image.
    @param in_nir_band A GDAL band object representing the near-infrared image data.
    @type in_nir_band GDALRasterBand
    @param in_colour_band A GDAL band object representing the colour image data.
    @type: in_colour_band GDALRasterBand
    @param in_rows The number of rows in both input bands.
    @type: in_rows int
    @param in_cols The number of columns in both input bands.
    @type: in_cols int
    @param in_geotransform The geographic transformation to be applied to the output image.
    @type in_geotransform Tuple (as returned by GetGeoTransform())
    @param out_tiff Path to the desired output .tif file.
    @type: out_tiff String (should end in ".tif")
    @param data_type Data type of output image.  Valid values are gdal.UInt16 and gdal.Float32.  Default is
                      gdal.Float32
    @type data_type GDALDataType
    @return None
    """

    # Read the input bands as numpy arrays.
    np_nir = in_nir_band.ReadAsArray(0, 0, in_cols, in_rows)
    np_colour = in_colour_band.ReadAsArray(0, 0, in_cols, in_rows)

    # Convert the np arrays to 32-bit floating point to make sure division will occur properly.
    np_nir_as32 = np_nir.astype(np.float32)
    np_colour_as32 = np_colour.astype(np.float32)

    # Calculate the NDVI formula.
    numerator = subtract(np_nir_as32, np_colour_as32)
    denominator = add(np_nir_as32, np_colour_as32)
    result = divide(numerator, denominator)

    # Remove any out-of-bounds areas
    result[result == -0] = -99

    # Initialize a geotiff driver.
    geotiff = GetDriverByName('GTiff')

    # If the desired output is an int16, map the domain [-1,1] to [0,255], create an int16 geotiff with one band and
    # write the contents of the int16 NDVI calculation to it.  Otherwise, create a float32 geotiff with one band and
    # write the contents of the float32 NDVI calculation to it.
    if data_type == gdal.GDT_UInt16:
        ndvi_int8 = multiply((result + 1), (2**7 - 1))
        output = geotiff.Create(out_tiff, in_cols, in_rows, 1, gdal.GDT_Byte)
        output_band = output.GetRasterBand(1)
        output_band.SetNoDataValue(-99)
        output_band.WriteArray(ndvi_int8)
    elif data_type == gdal.GDT_Float32:
        output = geotiff.Create(out_tiff, in_cols, in_rows, 1, gdal.GDT_Float32)
        output_band = output.GetRasterBand(1)
        output_band.SetNoDataValue(-99)
        output_band.WriteArray(result)
    else:
        raise ValueError('Invalid output data type.  Valid types are gdal.UInt16 or gdal.Float32.')

    # Set the geographic transformation as the input.
    output.SetGeoTransform(in_geotransform)

    return None

