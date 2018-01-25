#!/usr/bin/env python3

import sys
sys.path.append('../common')

import sensitivity_benchmark as seb


if __name__ == '__main__':
    # create new benchmark instance
    sensbench = seb.SensitivityBenchmark()

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

    # set number of threads
    lNumberOfThreads = 4

    # set pathes to imagesets that should be hashed
    aImagesets = [
        "../data/img/"
    ]

    # ---- add definitions to benchmark
    sensbench.set_hashes(aHashes)
    sensbench.set_nr_of_threads(lNumberOfThreads)

    # -------- run test -------
    for sPathToImageSet in aImagesets:
        sensbench.hash_imageset(sPathToImageSet)
