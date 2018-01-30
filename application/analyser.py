#!/usr/bin/env python3
import sys
sys.path.append('../common')

import util
import deviation
import dbcon
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# -------- helper functions -------


def convert_db_to_pandas(sPathToDB="../data/application_results/application_results.db"):
    # check if db is existend
    if not util.check_if_file_exists(sPathToDB):
        raise Exception("database %s is not existend" % sPathToDB)
    dbData = dbcon.Dbcon(sPathToDB)

    # get all tests and parse it to panda dataframe
    oApplicationTestData = pd.read_sql_query(
        "SELECT i.name as 'image', c.name as 'collection', h.hash, (ht.name || ' ' || ht.params) as 'hashalgorithm'  FROM images as i INNER JOIN collections as c on c.id = i.collection_id INNER JOIN images_hashes as ih on ih.image_id = i.id INNER JOIN hashes as h on h.id = ih.hash_id INNER JOIN hash_types as ht on ht.id = h.hash_type_id;", dbData.con)

    return oApplicationTestData


def get_deviations_to_original(oPandasData, sReferenceCollectionName):
    oPandasFullHashTypeDataset = None
    for sHashType in oPandasData.hashalgorithm.unique():
        for sImageBaseName in oPandasData[oPandasData.collection == sReferenceCollectionName].image.unique():
            sImageBaseName = sImageBaseName.split(".")[-2]
            oPandasHashData = oPandasData[(oPandasData.hashalgorithm == sHashType) & (
                oPandasData.image.str.contains(sImageBaseName))]
            oRefHash = oPandasHashData[oPandasHashData.collection ==
                                       sReferenceCollectionName].hash.values[0]
            oPandasHashData = oPandasHashData[oPandasHashData.collection !=
                                              sReferenceCollectionName]
            oPandasHashData["deviation"] = oPandasHashData.apply(
                lambda row: deviation.hamming_distance(row["hash"], oRefHash), axis=1)
            if isinstance(oPandasFullHashTypeDataset, pd.DataFrame):
                oPandasFullHashTypeDataset = pd.concat(
                    [oPandasFullHashTypeDataset, oPandasHashData])
            else:
                oPandasFullHashTypeDataset = oPandasHashData

    return oPandasFullHashTypeDataset


def get_deviations_to_notoriginal(oPandasData, sReferenceCollectionName):
    """ used for FAR test """
    oPandasFullHashTypeDataset = None
    for sHashType in oPandasData.hashalgorithm.unique():
        for i, sImageBaseName in enumerate(oPandasData[oPandasData.collection == sReferenceCollectionName].image.unique()):
            sImageBaseName = sImageBaseName.split(".")[-2]
            oPandasHashData = oPandasData[(oPandasData.hashalgorithm == sHashType) & (
                oPandasData.image.str.contains(sImageBaseName))]
            # choose a deterministic ref image that is not the original
            np.random.seed(i)
            oRefHash = np.random.choice(oPandasData[(oPandasData.collection == sReferenceCollectionName) & (oPandasData.hashalgorithm == sHashType) & (
                ~oPandasData.image.str.contains(sImageBaseName))].hash.values)
            oPandasHashData = oPandasHashData[oPandasHashData.collection !=
                                              sReferenceCollectionName]
            oPandasHashData["deviation"] = oPandasHashData.apply(
                lambda row: deviation.hamming_distance(row["hash"], oRefHash), axis=1)
            if isinstance(oPandasFullHashTypeDataset, pd.DataFrame):
                oPandasFullHashTypeDataset = pd.concat(
                    [oPandasFullHashTypeDataset, oPandasHashData])
            else:
                oPandasFullHashTypeDataset = oPandasHashData

    return oPandasFullHashTypeDataset

#---------- user defined functions ----------------


def add_image_name_information_to_dataframe(oPandasDataframe):

    aSplitNameArray = []
    for index, row in oPandasDataframe.iterrows():
        aSplitNameArray.append(row["image"].split("_"))

    pdDataFrameImageNamesSplit = pd.DataFrame({"split": aSplitNameArray})

    oPandasDataframe["printer"] = pdDataFrameImageNamesSplit.apply(
        lambda row: row["split"][0] if len(row["split"]) > 1 else np.NaN, axis=1)

    oPandasDataframe["printer_resolution"] = pdDataFrameImageNamesSplit.apply(
        lambda row: row["split"][2] if len(row["split"]) > 1 else np.NaN, axis=1)

    oPandasDataframe["scanner_resolution"] = pdDataFrameImageNamesSplit.apply(
        lambda row: row["split"][3] if len(row["split"]) > 1 else np.NaN, axis=1)

    oPandasDataframe["scanner"] = pdDataFrameImageNamesSplit.apply(
        lambda row: row["split"][5] if len(row["split"]) > 1 else np.NaN, axis=1)

    oPandasDataframe["paper"] = pdDataFrameImageNamesSplit.apply(
        lambda row: row["split"][6] if len(row["split"]) > 1 else np.NaN, axis=1)

    oPandasDataframe["special"] = pdDataFrameImageNamesSplit.apply(
        lambda row: row["split"][7] if len(row["split"]) > 8 else np.NaN, axis=1)

    return oPandasDataframe


# ----------------------------------------------------


if __name__ == "__main__":
    # ---------- config ----------------------

    # set name reference collection
    sReferenceCollectionName = "ref"

    # define the steps for the calculation of the error rate
    # and the plot (min, max + step, step)
    aThresholdSteps = np.arange(0, 1.01, 0.01)

    # define path for plots and starts
    sApplicationTestResultBasePath = "../data/application_results/"

    # set size of the plot
    # set figure size
    plt.figure(num=None, figsize=(7, 6), dpi=100,
               facecolor='w', edgecolor='k')

    # ----------------------------------------

    # get all data in pandas dataframe
    oApplicationTestData = convert_db_to_pandas()

    ###### USER SPECIFIC#####################
    # define custom feature generators here
    oApplicationTestData = add_image_name_information_to_dataframe(
        oApplicationTestData)

    #########################################

    # calculate deviations to original
    oPandasDeviationsToOriginal = get_deviations_to_original(
        oApplicationTestData, sReferenceCollectionName)

   # calculate deviations to not original
    oPandasDeviationsToNonoriginal = get_deviations_to_notoriginal(
        oApplicationTestData, sReferenceCollectionName)

    print(oPandasDeviationsToNonoriginal)
