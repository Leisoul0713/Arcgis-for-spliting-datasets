# coding=utf-8
import arcpy
import os


def shp_to_tif(input_shp, output_tif, field, cell_size):
    # 设置工作空间
    arcpy.env.workspace = arcpy.Describe(input_shp).path
    # 启用覆盖现有数据集选项
    arcpy.env.overwriteOutput = True

    # 执行转换
    arcpy.FeatureToRaster_conversion(input_shp, field, output_tif, cell_size)


if __name__ == "__main_":
    # 示例用法
    input_shp = r"C:\workspace\output\Pingtung_resized.shp"
    output_tif = r"C:\workspace\clip_label\Pingtung.tif"

    field = "FID"
    cell_size = 0.5

    shp_to_tif(input_shp, output_tif, field, cell_size)
