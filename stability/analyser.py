#!/usr/bin/env python3
import sys
sys.path.append('../common')

import util
import dbcon
import ast
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


# --------- helper functions -------

def convert_db_to_pandas(sPathToDB="./data/stability_results/stability_results.db"):
    # check if db is existend
    if not util.check_if_file_exists(sPathToDB):
        raise Exception("database %s is not existend" % sPathToDB)
    dbData = dbcon.Dbcon(sPathToDB)

    # get all tests and parse it to panda dataframe
    oStabilityTestData = pd.read_sql_query(
        "SELECT t.id, t.image, t.deviation_hash, ht.hash_fn, ht.hash_params , a.attack_fn, a.attack_params, i.name as 'image_name' FROM tests as t INNER JOIN attacks as a on a.id = t.attack INNER JOIN hash_types as ht on ht.id = t.hash_type INNER JOIN images as i ON i.id = t.image;", dbData.con)

    oStabilityTestData["hashalgorithm"] = oStabilityTestData.apply(
        lambda row: row["hash_fn"] + " " + row["hash_params"], axis=1)

    return oStabilityTestData


def get_list_of_attacks(oPandasData):
    """ returns a list of attacks when a pandas dataframe if given """
    return oStabilityTestData.attack_fn.unique()


# ----------- diagram functions ----------------------------#

def plot_single_parameter_sortable(sImageName,
                                   oPandasData,
                                   sXColumnName,
                                   sYColumnName,
                                   sCategoryColumnName,
                                   sBasePath,
                                   sUnitColumnName="image",
                                   sDiagramTitle=None,
                                   sXLabel=None,
                                   sYLabel=None,
                                   aXTicks=None,
                                   lConfidenceInterval=95,
                                   bInterpolate=True,
                                   aYLim=None):
    """plot the mean values and the confidence interval over the unit column for each category (mostly hashes)"""
    plt.clf()
    oSeabornPlot = sb.tsplot(time=sXColumnName, value=sYColumnName, unit=sUnitColumnName, condition=sCategoryColumnName, ci=lConfidenceInterval, interpolate=bInterpolate,
                             data=oPandasData)
    if sDiagramTitle:
        oSeabornPlot.set(title=sDiagramTitle)
    if sXLabel:
        oSeabornPlot.set(xlabel=sXLabel)
    if sYLabel:
        oSeabornPlot.set(ylabel=sYLabel)
    if not (aXTicks is None):
        oSeabornPlot.set(xticks=aXTicks)
    if not (aYLim is None):
        oSeabornPlot.set(ylim=aYLim)
    sTargetPath = sStabilityResultsPath + sBasePath + sPlotSubpath
    util.create_path(sTargetPath)
    oSeabornPlot.get_figure().savefig(sTargetPath + sImageName)
    plt.clf()


def plot_single_parameter_sortable_for_each_hash(sImageBaseName,
                                                 sImageExtension,
                                                 oPandasData,
                                                 sXColumnName,
                                                 sYColumnName,
                                                 sCategoryColumnName,
                                                 sBasePath,
                                                 sUnitColumnName="image",
                                                 sDiagramTitle=None,
                                                 sXLabel=None,
                                                 sYLabel=None,
                                                 aXTicks=None,
                                                 lConfidenceInterval=95,
                                                 bInterpolate=True):
    """for each hashfunction: plot the mean values and the confidence interval over the unit column for each category (mostly hashes)"""
    dYMax = np.percentile(oPandasData[sYColumnName].values, 99)
    aYLim = (0, dYMax)
    for sHashFunction in oPandasData["hash_fn"].unique():
        plot_single_parameter_sortable(sImageBaseName + "__" + sHashFunction + sImageExtension,
                                       oPandasData[oPandasData["hash_fn"]
                                                   == sHashFunction],
                                       sXColumnName,
                                       sYColumnName,
                                       sCategoryColumnName,
                                       sBasePath,
                                       sUnitColumnName,
                                       sDiagramTitle,
                                       sXLabel,
                                       sYLabel,
                                       aXTicks,
                                       lConfidenceInterval,
                                       bInterpolate,
                                       aYLim=aYLim)


