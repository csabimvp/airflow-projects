import os
import pathlib
import random
import string

# import sys
from dataclasses import dataclass
from datetime import datetime

import requests

from ...lib.Processors import Authenticator, DataProcessor, ItemProcessor

# lib = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "lib")
# sys.path.append(lib)
# from Processors import Authenticator, DataProcessor, ItemProcessor


@dataclass
class StravaAthleteStats(ItemProcessor):
    activity_id: str
    activity_count: int
    athlete_id: str
    date_refreshed: str
    distance: float
    elapsed_time: int
    elevation_gain: float
    moving_time: int
    stat_type: str
    sport_type: str

    def generate_id():
        characterList = string.ascii_letters + string.digits
        myId = "".join([random.choice(characterList) for i in range(30)])
        return myId


@dataclass
class StravaActivityItem(ItemProcessor):
    activity_id: str
    athlete_id: str
    average_speed: float
    distance: float
    elapsed_time: int
    elev_high: float
    elev_low: float
    external_id: str
    gear_id: str
    kudos_count: int
    comment_count: int
    pr_count: int
    achievement_count: int
    latitude: float
    longitude: float
    moving_time: int
    source_system: str
    sport_type: str
    start_date: str
    total_elevation_gain: float


@dataclass
class StravaData(DataProcessor):
    """
    Distance is in meters
    Time is in seconds.
    """

    athlete_stats: list
    athlete_activities: list


