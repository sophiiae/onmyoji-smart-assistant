import sys
import cv2
from rule_image import RuleImage
from rule_ocr import RuleOcr

def load_image(file_path: str):
    img = cv2.imread(file_path)
    height, width, channels = img.shape
    if height != 720 or width != 1280:
        print(f'Image size is {height}x{width}, not 720x1280')
        return None
    return img

def detect_image(file_path: str, target: RuleImage) -> bool:
    img = load_image(file_path)
    result = target.match_target(img)
    if not result:
        print(f"!!Error: no match for [{target.name}].")
    return result

def detect_ocr(file_path: str, target: RuleOcr):
    image = load_image(file_path)
    return target.ocr_single(image)


if __name__ == '__main__':
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from tasks.main_page.assets import MainPageAssets

    target = MainPageAssets.I_GUILD_PACK
    dir = r"D:\OneDrive\Pictures\Pages"
    file = "main_open.png"
    screenshot_path = f"{dir}/{file}"

    print(detect_image(screenshot_path, target))

    from tasks.realm_raid.assets import RealmRaidAssets
    file = "raid_o.png"
    screenshot_path = f"{dir}/{file}"
    target = RealmRaidAssets.O_RAID_TICKET
    print(detect_ocr(screenshot_path, target))
