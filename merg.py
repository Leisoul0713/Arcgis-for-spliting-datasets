from PIL import Image


def linear_stretching(image):
    # 获取图像的最小和最大像素值
    min_val = image.getextrema()[0]
    max_val = image.getextrema()[1]

    # 线性拉伸
    stretched_image = image.point(lambda x: 255 * (x - min_val) / (max_val - min_val))

    return stretched_image


def tiff_to_png(tiff_path, output_path):
    # 读取TIFF图像
    tiff_image = Image.open(tiff_path)

    # 线性拉伸图像的像素值范围到0到255
    stretched_image = linear_stretching(tiff_image)

    # 将TIFF转换为PNG并保存
    stretched_image = stretched_image.convert("RGB")
    stretched_image.save(output_path)


def merge_rgb(tiff_paths, output_path):
    # 分别读取三个频段的TIFF图像并转换为灰度模式
    red_band = Image.open(tiff_paths[0]).convert("I;16")
    green_band = Image.open(tiff_paths[1]).convert("I;16")
    blue_band = Image.open(tiff_paths[2]).convert("I;16")

    # 调整大小为相同的大小
    red_band = red_band.resize(green_band.size)
    blue_band = blue_band.resize(green_band.size)

    # 合成彩色影像
    merged_image = Image.merge("RGB", (red_band, green_band, blue_band))

    # 保存合成的彩色影像
    merged_image.save(output_path)


if __name__ == "__main__":
    # 输入的三个频段TIFF图像路径
    tiff_paths = ["Red_8887.TIF", "Green_8887.TIF", "Blue_8887.TIF"]

    # 输出的合成彩色影像路径
    png_output_paths = ["red_stretched.png", "green_stretched.png", "blue_stretched.png"]

    # 对每个频段的TIFF图像进行线性拉伸并转换为PNG格式
    for tiff_path, png_output_path in zip(tiff_paths, png_output_paths):
        tiff_to_png(tiff_path, png_output_path)

    # 合成彩色影像
    merge_rgb(png_output_paths, "merged_image.png")
