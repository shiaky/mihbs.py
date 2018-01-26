#!/usr/bin/env python3

import sys
sys.path.append('../common')

import util
import stability_benchmark as stb


if __name__ == '__main__':
    # create new benchmark instance
    stabbench = stb.StabilityBenchmark()

    # define a set of attacks
    import attacks as at
    aAttacks = [
        # scale uniform
        (at.scale, {"lScalefactorX": 0.25, "lScaleFactorY": 0.25}),
        (at.scale, {"lScalefactorX": 0.5, "lScaleFactorY": 0.5}),
        (at.scale, {"lScalefactorX": 0.75, "lScaleFactorY": 0.75}),
        (at.scale, {"lScalefactorX": 0.9, "lScaleFactorY": 0.9}),
        (at.scale, {"lScalefactorX": 1.1, "lScaleFactorY": 1.1}),
        (at.scale, {"lScalefactorX": 1.5, "lScaleFactorY": 1.5}),
        (at.scale, {"lScalefactorX": 2, "lScaleFactorY": 2}),
        (at.scale, {"lScalefactorX": 4, "lScaleFactorY": 4}),
        # (0.25,0.25)(0.5,0.5)(0.75,0.75)(0.9,0.9)(1.1,1.1)(1.5,1.5)(2,2)(4,4)

        # scale nonuniform - X
        (at.scale, {"lScalefactorX": 0.25, "lScaleFactorY": 1}),
        (at.scale, {"lScalefactorX": 0.5, "lScaleFactorY": 1}),
        (at.scale, {"lScalefactorX": 0.75, "lScaleFactorY": 1}),
        (at.scale, {"lScalefactorX": 1.5, "lScaleFactorY": 1}),
        (at.scale, {"lScalefactorX": 2, "lScaleFactorY": 1}),
        (at.scale, {"lScalefactorX": 4, "lScaleFactorY": 1}),
        #(0.25,1)(0.5,1)(0.75,1) (1.5,1)(2,1)(4,1)

        # scale nonuniform - Y
        (at.scale, {"lScalefactorX": 1, "lScaleFactorY": 0.25}),
        (at.scale, {"lScalefactorX": 1, "lScaleFactorY": 0.5}),
        (at.scale, {"lScalefactorX": 1, "lScaleFactorY": 0.75}),
        (at.scale, {"lScalefactorX": 1, "lScaleFactorY": 1.5}),
        (at.scale, {"lScalefactorX": 1, "lScaleFactorY": 2}),
        (at.scale, {"lScalefactorX": 1, "lScaleFactorY": 4}),
        # (1,0.25)(1,0.5)(1,0.75)(1,1.5)(1,2)(1,4)

        # scale nonuniform X-Y
        (at.scale, {"lScalefactorX": 0.25, "lScaleFactorY": 0.5}),
        (at.scale, {"lScalefactorX": 0.5, "lScaleFactorY": 0.25}),
        (at.scale, {"lScalefactorX": 0.25, "lScaleFactorY": 2}),
        (at.scale, {"lScalefactorX": 2, "lScaleFactorY": 0.25}),
        (at.scale, {"lScalefactorX": 2, "lScaleFactorY": 4}),
        (at.scale, {"lScalefactorX": 4, "lScaleFactorY": 2}),
        (at.scale, {"lScalefactorX": 0.9, "lScaleFactorY": 1.1}),
        (at.scale, {"lScalefactorX": 1.1, "lScaleFactorY": 0.9}),
        #(0.25,0.5)(0.5,0.25)(0.25,2)(2,0.25)(2,4)(4,2)(0.9,1.1)(1.1,0.9)

        # rotation - with rescale
        (at.rotation, {"dRotationAngle": 1, "bFit": True}),
        (at.rotation, {"dRotationAngle": 2, "bFit": True}),
        (at.rotation, {"dRotationAngle": 3, "bFit": True}),
        (at.rotation, {"dRotationAngle": 4, "bFit": True}),
        (at.rotation, {"dRotationAngle": 5, "bFit": True}),
        (at.rotation, {"dRotationAngle": 15, "bFit": True}),
        (at.rotation, {"dRotationAngle": 30, "bFit": True}),
        (at.rotation, {"dRotationAngle": 45, "bFit": True}),
        (at.rotation, {"dRotationAngle": 60, "bFit": True}),
        (at.rotation, {"dRotationAngle": 75, "bFit": True}),
        (at.rotation, {"dRotationAngle": 85, "bFit": True}),
        (at.rotation, {"dRotationAngle": 86, "bFit": True}),
        (at.rotation, {"dRotationAngle": 87, "bFit": True}),
        (at.rotation, {"dRotationAngle": 88, "bFit": True}),
        (at.rotation, {"dRotationAngle": 89, "bFit": True}),
        (at.rotation, {"dRotationAngle": 90, "bFit": True}),
        (at.rotation, {"dRotationAngle": 91, "bFit": True}),
        (at.rotation, {"dRotationAngle": 92, "bFit": True}),
        (at.rotation, {"dRotationAngle": 93, "bFit": True}),
        (at.rotation, {"dRotationAngle": 94, "bFit": True}),
        (at.rotation, {"dRotationAngle": 95, "bFit": True}),
        (at.rotation, {"dRotationAngle": 105, "bFit": True}),
        (at.rotation, {"dRotationAngle": 120, "bFit": True}),
        (at.rotation, {"dRotationAngle": 135, "bFit": True}),
        (at.rotation, {"dRotationAngle": 150, "bFit": True}),
        (at.rotation, {"dRotationAngle": 165, "bFit": True}),
        (at.rotation, {"dRotationAngle": 175, "bFit": True}),
        (at.rotation, {"dRotationAngle": 176, "bFit": True}),
        (at.rotation, {"dRotationAngle": 177, "bFit": True}),
        (at.rotation, {"dRotationAngle": 178, "bFit": True}),
        (at.rotation, {"dRotationAngle": 179, "bFit": True}),
        (at.rotation, {"dRotationAngle": 180, "bFit": True}),
        (at.rotation, {"dRotationAngle": 181, "bFit": True}),
        (at.rotation, {"dRotationAngle": 182, "bFit": True}),
        (at.rotation, {"dRotationAngle": 183, "bFit": True}),
        (at.rotation, {"dRotationAngle": 184, "bFit": True}),
        (at.rotation, {"dRotationAngle": 185, "bFit": True}),
        (at.rotation, {"dRotationAngle": 195, "bFit": True}),
        (at.rotation, {"dRotationAngle": 210, "bFit": True}),
        (at.rotation, {"dRotationAngle": 225, "bFit": True}),
        (at.rotation, {"dRotationAngle": 240, "bFit": True}),
        (at.rotation, {"dRotationAngle": 255, "bFit": True}),
        (at.rotation, {"dRotationAngle": 265, "bFit": True}),
        (at.rotation, {"dRotationAngle": 266, "bFit": True}),
        (at.rotation, {"dRotationAngle": 267, "bFit": True}),
        (at.rotation, {"dRotationAngle": 268, "bFit": True}),
        (at.rotation, {"dRotationAngle": 269, "bFit": True}),
        (at.rotation, {"dRotationAngle": 270, "bFit": True}),
        (at.rotation, {"dRotationAngle": 271, "bFit": True}),
        (at.rotation, {"dRotationAngle": 272, "bFit": True}),
        (at.rotation, {"dRotationAngle": 273, "bFit": True}),
        (at.rotation, {"dRotationAngle": 274, "bFit": True}),
        (at.rotation, {"dRotationAngle": 275, "bFit": True}),
        (at.rotation, {"dRotationAngle": 285, "bFit": True}),
        (at.rotation, {"dRotationAngle": 300, "bFit": True}),
        (at.rotation, {"dRotationAngle": 315, "bFit": True}),
        (at.rotation, {"dRotationAngle": 330, "bFit": True}),
        (at.rotation, {"dRotationAngle": 345, "bFit": True}),
        (at.rotation, {"dRotationAngle": 355, "bFit": True}),
        (at.rotation, {"dRotationAngle": 356, "bFit": True}),
        (at.rotation, {"dRotationAngle": 357, "bFit": True}),
        (at.rotation, {"dRotationAngle": 358, "bFit": True}),
        (at.rotation, {"dRotationAngle": 359, "bFit": True}),
        #1, 2, 3, 4, 5, 15, 30, 45, 60, 75, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 105, 120, 135, 150, 165,
        # 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 195, 210, 225, 240, 255, 265, 266, 267, 268, 269,
        # 270, 271, 272, 273, 274, 275, 285, 300, 315, 330, 345, 355, 356, 357, 358, 359


        # rotation - without rescale
        (at.rotation, {"dRotationAngle": 1, "bFit": False}),
        (at.rotation, {"dRotationAngle": 2, "bFit": False}),
        (at.rotation, {"dRotationAngle": 3, "bFit": False}),
        (at.rotation, {"dRotationAngle": 4, "bFit": False}),
        (at.rotation, {"dRotationAngle": 5, "bFit": False}),
        (at.rotation, {"dRotationAngle": 15, "bFit": False}),
        (at.rotation, {"dRotationAngle": 30, "bFit": False}),
        (at.rotation, {"dRotationAngle": 45, "bFit": False}),
        (at.rotation, {"dRotationAngle": 60, "bFit": False}),
        (at.rotation, {"dRotationAngle": 75, "bFit": False}),
        (at.rotation, {"dRotationAngle": 85, "bFit": False}),
        (at.rotation, {"dRotationAngle": 86, "bFit": False}),
        (at.rotation, {"dRotationAngle": 87, "bFit": False}),
        (at.rotation, {"dRotationAngle": 88, "bFit": False}),
        (at.rotation, {"dRotationAngle": 89, "bFit": False}),
        (at.rotation, {"dRotationAngle": 90, "bFit": False}),
        (at.rotation, {"dRotationAngle": 91, "bFit": False}),
        (at.rotation, {"dRotationAngle": 92, "bFit": False}),
        (at.rotation, {"dRotationAngle": 93, "bFit": False}),
        (at.rotation, {"dRotationAngle": 94, "bFit": False}),
        (at.rotation, {"dRotationAngle": 95, "bFit": False}),
        (at.rotation, {"dRotationAngle": 105, "bFit": False}),
        (at.rotation, {"dRotationAngle": 120, "bFit": False}),
        (at.rotation, {"dRotationAngle": 135, "bFit": False}),
        (at.rotation, {"dRotationAngle": 150, "bFit": False}),
        (at.rotation, {"dRotationAngle": 165, "bFit": False}),
        (at.rotation, {"dRotationAngle": 175, "bFit": False}),
        (at.rotation, {"dRotationAngle": 176, "bFit": False}),
        (at.rotation, {"dRotationAngle": 177, "bFit": False}),
        (at.rotation, {"dRotationAngle": 178, "bFit": False}),
        (at.rotation, {"dRotationAngle": 179, "bFit": False}),
        (at.rotation, {"dRotationAngle": 180, "bFit": False}),
        (at.rotation, {"dRotationAngle": 181, "bFit": False}),
        (at.rotation, {"dRotationAngle": 182, "bFit": False}),
        (at.rotation, {"dRotationAngle": 183, "bFit": False}),
        (at.rotation, {"dRotationAngle": 184, "bFit": False}),
        (at.rotation, {"dRotationAngle": 185, "bFit": False}),
        (at.rotation, {"dRotationAngle": 195, "bFit": False}),
        (at.rotation, {"dRotationAngle": 210, "bFit": False}),
        (at.rotation, {"dRotationAngle": 225, "bFit": False}),
        (at.rotation, {"dRotationAngle": 240, "bFit": False}),
        (at.rotation, {"dRotationAngle": 255, "bFit": False}),
        (at.rotation, {"dRotationAngle": 265, "bFit": False}),
        (at.rotation, {"dRotationAngle": 266, "bFit": False}),
        (at.rotation, {"dRotationAngle": 267, "bFit": False}),
        (at.rotation, {"dRotationAngle": 268, "bFit": False}),
        (at.rotation, {"dRotationAngle": 269, "bFit": False}),
        (at.rotation, {"dRotationAngle": 270, "bFit": False}),
        (at.rotation, {"dRotationAngle": 271, "bFit": False}),
        (at.rotation, {"dRotationAngle": 272, "bFit": False}),
        (at.rotation, {"dRotationAngle": 273, "bFit": False}),
        (at.rotation, {"dRotationAngle": 274, "bFit": False}),
        (at.rotation, {"dRotationAngle": 275, "bFit": False}),
        (at.rotation, {"dRotationAngle": 285, "bFit": False}),
        (at.rotation, {"dRotationAngle": 300, "bFit": False}),
        (at.rotation, {"dRotationAngle": 315, "bFit": False}),
        (at.rotation, {"dRotationAngle": 330, "bFit": False}),
        (at.rotation, {"dRotationAngle": 345, "bFit": False}),
        (at.rotation, {"dRotationAngle": 355, "bFit": False}),
        (at.rotation, {"dRotationAngle": 356, "bFit": False}),
        (at.rotation, {"dRotationAngle": 357, "bFit": False}),
        (at.rotation, {"dRotationAngle": 358, "bFit": False}),
        (at.rotation, {"dRotationAngle": 359, "bFit": False}),
        #1, 2, 3, 4, 5, 15, 30, 45, 60, 75, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 105, 120, 135, 150, 165,
        # 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 195, 210, 225, 240, 255, 265, 266, 267, 268, 269,
        # 270, 271, 272, 273, 274, 275, 285, 300, 315, 330, 345, 355, 356, 357, 358, 359

        # rotation - cropped
        (at.rotation_cropped, {"dRotationAngle": 1}),
        (at.rotation_cropped, {"dRotationAngle": 2}),
        (at.rotation_cropped, {"dRotationAngle": 3}),
        (at.rotation_cropped, {"dRotationAngle": 4}),
        (at.rotation_cropped, {"dRotationAngle": 5}),
        (at.rotation_cropped, {"dRotationAngle": 15}),
        (at.rotation_cropped, {"dRotationAngle": 30}),
        (at.rotation_cropped, {"dRotationAngle": 45}),
        (at.rotation_cropped, {"dRotationAngle": 60}),
        (at.rotation_cropped, {"dRotationAngle": 75}),
        (at.rotation_cropped, {"dRotationAngle": 85}),
        (at.rotation_cropped, {"dRotationAngle": 86}),
        (at.rotation_cropped, {"dRotationAngle": 87}),
        (at.rotation_cropped, {"dRotationAngle": 88}),
        (at.rotation_cropped, {"dRotationAngle": 89}),
        (at.rotation_cropped, {"dRotationAngle": 90}),
        (at.rotation_cropped, {"dRotationAngle": 91}),
        (at.rotation_cropped, {"dRotationAngle": 92}),
        (at.rotation_cropped, {"dRotationAngle": 93}),
        (at.rotation_cropped, {"dRotationAngle": 94}),
        (at.rotation_cropped, {"dRotationAngle": 95}),
        (at.rotation_cropped, {"dRotationAngle": 105}),
        (at.rotation_cropped, {"dRotationAngle": 120}),
        (at.rotation_cropped, {"dRotationAngle": 135}),
        (at.rotation_cropped, {"dRotationAngle": 150}),
        (at.rotation_cropped, {"dRotationAngle": 165}),
        (at.rotation_cropped, {"dRotationAngle": 175}),
        (at.rotation_cropped, {"dRotationAngle": 176}),
        (at.rotation_cropped, {"dRotationAngle": 177}),
        (at.rotation_cropped, {"dRotationAngle": 178}),
        (at.rotation_cropped, {"dRotationAngle": 179}),
        (at.rotation_cropped, {"dRotationAngle": 180}),
        (at.rotation_cropped, {"dRotationAngle": 181}),
        (at.rotation_cropped, {"dRotationAngle": 182}),
        (at.rotation_cropped, {"dRotationAngle": 183}),
        (at.rotation_cropped, {"dRotationAngle": 184}),
        (at.rotation_cropped, {"dRotationAngle": 185}),
        (at.rotation_cropped, {"dRotationAngle": 195}),
        (at.rotation_cropped, {"dRotationAngle": 210}),
        (at.rotation_cropped, {"dRotationAngle": 225}),
        (at.rotation_cropped, {"dRotationAngle": 240}),
        (at.rotation_cropped, {"dRotationAngle": 255}),
        (at.rotation_cropped, {"dRotationAngle": 265}),
        (at.rotation_cropped, {"dRotationAngle": 266}),
        (at.rotation_cropped, {"dRotationAngle": 267}),
        (at.rotation_cropped, {"dRotationAngle": 268}),
        (at.rotation_cropped, {"dRotationAngle": 269}),
        (at.rotation_cropped, {"dRotationAngle": 270}),
        (at.rotation_cropped, {"dRotationAngle": 271}),
        (at.rotation_cropped, {"dRotationAngle": 272}),
        (at.rotation_cropped, {"dRotationAngle": 273}),
        (at.rotation_cropped, {"dRotationAngle": 274}),
        (at.rotation_cropped, {"dRotationAngle": 275}),
        (at.rotation_cropped, {"dRotationAngle": 285}),
        (at.rotation_cropped, {"dRotationAngle": 300}),
        (at.rotation_cropped, {"dRotationAngle": 315}),
        (at.rotation_cropped, {"dRotationAngle": 330}),
        (at.rotation_cropped, {"dRotationAngle": 345}),
        (at.rotation_cropped, {"dRotationAngle": 355}),
        (at.rotation_cropped, {"dRotationAngle": 356}),
        (at.rotation_cropped, {"dRotationAngle": 357}),
        (at.rotation_cropped, {"dRotationAngle": 358}),
        (at.rotation_cropped, {"dRotationAngle": 359}),
        #1, 2, 3, 4, 5, 15, 30, 45, 60, 75, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 105, 120, 135, 150, 165,
        # 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 195, 210, 225, 240, 255, 265, 266, 267, 268, 269,
        # 270, 271, 272, 273, 274, 275, 285, 300, 315, 330, 345, 355, 356, 357, 358, 359

        # crop percentage - uniform
        (at.crop_percentage, {
            "tpSlice": (0.01, 0.01, 0.01, 0.01)}),
        (at.crop_percentage, {
            "tpSlice": (0.02, 0.02, 0.02, 0.02)}),
        (at.crop_percentage, {
            "tpSlice": (0.05, 0.05, 0.05, 0.05)}),
        (at.crop_percentage, {"tpSlice": (0.1, 0.1, 0.1, 0.1)}),
        (at.crop_percentage, {
            "tpSlice": (0.15, 0.15, 0.15, 0.15)}),
        (at.crop_percentage, {"tpSlice": (0.2, 0.2, 0.2, 0.2)}),
        (at.crop_percentage, {
            "tpSlice": (0.25, 0.25, 0.25, 0.25)}),
        (at.crop_percentage, {"tpSlice": (0.3, 0.3, 0.3, 0.3)}),
        # 0.01, 0.02 , 0.05, 0.10, 0.15, 0.20, 0.25, 0.30

        # crop percentage - nonuniform
        (at.crop_percentage, {"tpSlice": (0.50, 0, 0, 0)}),
        (at.crop_percentage, {"tpSlice": (0, 0.50, 0, 0)}),
        (at.crop_percentage, {"tpSlice": (0, 0, 0.50, 0)}),
        (at.crop_percentage, {"tpSlice": (0, 0, 0, 0.50)}),
        (at.crop_percentage, {"tpSlice": (0.50, 0.50, 0, 0)}),
        (at.crop_percentage, {"tpSlice": (0, 0.50, 0.50, 0)}),
        (at.crop_percentage, {"tpSlice": (0, 0, 0.50, 0.50)}),
        (at.crop_percentage, {"tpSlice": (0.50, 0, 0, 0.50)}),
        (at.crop_percentage, {
            "tpSlice": (0.25, 0.25, 0.1, 0.1)}),
        (at.crop_percentage, {
            "tpSlice": (0.1, 0.1, 0.25, 0.25)}),
        # (0.50, 0, 0, 0)(0, 0.50, 0, 0)(0, 0, 0.50, 0)(0, 0, 0, 0.50)(0.50,0.50,0,0)(0,0.50,0.50,0)
        # (0,0,0.50,0.50)(0.50,0,0,0.50) (0.25, 0.25,0.1,0.1) (0.1,0.1,0.25,0.25)

        # shift vertical
        (at.shift_vertical, {"lPixles": 1}),
        (at.shift_vertical, {"lPixles": 2}),
        (at.shift_vertical, {"lPixles": 5}),
        (at.shift_vertical, {"lPixles": 7}),
        (at.shift_vertical, {"lPixles": 10}),
        (at.shift_vertical, {"lPixles": 15}),
        (at.shift_vertical, {"lPixles": 20}),
        (at.shift_vertical, {"lPixles": -1}),
        (at.shift_vertical, {"lPixles": -2}),
        (at.shift_vertical, {"lPixles": -5}),
        (at.shift_vertical, {"lPixles": -7}),
        (at.shift_vertical, {"lPixles": -10}),
        (at.shift_vertical, {"lPixles": -15}),
        (at.shift_vertical, {"lPixles": -20}),
        # 1, 2, 5, 7, 10, 15, 20

        # shift horizontal
        (at.shift_horizontal, {"lPixles": 1}),
        (at.shift_horizontal, {"lPixles": 2}),
        (at.shift_horizontal, {"lPixles": 5}),
        (at.shift_horizontal, {"lPixles": 7}),
        (at.shift_horizontal, {"lPixles": 10}),
        (at.shift_horizontal, {"lPixles": 15}),
        (at.shift_horizontal, {"lPixles": 20}),
        (at.shift_horizontal, {"lPixles": -1}),
        (at.shift_horizontal, {"lPixles": -2}),
        (at.shift_horizontal, {"lPixles": -5}),
        (at.shift_horizontal, {"lPixles": -7}),
        (at.shift_horizontal, {"lPixles": -10}),
        (at.shift_horizontal, {"lPixles": -15}),
        (at.shift_horizontal, {"lPixles": -20}),
        # 1, 2, 5, 7, 10, 15, 2

        # flip
        (at.flip, {"bVertical": False}),
        (at.flip, {"bVertical": True}),

        # contrast
        (at.contrast, {"lContrast": 5}),
        (at.contrast, {"lContrast": 10}),
        (at.contrast, {"lContrast": 15}),
        (at.contrast, {"lContrast": 20}),
        (at.contrast, {"lContrast": 25}),
        (at.contrast, {"lContrast": 30}),
        (at.contrast, {"lContrast": 35}),
        (at.contrast, {"lContrast": 40}),
        (at.contrast, {"lContrast": 45}),
        (at.contrast, {"lContrast": 50}),
        (at.contrast, {"lContrast": 55}),
        (at.contrast, {"lContrast": 60}),
        (at.contrast, {"lContrast": 65}),
        (at.contrast, {"lContrast": 70}),
        (at.contrast, {"lContrast": -5}),
        (at.contrast, {"lContrast": -10}),
        (at.contrast, {"lContrast": -15}),
        (at.contrast, {"lContrast": -20}),
        (at.contrast, {"lContrast": -25}),
        (at.contrast, {"lContrast": -30}),
        (at.contrast, {"lContrast": -35}),
        (at.contrast, {"lContrast": -40}),
        (at.contrast, {"lContrast": -45}),
        (at.contrast, {"lContrast": -50}),
        (at.contrast, {"lContrast": -55}),
        (at.contrast, {"lContrast": -60}),
        (at.contrast, {"lContrast": -65}),
        (at.contrast, {"lContrast": -70}),
        # 	+-5, +-10, +-15, +-20, +- 25, +-30, +-35, +-40, +-45,
        # +-50, +-55, +-60, +-65, +-70


        # gamma adjustment
        (at.gamma_adjustment, {"dGamma": 0.25}),
        (at.gamma_adjustment, {"dGamma": 0.3}),
        (at.gamma_adjustment, {"dGamma": 0.4}),
        (at.gamma_adjustment, {"dGamma": 0.5}),
        (at.gamma_adjustment, {"dGamma": 0.75}),
        (at.gamma_adjustment, {"dGamma": 0.9}),
        (at.gamma_adjustment, {"dGamma": 1.1}),
        (at.gamma_adjustment, {"dGamma": 1.25}),
        (at.gamma_adjustment, {"dGamma": 1.5}),
        (at.gamma_adjustment, {"dGamma": 2}),
        (at.gamma_adjustment, {"dGamma": 2.5}),
        (at.gamma_adjustment, {"dGamma": 3}),
        (at.gamma_adjustment, {"dGamma": 3.5}),
        (at.gamma_adjustment, {"dGamma": 4}),
        (at.gamma_adjustment, {"dGamma": 5}),
        # 0.25, 0.3, 0.4, 0.5, 0.75, 0.9, 1.1, 1.25,
        # 1.5, 2, 2.5, 3, 3.5, 4, 5

        # median filter
        (at.median_filter, {"lKernelSize": 3}),
        (at.median_filter, {"lKernelSize": 5}),
        (at.median_filter, {"lKernelSize": 7}),
        (at.median_filter, {"lKernelSize": 9}),
        # 3,5,7,9

        # gauss filter
        (at.gaussian_filter, {"lSigma": 3}),
        (at.gaussian_filter, {"lSigma": 5}),
        (at.gaussian_filter, {"lSigma": 7}),
        (at.gaussian_filter, {"lSigma": 9}),
        # 3, 5, 7, 9

        # jpeg compression
        (at.jpeg_compression, {"lJPEGQuality": 0}),
        (at.jpeg_compression, {"lJPEGQuality": 10}),
        (at.jpeg_compression, {"lJPEGQuality": 20}),
        (at.jpeg_compression, {"lJPEGQuality": 30}),
        (at.jpeg_compression, {"lJPEGQuality": 40}),
        (at.jpeg_compression, {"lJPEGQuality": 50}),
        (at.jpeg_compression, {"lJPEGQuality": 60}),
        (at.jpeg_compression, {"lJPEGQuality": 70}),
        (at.jpeg_compression, {"lJPEGQuality": 80}),
        (at.jpeg_compression, {"lJPEGQuality": 90}),
        (at.jpeg_compression, {"lJPEGQuality": 100}),
        # 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100


        # gaussian noise
        (at.gauss_noise, {"dSigma": 0.01}),
        (at.gauss_noise, {"dSigma": 0.02}),
        (at.gauss_noise, {"dSigma": 0.03}),
        (at.gauss_noise, {"dSigma": 0.05}),
        (at.gauss_noise, {"dSigma": 0.07}),
        (at.gauss_noise, {"dSigma": 0.09}),
        (at.gauss_noise, {"dSigma": 0.1}),
        (at.gauss_noise, {"dSigma": 0.11}),
        (at.gauss_noise, {"dSigma": 0.15}),
        (at.gauss_noise, {"dSigma": 0.2}),
        # 0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.11, 0.15, 0.2

        # speckle noise
        (at.speckle_noise, {"dSigma": 0.01}),
        (at.speckle_noise, {"dSigma": 0.02}),
        (at.speckle_noise, {"dSigma": 0.03}),
        (at.speckle_noise, {"dSigma": 0.05}),
        (at.speckle_noise, {"dSigma": 0.07}),
        (at.speckle_noise, {"dSigma": 0.09}),
        (at.speckle_noise, {"dSigma": 0.1}),
        (at.speckle_noise, {"dSigma": 0.11}),
        (at.speckle_noise, {"dSigma": 0.15}),
        (at.speckle_noise, {"dSigma": 0.2}),
        # 0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.11, 0.15, 0.2

        # salt and pepper noise
        (at.salt_and_pepper_noise, {"dAmount": 0.01}),
        (at.salt_and_pepper_noise, {"dAmount": 0.02}),
        (at.salt_and_pepper_noise, {"dAmount": 0.03}),
        (at.salt_and_pepper_noise, {"dAmount": 0.05}),
        (at.salt_and_pepper_noise, {"dAmount": 0.07}),
        (at.salt_and_pepper_noise, {"dAmount": 0.09}),
        (at.salt_and_pepper_noise, {"dAmount": 0.1}),
        (at.salt_and_pepper_noise, {"dAmount": 0.11}),
        (at.salt_and_pepper_noise, {"dAmount": 0.15}),
        (at.salt_and_pepper_noise, {"dAmount": 0.2}),
        # 0.01, 0.03, 0.05, 0.07, 0.09, 0.1, 0.11, 0.15, 0.2


        # brightness
        (at.brightness, {"lBrightness": 10}),
        (at.brightness, {"lBrightness": 20}),
        (at.brightness, {"lBrightness": 30}),
        (at.brightness, {"lBrightness": 40}),
        (at.brightness, {"lBrightness": 50}),
        (at.brightness, {"lBrightness": 60}),
        (at.brightness, {"lBrightness": 70}),
        (at.brightness, {"lBrightness": 80}),
        (at.brightness, {"lBrightness": 90}),
        (at.brightness, {"lBrightness": 100}),
        (at.brightness, {"lBrightness": 110}),
        (at.brightness, {"lBrightness": 120}),
        (at.brightness, {"lBrightness": -10}),
        (at.brightness, {"lBrightness": -20}),
        (at.brightness, {"lBrightness": -30}),
        (at.brightness, {"lBrightness": -40}),
        (at.brightness, {"lBrightness": -50}),
        (at.brightness, {"lBrightness": -60}),
        (at.brightness, {"lBrightness": -70}),
        (at.brightness, {"lBrightness": -80}),
        (at.brightness, {"lBrightness": -90}),
        (at.brightness, {"lBrightness": -100}),
        (at.brightness, {"lBrightness": -110}),
        (at.brightness, {"lBrightness": -120}),
        # +-10, +-20, +-30, +-40, +-50, +-60, +-70, +-80,
        # +-90,+-100, +-110, +-120

    ]

    # define a set of hashing algorithms
    # NOTE: add your own hashing algorithms here
    import wuhash as wu
    import blockhash as block
    import predef_hashes as pdh

    aHashes = [
        (pdh.average_hash, {}),
        # (pdh.phash, {}),
        (pdh.dhash, {}),
        # (pdh.whash, {}),
        (block.blockhash, {}),
        # (wu.wuhash, {}),
        # add rotation handling to wuhash
        # (wu.wuhash, {"bRotationHandling": True}),
        # add fliphandling to all hashing methods
        (pdh.average_hash, {"bFlipHandling": True}),
        # (pdh.phash, {"bFlipHandling": True}),
        (pdh.dhash, {"bFlipHandling": True}),
        # (pdh.whash, {"bFlipHandling": True}),
        (block.blockhash, {"bFlipHandling": True}),
        # (wu.wuhash, {"bFlipHandling": True}),
        # (wu.wuhash, {"bFlipHandling": True,
        #              "bRotationHandling": True}),
    ]

    # define the deviation function if whished
    import deviation as dv
    fnDeviationFunction = dv.hamming_distance

    # set number of threads
    lNumberOfThreads = 4

    # set path of image folder
    sPathToImages = "../data/img/"

    # ---- add definitions to benchmark
    stabbench.set_attacks(aAttacks)
    stabbench.set_hashes(aHashes)
    stabbench.set_deviation_fn(fnDeviationFunction)
    stabbench.set_nr_of_threads(lNumberOfThreads)

    # -------- run test -------
    stabbench.run_test_on_images(sPathToImages)
