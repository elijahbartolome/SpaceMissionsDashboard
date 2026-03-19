import pandas as pd
from datetime import datetime
from pydantic import validate_call

df = pd.read_csv("space_missions.csv")

@validate_call
def getMissionCountByCompany(companyName: str) -> int:
    return len(df[df["Company"] == companyName]["Mission"].unique())

@validate_call
def getSuccessRate(companyName: str) -> float:
    companyDF = df[df["Company"] == companyName]
    numMissions = len(companyDF["Mission"].unique())
    if numMissions == 0:
        return 0.0
    
    numSuccess = len(companyDF[companyDF["MissionStatus"] == "Success"]["Mission"].unique())

    # Round to two decimal places as a percentage
    return round((numSuccess/numMissions) * 100, 2)

@validate_call
def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    try:
        start = datetime.strptime(startDate, "%Y-%m-%d")
        end = datetime.strptime(endDate, "%Y-%m-%d")
    except:
        raise ValueError("Invalid Date Format. Must be YYYY-MM-DD")
    
    if end < start:
        raise ValueError("startDate must be before or at endDate")
    df["Date"] = pd.to_datetime(df["Date"])

    filteredDF = df[df["Date"].between(start, end, inclusive="both")]

    sortedMissions = filteredDF.sort_values(by="Date")["Mission"].unique()

    return list(sortedMissions)

@validate_call
def getTopCompaniesByMissionCount(n: int) -> list:
    if n < 0:
        raise ValueError("Invalid n. Must be equal or greater than 0.")
    
    # Group by Company with Mission Count Aggregate
    groupedDF = df.groupby("Company")["Mission"].nunique()
    # Sort by Mission count then Company alphabetically
    sortedDF = groupedDF.reset_index(name="Count")
    sortedDF = sortedDF.sort_values(by=["Count", "Company"], ascending=[False, True])

    headDF = sortedDF.head(n)

    return list(headDF.itertuples(index=False, name=None))

@validate_call
def getMissionStatusCount() -> dict:
    groupedDF = df.groupby("MissionStatus")["Mission"].unique().reset_index()
    groupedDF["count"] = groupedDF["Mission"].apply(len)

    return groupedDF.set_index("MissionStatus")["count"].to_dict()

@validate_call
def getMissionsByYear(year: int) -> int:
    df["Year"] = pd.to_datetime(df["Date"]).dt.year

    groupedDF = df.groupby("Year")["Mission"].nunique()

    return groupedDF[year]

@validate_call
def getMostUsedRocket() -> str:
    # Group by Rocket
    groupedDF = df.groupby("Rocket").size()
    groupedDF = groupedDF.reset_index(name="Count")

    sortedDF = groupedDF.sort_values(by=["Count", "Rocket"], ascending=[False, True])

    return sortedDF["Rocket"].iloc[0]

@validate_call
def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    if endYear < startYear:
        raise ValueError("startYear must be less or equal to endYear")
    df["Year"] = pd.to_datetime(df["Date"]).dt.year

    groupedDF = df.groupby(["Year", "Mission"])["Mission"].nunique()
    groupedDF = groupedDF.reset_index(name="Count")
    
    filteredDF = groupedDF[groupedDF["Year"].between(startYear, endYear, inclusive="both")]
    
    numMissions = filteredDF["Count"].sum()
    numYears = (endYear - startYear) + 1

    return round((numMissions/numYears), 2)

def main():
    print("1.")
    print(getMissionCountByCompany("NASA"))

    print("2.")
    print(getSuccessRate("NASA"))

    print("3.")
    print(getMissionsByDateRange("1957-10-01", "1957-12-31"))

    print("4.")
    print(getTopCompaniesByMissionCount(3))

    print("5.")
    print(getMissionStatusCount())

    print("6.")
    print(getMissionsByYear(2020))

    print("7.")
    print(getMostUsedRocket())

    print("8.")
    print(getAverageMissionsPerYear(2010, 2020))

if __name__ == "__main__":
    main()