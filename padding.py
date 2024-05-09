# -*- coding: utf-8 -*-
import arcpy
from arcpy import env
from arcpy.sa import *

# 设置工作环境
env.workspace = r"C:\Your\Workspace"
env.overwriteOutput = True

# 输入TIF图像
input_tif = r"C:\workspace\asd\tif1.tif"
# 输入需要填充的图像
fill_image = r"C:\workspace\clip_label\Pingtung.tif"
# 输出路径
output_tif = r"C:\workspace\bnm\asdf.tif"

# 提取边界
boundaries = arcpy.RasterToPolygon_conversion(input_tif, "in_memory/boundaries", "NO_SIMPLIFY")
print("boundaries sucessful ")
# 为填充图像创建空白栅格
arcpy.PolygonToRaster_conversion(boundaries, "OBJECTID", "in_memory/boundary_raster", cellsize=input_tif)
print("ceate sucessful")
# 填充到边界内
filled_raster = arcpy.sa.ExtractByMask(fill_image, "in_memory/boundary_raster")
print("padding sucessful")
# 保存结果
filled_raster.save(output_tif)

# 清理临时文件
arcpy.Delete_management("in_memory")
