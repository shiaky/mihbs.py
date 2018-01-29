#!/usr/bin/env python3
import sys
sys.path.append('../common')

import util
import deviation
import dbcon
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


# ---- helper functions ------


def convert_db_to_pandas(sPathToDB="../data/sensitivity_results/sensitivity_results.db"):
    # check if db is existend
    if not util.check_if_file_exists(sPathToDB):
        raise Exception("database %s is not existend" % sPathToDB)
    dbData = dbcon.Dbcon(sPathToDB)

    # get all tests and parse it to panda dataframe
    oSensitivityTestData = pd.read_sql_query(
        "SELECT i.name as 'image', c.name as 'collection', h.hash, (ht.name || ' ' || ht.params) as 'hashalgorithm'  FROM images as i INNER JOIN collections as c on c.id = i.collection_id INNER JOIN images_hashes as ih on ih.image_id = i.id INNER JOIN hashes as h on h.id = ih.hash_id INNER JOIN hash_types as ht on ht.id = h.hash_type_id;", dbData.con)

    return oSensitivityTestData


def calculate_stats(oSensitivityTestData, lTestDatasetSize, lRandomDataSplitSeed=None, aFARThresholdSteps=np.arange(0, 1.01, 0.01)):

    dicResult = {}

    # do it for every single hash algorithm
    for sHashAlgo in oSensitivityTestData.hashalgorithm.unique():
        # filter dataset by hashalgo
        oFilteredSensitivityTestData = oSensitivityTestData[
            oSensitivityTestData.hashalgorithm == sHashAlgo]

        #  split the data in a testset and a big reference set
        oBigDataset, oTestDataset = train_test_split(
            oFilteredSensitivityTestData, test_size=lTestDatasetSize, random_state=lRandomDataSplitSeed)

        # create deviation array having size of
        # nr. of test_images * # nr. of reference_images
        lNumberOfTestReferenceRelationsTotal = oTestDataset.shape[0] * \
            oBigDataset.shape[0]
        aHashDeviations = np.zeros(lNumberOfTestReferenceRelationsTotal)
        # iterate over every image in the test dataset
        i = 0
        for aTestImageHash in oTestDataset["hash"].values:
            # iterate over all images in the big reference dataset
            for aReferenceImageHash in oBigDataset["hash"].values:
                aHashDeviations[i] = deviation.hamming_distance(
                    aTestImageHash, aReferenceImageHash)
                i += 1

        # calculate metrics
        dicMetrics = {
            "min": np.min(aHashDeviations),
            "p25": np.percentile(aHashDeviations, 25),
            "p75": np.percentile(aHashDeviations, 75),
            "max": np.max(aHashDeviations),
            "mean": np.mean(aHashDeviations)
        }

        # calculate FAR error rate for every threshold step
        aErrorRate = []
        for dThreshold in aThresholdSteps:
            lCountOfValuesSmallerThreshold = np.sum(
                np.array(aHashDeviations) < dThreshold)
            aErrorRate.append(lCountOfValuesSmallerThreshold /
                              lNumberOfTestReferenceRelationsTotal)
        oErrorRate = pd.DataFrame(
            {"threshold": aThresholdSteps, "errorrate": aErrorRate})

        dicResult[sHashAlgo] = {"metrics": dicMetrics, "errorrate": oErrorRate}
    return dicResult


#-------------------------------


if __name__ == "__main__":

    # ---------- config ----------------------

    # set name of collection to test
    sCollectionName = "img"
    # TODO: save results of collection to folder having the same name

    # set size of test dataset to split from full dataset
    # NOTE: you can define
    # an arbitrary number here but keep in mind that
    # every image from the testset will be compared to every
    # image from the big set. The more test images you want to have
    # the more time the test will consume
    lTestDatasetSize = 10

    # data will be splitted by a randomized method. Define a fixed
    # seed if you need reproducible results. Define it as None to
    # start the PRNG with a random seed
    lRandomDataSplitSeed = None

    # define the steps for the calculation of the error rate
    # and the plot (min, max + step, step)
    aThresholdSteps = np.arange(0, 1.01, 0.01)

    # ----------------------------------------

    # get all data in pandas dataframe
    oSensitivityTestData = convert_db_to_pandas()

    # set name of test dataset
    oSensitivityTestData = oSensitivityTestData[oSensitivityTestData.collection == sCollectionName]

    # split dataset in test and big dataset

    # perform error handling regarding size of the dataset and test ratio
    lDatasetSize = len(oSensitivityTestData.image.unique())
    dTestSizePercentage = lTestDatasetSize / lDatasetSize

    # TODO: actovate checks again
    # if lDatasetSize < 100:
    #     raise Exception(
    #         "Your chosen dataset contains %i images. This seems to be to small for this kind of test. Try a set with 100 images and more." % lDatasetSize)
    # if dTestSizePercentage > 0.3:
    #     raise Exception(
    #         "You tried to use %f of the images as testset. You can not use a ratio bigger than 0.3 as testset." % dTestSizePercentage)
    # if lTestDatasetSize < 5:
    #     raise Exception(
    #         "You tried to use a testset of %i images. Use at least 5 images as testset to gain reliable results.")

    # calculate the min, mean und max deviation
    # from every image from the test dataset to
    # every image in the simila image dataset
    # for every hashing algo
    # calc number of hits for thresholds (0, 0.5)
    # (threaded)
    dicSensitivityResults = calculate_stats(oSensitivityTestData,
                                            lTestDatasetSize, lRandomDataSplitSeed, aThresholdSteps)

    # plot min mean max for every hashing algo
    # TODO: plot

    # export min, mean, max for every hashing algo
    # TODO: export
