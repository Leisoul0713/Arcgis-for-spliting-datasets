# coding=utf-8
import arcpy


def clip_and_merge(shapefile, tiff_file, output_folder, output_filename):
    # 获取TIFF文件的地理范围和大小
    desc_tiff = arcpy.Describe(tiff_file)
    tiff_extent = desc_tiff.extent

    # 创建一个几何对象来存储裁剪出来的要素
    merged_feature = None

    # 遍历shapefile的要素
    with arcpy.da.SearchCursor(shapefile, ["SHAPE@"]) as cursor:
        for row in cursor:
            # 获取要素的几何范围
            feature_geom = row[0]
            feature_extent = feature_geom.extent

            # 检查要素范围是否完全包含在TIFF文件范围内
            if (tiff_extent.contains(feature_extent.lowerLeft) and
                    tiff_extent.contains(feature_extent.lowerRight) and
                    tiff_extent.contains(feature_extent.upperLeft) and
                    tiff_extent.contains(feature_extent.upperRight)):
                # 如果没有合并的要素，则将当前要素直接赋值给合并的要素
                if merged_feature is None:
                    merged_feature = feature_geom
                # 否则，将当前要素与已合并的要素进行合并
                else:
                    try:
                        merged_feature = merged_feature.union(feature_geom)
                    except ValueError as e:
                        print("合并要素时发生错误：{}".format(str(e)))

    # 如果存在合并的要素，则保存为一个文件
    if merged_feature:
        # 构建输出路径
        merged_output = output_folder + "\\" + output_filename

        # 保存合并后的要素为一个文件
        arcpy.CopyFeatures_management(merged_feature, merged_output)

        # 设置输出的要素类的空间参考与 TIFF 文件相同
        arcpy.DefineProjection_management(merged_output, desc_tiff.spatialReference)

        print("裁剪后的要素已合并，并保存为{}".format(merged_output))
    else:
        print("没有要素需要合并。")


if __name__ == "__main__":
    # 输入文件路径
    shapefile = r"C:\workspace\original\asd\merge.shp"
    tiff_file = r"C:\workspace\original\Pingtung.tif"

    # 设置输出文件夹路径和文件名
    output_folder = r"C:\workspace\feature"  # 输出文件夹路径
    output_filename = "Pingtung.shp"  # 输出文件名

    # 调用函数
    clip_and_merge(shapefile, tiff_file, output_folder, output_filename)
