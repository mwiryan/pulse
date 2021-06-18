"""
Implements web scraper for collecting PULSE data
"""
from datetime import datetime
import os
import numpy as np
import pandas as pd
from pprint import pprint
import re
import requests
import sys
import urllib.request
from zipfile import ZipFile
import urllib.request
from typing import Dict
import shutil


class PULSE:
    def __init__(self):
        self.source_url = "https://www.census.gov/programs-surveys/household-pulse-survey/datasets.html"
        self.data_store = r'../data'
        self.links = self._connect()

    def logging(self):
        """
        Logs information
        """
        pass

    def _connect(self) -> Dict:
        """
        Connects to the source page and collects information about rounds of the
        survey, which are subsequently returned and stored as the links attribute
        of the PULSE class.

        :returns: A dictionary whose keys correspond to a round of the survey and
        whose items correspond to the associated URL
        """
        print(f'Attempting to connect to {self.source_url}\n')

        page = requests.get(self.source_url)
        if any(re.findall(r'href.*CSV\.zip', page.text)):
            matches = re.findall(r'href.*CSV\.zip', page.text)
            links = [re.sub(r'href=\"', 'https:', l) for l in matches]
            weeks = [int(re.sub(r'wk', '', re.search(r'wk[0-9]+', link).group(0))) for link in links]
            print(f'Succeessfully connected and identified {len(weeks)} rounds of the survey.\n')

        return {int(re.sub(r'wk', '', re.search(r'wk[0-9]{,2}', l).group(0))): re.sub(r'href=\"', 'https:', l) for l in
                matches}

    def download(self, survey_round: int) -> None:
        """
        Downloads a specified round of the PULSE survey.

        :param survey_round: An integer indicating the round of the survey to download
        :returns: None
        """
        # Download round of data
        files = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(self.data_store)) for f in fn]
        matches = [file for file in files if re.search(fr'{survey_round}', file)]
        if matches:
            print(f'Round {survey_round} of the survey has already been collected and is available at {self.data_store}.\n')
        else:
            url = pulse.links[survey_round]
            file_name = re.sub(r'.*HPS_', '', url)
            save_path = os.path.join(self.data_store, 'zipped', file_name)
            print(f'Collecting data for round {survey_round} from {url}.\n')
            urllib.request.urlretrieve(url, save_path)
            with ZipFile(save_path, 'r') as f:
                f.extractall(path=os.path.join(self.data_store, 'zipped'))

            # Move zip contents to respective locations
            unzipped = [file for file in os.listdir(os.path.join(self.data_store, 'zipped')) if
                        re.search(r'^pulse', file)]
            assert len(unzipped) == 3
            for file in unzipped:
                if re.search(r'dictionary', file):
                    print(fr'Moving {file} to ../docs/raw')
                    shutil.move(os.path.join(self.data_store, 'zipped', file),
                                os.path.join(r'../docs/raw', file))
                elif re.search(r'repwgt', file):
                    print(fr'Moving {file} to ../data/weights')
                    shutil.move(os.path.join(self.data_store, 'zipped', file),
                                os.path.join(self.data_store, 'weights', file))
                else:
                    print(fr'Moving {file} to ../data/raw')
                    shutil.move(os.path.join(self.data_store, 'zipped', file),
                                os.path.join(self.data_store, 'raw', file))

        return None

    def update(self) -> None:
        """
        Updates data with all rounds not currently available at ../data.

        :returns: None
        """
        weeks = [re.sub(r'[A-z_.]', '', file) for file in os.listdir(os.path.join(pulse.data_store, 'zipped'))]
        for week in pulse.links.items():
            if week in weeks:
                continue
            else:
                pulse.download(survey_round=int(week))

        return None

    def combine(self):
        """
        Combines rounds of data
        """
        pass

    def clean(self):
        """
        Processes the data
        """
        pass

if __name__ == "__main__":
    pulse = PULSE()
    pulse.download(survey_round=25)

    df = pd.read_csv(os.path.join(pulse.data_store, 'raw', os.listdir(r'../data/raw')[0]))
    df.head()




