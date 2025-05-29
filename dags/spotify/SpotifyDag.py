import os
import pathlib
import secrets
import string
import sys
from dataclasses import dataclass
from datetime import timedelta

import requests

# from ...lib.Logger import Logger, LogItem
# from ...lib.Processors import Authenticator, DataProcessor, ItemProcessor

lib = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "lib")
sys.path.append(lib)
from Processors import Authenticator, DataProcessor, ItemProcessor, LogItem


@dataclass
class LogData(DataProcessor):
    dag_logs: list


@dataclass
class SpotifyData(DataProcessor):
    user_top_artists: list
    user_top_tracks: list


@dataclass
class Tracks(ItemProcessor):
    track_id: str
    track_name: str
    artist_ids: list
    rs_rank: int
    is_explicit: bool
    popularity: int
    duration_ms: int
    track_number_on_album: int
    external_url: str
    uri: str
    released_year: int
    album_id: str
    thumbnail: str

    # Compare with Other Objects:
    def __eq__(self, other):
        # If type is the same.
        if isinstance(other, Tracks):
            if other.track_id == self.track_id:
                return True
            else:
                return False
        # If it's a string
        elif isinstance(other, str):
            if other == self.track_id:
                return True
            else:
                return False
        # Every other just in case.
        else:
            return False


@dataclass
class Artists(ItemProcessor):
    artist_id: str
    artist_name: str
    albums: list
    genres: list
    total_followers: int
    rs_rank: int
    popularity: int
    external_url: str
    uri: str
    thumbnail: str

    # Compare with Other Objects:
    def __eq__(self, other):
        # If type is the same.
        if isinstance(other, Artists):
            if other.artist_id == self.artist_id:
                return True
            else:
                return False
        # If it's a string
        elif isinstance(other, str):
            if other == self.artist_id:
                return True
            else:
                return False
        # Every other just in case.
        else:
            return False


