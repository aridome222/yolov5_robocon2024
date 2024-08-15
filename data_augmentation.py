import os
from PIL import Image
import torchvision
from torchvision import transforms
import torchvision.transforms.functional as F

# 指定領域の切り出しと拡大処理
def crop_and_resize(image, crop_box):
    # 画像の元のサイズを取得
    original_width, original_height = image.size
    
    # 指定領域を切り出し
    image_cropped = image.crop(crop_box)
    
    # 元のサイズにリサイズ
    image_resized = F.resize(image_cropped, (original_height, original_width))
    
    return image_resized

# 画像の左右反転処理（pの確率で反転する）
DA_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0),
])

# 入力ディレクトリと出力ディレクトリのパス
input_dir = './fig_data/2024_data/jpeg'
output_dir = './fig_data/2024_data/cut_data'

# 出力ディレクトリが存在しない場合は作成する
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 切り出す領域を指定 (left, upper, right, lower)
crop_box = (410, 0, 1230, 616)

# データを読み込み、変換し、保存する処理
for filename in os.listdir(input_dir):
    if filename.endswith('.jpeg'):
        # 画像を開く
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path)

        # 変換処理を適用
        transformed_img = DA_transform(img)

        # 指定領域の切り出しと元サイズへのリサイズを適用
        transformed_img = crop_and_resize(img, crop_box)

        # 新しいファイル名を作成
        new_filename = filename.replace('.jpeg', '_cuted.jpeg')

        # 画像を保存する（再度PIL Image形式に変換して保存）
        save_path = os.path.join(output_dir, new_filename)
        transformed_img.save(save_path)

        print(f"{filename} を処理し、{save_path} に保存しました。")