class StravaApi(Authenticator):
    def __init__(self):
        super().__init__(account="STRAVA")
        self.RequestRefreshToken()

    def FetchAthleteStats(self):
        athlete_id = "87270249"
        date_refreshed = datetime.now().strftime("%Y-%m-%d")
        url = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"
        data = requests.get(url, headers=self.getHeaders()).json()

        # All
        allRun = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["all_run_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["all_run_totals"]["distance"],
            elapsed_time=data["all_run_totals"]["elapsed_time"],
            elevation_gain=data["all_run_totals"]["elevation_gain"],
            moving_time=data["all_run_totals"]["moving_time"],
            stat_type="all_time",
            sport_type="running",
        )
        allRide = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["all_ride_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["all_ride_totals"]["distance"],
            elapsed_time=data["all_ride_totals"]["elapsed_time"],
            elevation_gain=data["all_ride_totals"]["elevation_gain"],
            moving_time=data["all_ride_totals"]["moving_time"],
            stat_type="all_time",
            sport_type="cycling",
        )
        allSwim = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["all_swim_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["all_swim_totals"]["distance"],
            elapsed_time=data["all_swim_totals"]["elapsed_time"],
            elevation_gain=data["all_swim_totals"]["elevation_gain"],
            moving_time=data["all_swim_totals"]["moving_time"],
            stat_type="all_time",
            sport_type="swimming",
        )

        # Recent
        recentRun = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["recent_run_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["recent_run_totals"]["distance"],
            elapsed_time=data["recent_run_totals"]["elapsed_time"],
            elevation_gain=data["recent_run_totals"]["elevation_gain"],
            moving_time=data["recent_run_totals"]["moving_time"],
            stat_type="recent",
            sport_type="running",
        )
        recentRide = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["recent_ride_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["recent_ride_totals"]["distance"],
            elapsed_time=data["recent_ride_totals"]["elapsed_time"],
            elevation_gain=data["recent_ride_totals"]["elevation_gain"],
            moving_time=data["recent_ride_totals"]["moving_time"],
            stat_type="recent",
            sport_type="cycling",
        )
        recentSwim = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["recent_swim_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["recent_swim_totals"]["distance"],
            elapsed_time=data["recent_swim_totals"]["elapsed_time"],
            elevation_gain=data["recent_swim_totals"]["elevation_gain"],
            moving_time=data["recent_swim_totals"]["moving_time"],
            stat_type="recent",
            sport_type="swimming",
        )

        # YtD
        ytdRun = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["ytd_run_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["ytd_run_totals"]["distance"],
            elapsed_time=data["ytd_run_totals"]["elapsed_time"],
            elevation_gain=data["ytd_run_totals"]["elevation_gain"],
            moving_time=data["ytd_run_totals"]["moving_time"],
            stat_type="year_to_date",
            sport_type="running",
        )
        ytdRide = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["ytd_ride_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["ytd_ride_totals"]["distance"],
            elapsed_time=data["ytd_ride_totals"]["elapsed_time"],
            elevation_gain=data["ytd_ride_totals"]["elevation_gain"],
            moving_time=data["ytd_ride_totals"]["moving_time"],
            stat_type="year_to_date",
            sport_type="cycling",
        )
        ytdSwim = StravaAthleteStats(
            activity_id=StravaAthleteStats.generate_id(),
            activity_count=data["ytd_swim_totals"]["count"],
            athlete_id=athlete_id,
            date_refreshed=date_refreshed,
            distance=data["ytd_swim_totals"]["distance"],
            elapsed_time=data["ytd_swim_totals"]["elapsed_time"],
            elevation_gain=data["ytd_swim_totals"]["elevation_gain"],
            moving_time=data["ytd_swim_totals"]["moving_time"],
            stat_type="year_to_date",
            sport_type="swimming",
        )

        # Stats
        stats = [
            allRun,
            allRide,
            allSwim,
            recentRun,
            recentRide,
            recentSwim,
            ytdRun,
            ytdRide,
            ytdSwim,
        ]
        return stats

    def FetchAllAthleteActivities(self):
        # First item is the latest, last item is the oldest activity.
        data = list()
        nextPage = True
        pageNumber = 1
        headers = self.getHeaders()
        while nextPage:
            url = f"https://www.strava.com/api/v3/activities?page={pageNumber}"
            r = requests.get(url, headers=headers)
            status_code = r.status_code
            print(f"url: {url} --- {status_code}")

            if status_code == 200:
                activities = r.json()
                if len(activities) != 0:
                    for activity in activities:

                        # Try/Except is required due to missing Elevation AND/OR Latitutude/Longitude data for some activities.
                        try:
                            activityItem = StravaActivityItem(
                                activity_id=str(activity["id"]),
                                athlete_id=str(activity["athlete"]["id"]),
                                average_speed=activity["average_speed"],
                                distance=activity["distance"],
                                elapsed_time=activity["elapsed_time"],
                                elev_high=activity["elev_high"],
                                elev_low=activity["elev_low"],
                                external_id=activity["external_id"],
                                gear_id=activity["gear_id"],
                                kudos_count=activity["kudos_count"],
                                comment_count=activity["comment_count"],
                                pr_count=activity["pr_count"],
                                achievement_count=activity["achievement_count"],
                                latitude=float(activity["start_latlng"][0]),
                                longitude=float(activity["start_latlng"][1]),
                                moving_time=activity["moving_time"],
                                source_system="strava",
                                sport_type=activity["sport_type"].lower(),
                                start_date=activity["start_date"],
                                total_elevation_gain=activity["total_elevation_gain"],
                            )
                        except KeyError:
                            print(activity["id"])
                            # key = e.args[0]
                            try:
                                activityItem = StravaActivityItem(
                                    activity_id=str(activity["id"]),
                                    athlete_id=str(activity["athlete"]["id"]),
                                    average_speed=activity["average_speed"],
                                    distance=activity["distance"],
                                    elapsed_time=activity["elapsed_time"],
                                    elev_high=float(0),
                                    elev_low=float(0),
                                    external_id=activity["external_id"],
                                    gear_id=activity["gear_id"],
                                    kudos_count=activity["kudos_count"],
                                    comment_count=activity["comment_count"],
                                    pr_count=activity["pr_count"],
                                    achievement_count=activity["achievement_count"],
                                    latitude=float(activity["start_latlng"][0]),
                                    longitude=float(activity["start_latlng"][1]),
                                    moving_time=activity["moving_time"],
                                    source_system="strava",
                                    sport_type=activity["sport_type"].lower(),
                                    start_date=activity["start_date"],
                                    total_elevation_gain=activity[
                                        "total_elevation_gain"
                                    ],
                                )
                            except IndexError:
                                activityItem = StravaActivityItem(
                                    activity_id=str(activity["id"]),
                                    athlete_id=str(activity["athlete"]["id"]),
                                    average_speed=activity["average_speed"],
                                    distance=activity["distance"],
                                    elapsed_time=activity["elapsed_time"],
                                    elev_high=float(0),
                                    elev_low=float(0),
                                    external_id=activity["external_id"],
                                    gear_id=activity["gear_id"],
                                    kudos_count=activity["kudos_count"],
                                    comment_count=activity["comment_count"],
                                    pr_count=activity["pr_count"],
                                    achievement_count=activity["achievement_count"],
                                    latitude=float(0),
                                    longitude=float(0),
                                    moving_time=activity["moving_time"],
                                    source_system="strava",
                                    sport_type=activity["sport_type"].lower(),
                                    start_date=activity["start_date"],
                                    total_elevation_gain=activity[
                                        "total_elevation_gain"
                                    ],
                                )
                        except IndexError:
                            print(activity["id"])
                            activityItem = StravaActivityItem(
                                activity_id=str(activity["id"]),
                                athlete_id=str(activity["athlete"]["id"]),
                                average_speed=activity["average_speed"],
                                distance=activity["distance"],
                                elapsed_time=activity["elapsed_time"],
                                elev_high=activity["elev_high"],
                                elev_low=activity["elev_low"],
                                external_id=activity["external_id"],
                                gear_id=activity["gear_id"],
                                kudos_count=activity["kudos_count"],
                                comment_count=activity["comment_count"],
                                pr_count=activity["pr_count"],
                                achievement_count=activity["achievement_count"],
                                latitude=float(0),
                                longitude=float(0),
                                moving_time=activity["moving_time"],
                                source_system="strava",
                                sport_type=activity["sport_type"].lower(),
                                start_date=activity["start_date"],
                                total_elevation_gain=activity["total_elevation_gain"],
                            )

                        data.append(activityItem)
                    pageNumber += 1
                else:
                    nextPage = False
            else:
                print(status_code, r)
                nextPage = False

        return data


def main() -> None:
    dataPath = os.path.join(pathlib.Path(__file__).parent.resolve(), "sql")
    strava = StravaApi()
    stats = strava.FetchAthleteStats()
    activities = strava.FetchAllAthleteActivities()
    stravaData = StravaData(athlete_stats=stats, athlete_activities=activities)
    stravaData.save_data_to_sql(schema="strava", sql_folder_path=dataPath)


if __name__ == "__main__":
    main()
