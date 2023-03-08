from GHCND import *
import json
import sys


def get_station_counts():
    """
    Counts the number of gaps in all station files.
    """
    ghn = GHNCD()
    ghn.readCountriesFile()
    ghn.readStationsFile()

    # get list of station names
    station_names = ghn.getStatKeyNames()

    # count number of gaps in each station
    counts = {}
    for station in station_names:
        try:
            # get url for a given station index
            fileName = f"{station}.dly"
            urlName = 'http://www.hep.ucl.ac.uk/undergrad/0056/other/projects/ghcnd/ghcnd_gsn/' + fileName

            # copy station data from remote to local
            destination = f"data/{fileName}"
            urllib.request.urlretrieve(urlName, destination)
            statDict = ghn.processFile(destination)
            print(ghn.getStation(station))

            var = Variable(ghn.getVar(statDict, 'TMAX'),
                           "max temp (degC)", ghn.stationDict[station].name)
            var.convert_time()
            count = var.count_gaps()
            counts[station] = count
        except Exception:
            print(f"Gaps couldn't be counted for station {station}")
            continue

    # save output in text file
    with open("stat_counts_tmax.txt", "a") as f:
        json.dump(counts, f, indent=2)


if __name__ == "__main__":
    # if len(sys.argv) != 1:
    #    sys.exit("Usage: get_station")
    # print(str(sys.argv))

    get_station_counts()
