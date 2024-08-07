import unittest
from image_to_psd.processor import process_image
import subprocess

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        try:
            subprocess.check_call(['convert', '--version'])
        except subprocess.CalledProcessError:
            self.fail("ImageMagick is not installed or not found in the system PATH.")

    def test_process_image(self):
        image_url = "https://example.com/image.jpg"
        result = process_image(image_url, method_type=1, bandwidth=25, is_dynamic=1, num_colors=5, save_layers=False)
        self.assertTrue(result.endswith('.psd'))

if __name__ == '__main__':
    unittest.main()