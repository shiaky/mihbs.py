#!/usr/bin/env python3

import sys
sys.path.append('../common')

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
