# -*- coding: utf-8 -*-
import os.path

from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import keyword, LibraryComponent


class Selenium2Screenshots(object):
    """This library provides a few Robot Framework resources for annotating
    and cropping screenshots taken with Selenium2Library.

    """
    def __init__(self):
        self.import_Selenium2Screenshots_resources()

    def import_Selenium2Screenshots_resources(self):
        """Import Selenium2Screenshots user keywords.
        """
        BuiltIn().import_resource('Selenium2Screenshots/keywords.robot')
        sl = BuiltIn().get_library_instance('Selenium2Library')
        sl.add_library_components([SeleniumChromeKeywords(sl)])
        BuiltIn().reload_library('Selenium2Library')


scale_factor = 1.0


class Image(object):

    def crop_image(self, output_dir, filename, left, top, width, height):
        """Crop the saved image with given filename for the given dimensions.
        """
        from PIL import Image

        img = Image.open(os.path.join(output_dir, filename))
        left, top, width, height = (
           left * scale_factor, top * scale_factor,
           width * scale_factor, height * scale_factor
        )
        box = (int(left), int(top), int(left + width), int(top + height))

        area = img.crop(box)

        with open(os.path.join(output_dir, filename), 'wb') as output:
            area.save(output, 'png')


class SeleniumChromeKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def set_devicescalefactor(self, factor):
        factor = float(factor)
        self.ctx.driver.execute_cdp_cmd(
            "Page.setDeviceMetricsOverride",
            {
                "deviceScaleFactor": factor,
                "width": 0,
                "height": 0,
                "mobile": False,
            }
        )
        global scale_factor
        scale_factor = factor
