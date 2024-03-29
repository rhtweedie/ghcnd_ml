# Copyright 2023 Heather Tweedie
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from GHCND import *
import json
import sys


def get_station_counts(var_type='TMAX'):
    """
    Counts the number of gaps in all station files.
    """
    ghn = GHCND()
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
            destination = f"data/stations_daily/{fileName}"
            urllib.request.urlretrieve(urlName, destination)
            statDict = ghn.processFile(destination)
            print(ghn.getStation(station))

            var = Variable(ghn.getVar(statDict, var_type),
                           var_type, ghn.stationDict[station].name)
            var.convert_time()
            count = var.count_gaps()
            counts[station] = count
        except Exception:
            print(f"Gaps couldn't be counted for station {station}")
            continue

    # save output in text file
    with open(f"stat_counts_{var_type[1:-2]}.txt", "a") as f:
        json.dump(counts, f, indent=2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(str(sys.argv))
        sys.exit("Usage: get_station_counts.py [var_type]")
    get_station_counts(sys.argv[1])
