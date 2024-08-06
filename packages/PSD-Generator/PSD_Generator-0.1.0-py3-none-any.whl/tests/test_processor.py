import unittest
from PSD_Generator.processor import process_image
import subprocess

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        try:
            subprocess.check_call(['convert', '--version'])
        except subprocess.CalledProcessError:
            self.fail("ImageMagick is not installed or not found in the system PATH.")

    def test_process_image(self):
        image_url = "https://s3.ap-south-1.amazonaws.com/sunniva.ai/Generated_Image/9f7eff5a5dd3b5c4d6e4506913483e343414c17b57367eebe28e6faf9d576a64.JPG"
        result = process_image(image_url, method_type=1, bandwidth=10, is_dynamic=1, num_colors=5)
        self.assertTrue(result.endswith('.psd'))

if __name__ == '__main__':
    unittest.main()