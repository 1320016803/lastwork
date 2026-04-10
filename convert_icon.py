
from PIL import Image
import sys
from pathlib import Path

def create_ico(input_path, output_path):
    """将图片转换为多尺寸的 ICO 图标"""
    img = Image.open(input_path)
    
    # ICO 需要的尺寸（从大到小）
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    
    # 保存为 ICO
    img.save(output_path, format='ICO', sizes=sizes)
    print("OK: Icon saved to:", output_path)

if __name__ == "__main__":
    # 假设输入图片是 cute-timer.png.png
    input_file = Path(__file__).parent / "cute-timer.png.png"
    output_file = Path(__file__).parent / "assets" / "app.ico"
    
    if input_file.exists():
        create_ico(input_file, output_file)
    else:
        print("ERROR: File not found:", input_file)
        print("Please save the image as cute-timer.png in the project root")