class SpotifyApi(Authenticator):
    def m_RequestAccessCode(client_id):
        def generate_state(lenght=50):
            characters = string.ascii_letters + string.digits
            result_str = "".join(secrets.choice(characters) for i in range(lenght))
            return result_str

        state = generate_state()
        redirect_uri = "https://csabakeller.com/api/webscrapers/authenticate/"
        scope = (
            "user-top-read"
            + "%20"
            + "user-read-recently-played"
            + "%20"
            + "user-read-email"
            + "%20"
            + "playlist-read-private"
            + "%20"
            + "playlist-modify-private"
        )
        url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}&state={state}"

        r = requests.get(url=url).json()
        print(r)
        code = r["code"]
        return code

    def m_RequestAccessToken(self):
        client_id = self.getClientId()
        code = SpotifyApi.m_RequestAccessCode(client_id=client_id)
        url = "https://accounts.spotify.com/api/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": self.getClientSecret(),
            "redirect_uri": "https://csabakeller.com/api/webscrapers/authenticate/",
            "code": code,
        }
        r = requests.post(url=url, data=payload).json()
        expires_in = r["expires_in"]
        new_expiry_date = self.today + timedelta(seconds=expires_in)

        self.keys["CODE"] = code
        self.keys["ACCESS_TOKEN"] = r["access_token"]
        self.keys["EXPIRY_DATE"] = new_expiry_date.strftime("%Y-%m-%d %H:%M:%S")
        self.keys["SCOPE"] = r["scope"]
        self.keys["REFRESH_TOKEN"] = r["refresh_token"]
        self.saveJson()

    def __init__(self):
        super().__init__(account="SPOTIFY")
        # self.m_RequestAccessCode()
        # self.m_RequestAccessToken()
        self.auth_log = self.RequestRefreshToken()

    def FetchUserProfile(self):
        url = f"https://api.spotify.com/v1/users/{self.keys["USER_ID"]}"
        return requests.get(url=url, headers=self.getHeaders()).json()

    def FetchTopItems(self, query_type, limit):
        url = f"https://api.spotify.com/v1/me/top/{query_type}?time_range=medium_term&limit={limit}"
        r = requests.get(url=url, headers=self.getHeaders()).json()
        ids = [item["id"] for item in r["items"]]
        return ids

    def FetchBatchTracks(self) -> list:
        # Log
        log_item = LogItem(
            project_name="spotify", task_name=self.FetchBatchTracks.__name__
        )

        tracks_data = list()
        top_tracks = SpotifyApi.FetchTopItems(self, query_type="tracks", limit=15)
        print(f"Fetching {len(top_tracks)} number of Tracks...")
        search_str = ",".join(top_tracks)
        url = f"https://api.spotify.com/v1/tracks?market=GB&ids={search_str}"
        r = requests.get(url=url, headers=self.getHeaders())

        if r.status_code == 200:
            response = r.json()

            for rank, item in enumerate(response["tracks"]):
                name = item["name"]
                track_id = item["id"]
                rs_rank = rank
                duration_ms = int(item["duration_ms"])
                explicit = item["explicit"]
                popularity = int(item["popularity"])
                track_number = int(item["track_number"])
                external_urls = item["external_urls"]["spotify"]
                released_year = int(item["album"]["release_date"][:4])
                album_id = item["album"]["id"]
                # artists = [artist["id"] for artist in item["artists"]]
                artists = [artist["name"] for artist in item["artists"]]
                uri = item["uri"]
                thumbnail = item["album"]["images"][0]["url"]

                track = Tracks(
                    track_name=name,
                    rs_rank=rs_rank,
                    track_id=track_id,
                    artist_ids=artists,
                    album_id=album_id,
                    duration_ms=duration_ms,
                    is_explicit=explicit,
                    popularity=popularity,
                    track_number_on_album=track_number,
                    external_url=external_urls,
                    uri=uri,
                    released_year=released_year,
                    thumbnail=thumbnail,
                )

                tracks_data.append(track)
            log_item.log_actions(
                data_items=len(tracks_data),
                description=r.reason,
                status_code=r.status_code,
            )
        else:
            log_item.log_actions(
                data_items=len(tracks_data),
                description=r.reason,
                status_code=r.status_code,
            )

        data = (log_item, tracks_data)
        return data

    def FetchBatchArtists(self) -> list:
        # Log
        log_item = LogItem(
            project_name="spotify", task_name=self.FetchBatchArtists.__name__
        )

        artists_data = list()
        top_artists = SpotifyApi.FetchTopItems(self, query_type="artists", limit=15)
        print(f"Fetching {len(top_artists)} number of Artists...")
        search_str = ",".join(top_artists)
        url = f"https://api.spotify.com/v1/artists?ids={search_str}"
        r = requests.get(url=url, headers=self.getHeaders())

        if r.status_code == 200:
            response = r.json()
            for rank, item in enumerate(response["artists"]):
                artist_id = item["id"]
                artist_name = item["name"]
                genres = item["genres"]
                total_followers = item["followers"]["total"]
                rs_rank = rank
                popularity = item["popularity"]
                external_url = item["external_urls"]["spotify"]
                uri = item["uri"]
                thumbnail = item["images"][0]["url"]

                if len(genres) > 1:
                    cleaned_genres = [genre.replace("'", "") for genre in genres]
                else:
                    cleaned_genres = ["NONE"]

                artist = Artists(
                    artist_id=artist_id,
                    artist_name=artist_name,
                    albums=["NONE"],
                    genres=cleaned_genres,
                    rs_rank=rs_rank,
                    total_followers=total_followers,
                    popularity=popularity,
                    external_url=external_url,
                    uri=uri,
                    thumbnail=thumbnail,
                )
                artists_data.append(artist)

            log_item.log_actions(
                data_items=len(artists_data),
                description=r.reason,
                status_code=r.status_code,
            )
        else:
            log_item.log_actions(
                data_items=len(artists_data),
                description=r.reason,
                status_code=r.status_code,
            )

        data = (log_item, artists_data)
        return data


def main() -> None:
    # Admin
    dataPath = os.path.join(pathlib.Path(__file__).parent.resolve(), "sql")
    spotify = SpotifyApi()

    # Main
    artists_log, artists = spotify.FetchBatchArtists()
    tracks_log, tracks = spotify.FetchBatchTracks()
    spotifyData = SpotifyData(user_top_artists=artists, user_top_tracks=tracks)
    spotifyData.save_data_to_sql(schema="spotify", sql_folder_path=dataPath)

    # Log
    L = LogData(dag_logs=[spotify.auth_log, artists_log, tracks_log])
    L.save_data_to_sql(schema="logs", sql_folder_path=dataPath)


if __name__ == "__main__":
    main()
