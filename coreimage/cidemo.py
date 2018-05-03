
import sys
import os

import pdb
import pprint
pp = pprint.pprint

from Foundation import *
from AppKit import *
from Quartz.QuartzCore import *


cicategories = (
    kCICategoryDistortionEffect,
    kCICategoryGeometryAdjustment,
    kCICategoryCompositeOperation,
    kCICategoryHalftoneEffect,
    kCICategoryColorAdjustment,
    kCICategoryColorEffect,
    kCICategoryTransition,
    kCICategoryTileEffect,
    kCICategoryGenerator,
    kCICategoryGradient,
    kCICategoryStylize,
    kCICategorySharpen,
    kCICategoryBlur)

ciusages = (
    kCICategoryStillImage,
    kCICategoryVideo,
    kCICategoryInterlaced,
    kCICategoryNonSquarePixels,
    kCICategoryHighDynamicRange)

ciorigin = (
    kCICategoryBuiltIn,
    )


allFilters = CIFilter.filterNamesInCategories_( cicategories )


# pdb.set_trace()

# ctx = NSGraphicsContext.currentContext().CIContext

for cat in cicategories:
    catfilters = CIFilter.filterNamesInCategory_( cat )

    for f in catfilters:
        if f == u"CIPerspectiveTile":
            flt = CIFilter.filterWithName_( f )
            attr = flt.attributes()
            print
            print f
            pp(attr)


# tiles = CIFilter.filterNamesInCategory_(kCICategoryTileEffect)

