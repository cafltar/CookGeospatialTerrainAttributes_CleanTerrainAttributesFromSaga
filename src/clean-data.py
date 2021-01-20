import pandas as pd
import pathlib
import geopandas as gpd
import time

def getCookEastData(filePath):
    colKeep = [
        1,11,12,18,19,20,21,22,23,24,25,26,27,29,30,31,32,35
    ]
    colName = [
        "ID2", 
        "Elevation",
        "Slope",
        "Aspect",
        "TRASP",
        "ProfileCurvature",
        "PlanCurvature",
        "TangentialCurvature",
        "AnalyticalHillshade",
        "ConvergenceIndex",
        "TotalCatchmentArea",
        "TopographicWetnessIndex",
        "LengthSlopeFactor",
        "ChannelNetworkBaseLevel",
        "ChannelNetworkDistance",
        "ValleyDepth",
        "RelativeSlopePosition",
        "AnnualGlobalSolarRadiation"]
    result = pd.read_excel(
        filePath, 
        "Sheet1",
        usecols=colKeep,
        names=colName)

    return result

def getCookWestData(filePath):
    colKeep = [
        4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21
    ]
    colName = [
        "ID2",
        "Elevation",
        "AnalyticalHillshade",
        "ConvergenceIndex",
        "TotalCatchmentArea",
        "TopographicWetnessIndex",
        "LengthSlopeFactor",
        "ChannelNetworkBaseLevel",
        "ChannelNetworkDistance",
        "ValleyDepth",
        "RelativeSlopePosition",
        "Slope",
        "Aspect",
        "TRASP",
        "ProfileCurvature",
        "PlanCurvature",
        "TangentialCurvature",
        "AnnualGlobalSolarRadiation"
    ]
    result = pd.read_csv(
        filePath,
        usecols=colKeep,
        names=colName,
        skiprows=1)

    return result

def main(args):
    
    # Load datasets
    ce = getCookEastData(args["PathCookEast"])
    cw = getCookWestData(args["PathCookWest"])

    # Add FieldNames and merge datasets
    ce["FieldName"] = "CookEast"
    cw["FieldName"] = "CookWest"
    cook = pd.concat([ce, cw], sort=True)

    # Load georeference points with lat/lon information
    cegp = gpd.read_file(args["PathCEGP"])
    cwgp = gpd.read_file(args["PathCWGP"])
    gp = pd.concat([cwgp, cegp])
    gp = gp.assign(Latitude = gp.geometry.y,Longitude = gp.geometry.x)
    
    # Merge lat/lon
    cookSpatial = cook.merge(gp, on = "ID2").drop(columns = ["geometry"])
    
    # Make pretty
    colsSort = colName = [
        "ID2",
        "FieldName",
        "Latitude",
        "Longitude",
        "Elevation",
        "AnalyticalHillshade",
        "ConvergenceIndex",
        "TotalCatchmentArea",
        "TopographicWetnessIndex",
        "LengthSlopeFactor",
        "ChannelNetworkBaseLevel",
        "ChannelNetworkDistance",
        "ValleyDepth",
        "RelativeSlopePosition",
        "Slope",
        "Aspect",
        "TRASP",
        "ProfileCurvature",
        "PlanCurvature",
        "TangentialCurvature",
        "AnnualGlobalSolarRadiation"
    ]

    result = cookSpatial[colsSort].sort_values(by = ["ID2"])

     # Write the file
    dateNow = time.strftime("%Y%m%d")
    outFilePath = args["PathOutput"] / f"CookTerrainAttributes10m2_P3A1_{dateNow}.csv"

    result.to_csv(outFilePath, index = False)

    return 0

if __name__ == "__main__":
    cwd = pathlib.Path.cwd()
    inputDir = cwd / "data" / "input"
    outputDir = cwd / "data" / "output"

    outputDir.mkdir(parents=True, exist_ok=True)

    args = {}

    args["PathCookEast"] = inputDir / "Final terrain attributes for each georeference points from SAGA_clean version for R_ 06122019.xlsx"
    args["PathCookWest"] = inputDir / "Cookwest 250points terrain attributes and clusterID updated20191125Final.csv"
    args["PathCEGP"] = inputDir / "cookeast_georeferencepoint_20190924.geojson"
    args["PathCWGP"] = inputDir / "cookwest_georeferencepoint_20190924.geojson"
    args["PathOutput"] = outputDir

    main(args)