def plot_single_parameter_categorical(sImageName,
                                      oPandasData,
                                      sXColumnName,
                                      sYColumnName,
                                      sCategoryColumnName,
                                      sBasePath,
                                      sDiagramTitle=None,
                                      sXLabel=None,
                                      sYLabel=None,
                                      aXTicks=None,
                                      lConfidenceInterval=95,
                                      aYLim=None):
    """plot the mean values and the confidence interval over whole dataFrame for each category (mostly hashes)"""
    plt.clf()
    # i have to filter the columns here because this plot can not deal with
    # multiple ids etc.
    oPandasData = oPandasData[[sXColumnName,
                               sYColumnName, sCategoryColumnName]]
    oSeabornPlot = sb.barplot(x=sXColumnName, y=sYColumnName,
                              hue=sCategoryColumnName, ci=lConfidenceInterval, capsize=.2,  data=oPandasData)
    if sDiagramTitle:
        oSeabornPlot.set(title=sDiagramTitle)
    if sXLabel:
        oSeabornPlot.set(xlabel=sXLabel)
    if sYLabel:
        oSeabornPlot.set(ylabel=sYLabel)
    if not (aXTicks is None):
        oSeabornPlot.set(xticks=aXTicks)
    if not (aYLim is None):
        oSeabornPlot.set(ylim=aYLim)
    sTargetPath = sStabilityResultsPath + sBasePath + sPlotSubpath
    util.create_path(sTargetPath)
    oSeabornPlot.get_figure().savefig(sTargetPath + sImageName)
    plt.clf()


def plot_single_parameter_categorical_for_each_hash(sImageBaseName,
                                                    sImageExtension,
                                                    oPandasData,
                                                    sXColumnName,
                                                    sYColumnName,
                                                    sCategoryColumnName,
                                                    sBasePath,
                                                    sDiagramTitle=None,
                                                    sXLabel=None,
                                                    sYLabel=None,
                                                    aXTicks=None,
                                                    lConfidenceInterval=95):
    """for each hashfunction: plot the mean values and the confidence interval over the pandas dataframe for each category (mostly hashes)"""
    dYMax = np.percentile(oPandasData[sYColumnName].values, 99)
    aYLim = (0, dYMax)
    for sHashFunction in oPandasData["hash_fn"].unique():
        plot_single_parameter_categorical(sImageBaseName + "__" + sHashFunction + sImageExtension,
                                          oPandasData[oPandasData["hash_fn"]
                                                      == sHashFunction],
                                          sXColumnName,
                                          sYColumnName,
                                          sCategoryColumnName,
                                          sBasePath,
                                          sDiagramTitle,
                                          sXLabel,
                                          sYLabel,
                                          aXTicks,
                                          lConfidenceInterval,
                                          aYLim=aYLim)

# --------------------- data stats generators ---------------------- #


def calc_values_single_parameter_for_each_hash(sFileBaseName, oPandasData, sXColumnName, sYColumnName, sCategoryColumnName, sBasePath, sFileExtension=".txt"):
    """ save the min, mean and max values to file grouped by every hash algorithm and parameter value"""
    sTargetPath = sStabilityResultsPath + sBasePath + sStatsSubpath
    util.create_path(sTargetPath)
    with open(sTargetPath + sFileBaseName + sFileExtension, 'w') as file:
        oPandasData.groupby([sCategoryColumnName, sXColumnName])[sYColumnName].agg(
            {"min": np.min, "mean": np.mean, "max": np.max}).to_string(file)


def calc_values_multiple_parameter_for_each_hash(sFileBaseName, oPandasData, sYColumnName, sCategoryColumnName, sBasePath, sFileExtension=".txt"):
    """ save the min, mean and max values to file grouped by every hash algorithm and parameters of attack 1 and 2"""
    sTargetPath = sStabilityResultsPath + sBasePath + sStatsSubpath
    util.create_path(sTargetPath)
    oGroupDF = oPandasData.groupby([sCategoryColumnName, "attack1", "params1", "attack2", "params2"])[sYColumnName].agg(
        {"min": np.min, "mean": np.mean, "max": np.max})
    with open(sTargetPath + sFileBaseName + sFileExtension, 'w') as file:
        oGroupDF.to_string(file)
    with open(sTargetPath + sFileBaseName + ".tex", 'w') as file:
        oGroupDF.to_latex(file)
    with open(sTargetPath + sFileBaseName + ".csv", 'w') as file:
        oGroupDF.to_csv(file)


