import os
from pathlib import Path
import sys
from ppadb.client import Client as AdbClient
import numpy as np
import cv2

from module.config.config import Config

class Connection():
    config: Config
    host = "127.0.0.1"
    port = None
    adb: AdbClient
    device = None
    screenshot = None

    def __init__(self, config: Config) -> None:
        self.config = config

        if not self.host or not self.port:
            serial = config.model.script.device.serial.split(":")
            self.host = serial[0]
            self.port = int(serial[1])

        os.system("adb devices")
        self.device = self.connect_device()

    def connect_device(self):
        self.adb = AdbClient(host=self.host, port=5037)
        print(f"connecting to {self.host}:{self.port}")

        self.adb.remote_connect(self.host, self.port)
        self.device = self.adb.device(f"{self.host}:{self.port}")
        return self.device

    def decode_image(self, image):
        image_bytes = np.array(image, dtype=np.uint8)
        image = cv2.imdecode(np.frombuffer(
            image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image

    def get_screenshot(self):
        """
        Returns:
            np.ndarray:
        """
        if self.device is None:
            print("Error: no device detected")
            return
        image = self.device.screencap()
        image = self.decode_image(image)
        return image

    def capture_screenshot(self, filepath):
        image = self.get_screenshot()
        if image is None:
            print("no image captured.")
            return
        cv2.imwrite(filepath, image)
        # cv2.waitKey(500)
        print(f"got a screenshot in {filepath}")


# test
if __name__ == "__main__":
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from module.config.config import Config

    name = sys.argv[1]
    config = Config("osa")
    cn = Connection(config)
    filepath = Path.cwd() / f"{name}.png"
    cn.capture_screenshot(filepath)