# ------------------------- attack handlers --------------------------
def scale_handler(oPandasData, sBasePath="unsegmented/", sYColumnName="deviation_hash", sYLabel="mittlere Hammingdistanz (ci = 95%)"):
    # filter all scale
    oScale = oPandasData[oPandasData["attack_fn"] == "scale"]

    # calculate x and y parameters
    oScale["paramY"] = oScale["attack_params"].map(
        lambda a: ast.literal_eval(a)["lScaleFactorY"])
    # TODO: change the typo in the attacks and here and in stability test
    oScale["paramX"] = oScale["attack_params"].map(
        lambda a: ast.literal_eval(a)["lScalefactorX"])

    # first progress with uniform scale
    oScaleUniform = oScale[oScale["paramX"] == oScale["paramY"]]

    aScaleTypes = [
        ("scale_uniform", "Skalierung (uniform)", "paramX", "Saklierungsfaktor x und y",
         oScale[oScale["paramX"] == oScale["paramY"]]),
        ("scale_nonuniform_x", "Skalierung (nichtuniform, X-Achse)", "paramX", "Saklierungsfaktor x",
         oScale[oScale["paramY"] == 1]),
        ("scale_nonuniform_y", "Skalierung (nichtuniform, Y-Achse)", "paramY", "Saklierungsfaktor y",
         oScale[oScale["paramX"] == 1])
    ]
    for sFileBaseName, sDiagramTitle, sXColumnName, sXLabel, oData in aScaleTypes:
        # plot uniform scale data
        plot_single_parameter_sortable_for_each_hash(sImageBaseName=sFileBaseName,
                                                     sImageExtension=".png",
                                                     oPandasData=oData,
                                                     sXColumnName=sXColumnName,
                                                     sYColumnName=sYColumnName,
                                                     sCategoryColumnName="hashalgorithm",
                                                     sBasePath=sBasePath,
                                                     sUnitColumnName="image",
                                                     sDiagramTitle=sDiagramTitle,
                                                     sXLabel=sXLabel,
                                                     sYLabel=sYLabel,
                                                     lConfidenceInterval=95,
                                                     bInterpolate=True)
        calc_values_single_parameter_for_each_hash(
            sFileBaseName, oPandasData=oData, sXColumnName=sXColumnName, sYColumnName=sYColumnName, sCategoryColumnName="hashalgorithm", sBasePath=sBasePath)

    # continue here with non uniform values
    oNonuniformScale = oScale[(oScale["paramX"] != oScale["paramY"]) & (
        oScale["paramX"] != 1) & (oScale["paramY"] != 1)]

    # create parameter
    oNonuniformScale["parameter"] = oNonuniformScale["attack_params"].map(
        lambda a: "(" + str(ast.literal_eval(a)["lScalefactorX"]) + ", " + str(ast.literal_eval(a)["lScaleFactorY"]) + ")")

    plot_single_parameter_categorical_for_each_hash(sImageBaseName="scale_nonuniform",
                                                    sImageExtension=".png",
                                                    oPandasData=oNonuniformScale,
                                                    sXColumnName="parameter",
                                                    sYColumnName=sYColumnName,
                                                    sCategoryColumnName="hashalgorithm",
                                                    sBasePath=sBasePath,
                                                    sDiagramTitle="Skalierung (nichtuniform)",
                                                    sXLabel="Skalierungsfaktor (x, y)",
                                                    sYLabel=sYLabel,
                                                    lConfidenceInterval=95)
    calc_values_single_parameter_for_each_hash(
        "scale_nonuniform", oPandasData=oNonuniformScale, sXColumnName="parameter", sYColumnName=sYColumnName, sCategoryColumnName="hashalgorithm", sBasePath=sBasePath)


#----------------------- main function ----------------------------


if __name__ == "__main__":

    # -------- global config ----------------
    # NOTE: add your custom pathes here
    sStabilityResultsPath = "../stability_results/"
    sPlotSubpath = "plots/"
    sStatsSubpath = "stats/"

    sPathToDB = "../data/stability_results/stability_results.db"

    # NOTE: if you define a new attack, you have to implement aAttacks
    # handler that extracts the data and plots the charts needed
    dicAttackHandler = {
        "scale": (scale_handler, {})
    }

    # ------------------------------------------------------
    # create pathes
    util.create_path(sStabilityResultsPath + sPlotSubpath)
    util.create_path(sStabilityResultsPath + sStatsSubpath)

    # read database
    oStabilityTestData = convert_db_to_pandas(sPathToDB)

    # get list of attacks applied
    aAttacks = get_list_of_attacks(oStabilityTestData)

    # run handler for every attack defined
    for sAttack in aAttacks:
        if not(sAttack in dicAttackHandler.keys()):
            print("There is no handler for attack %s" % sAttack)
            continue
        fnAttackHandler, dicHandlerParams = dicAttackHandler[sAttack]
        # run attackhandler with params
        fnAttackHandler(oStabilityTestData, **dicHandlerParams)
