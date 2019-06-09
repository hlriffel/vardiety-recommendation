from pathlib import Path
from turicreate import item_similarity_recommender, SFrame

import pandas as pd
import os

from ..storage import Storage
from .combination import CombinationController


class PreferenceController:

    PREFERENCES_PATH = '/tmp/preferences.csv'
    COMBINATIONS_PATH = '/tmp/combinations.csv'

    @staticmethod
    def get_data_frame(
            data_type='pref'
    ):
        if data_type == 'pref':
            filename = 'preferences.csv'
            columns = ['user_id', 'combination_id', 'rating']
        else:
            filename = 'combinations.csv'
            columns = ['combination_id', 'items']

        path_to_csv = '/tmp/' + filename
        csv = Path(path_to_csv)

        if csv.is_file():
            os.remove(path_to_csv)

        Storage.download_file(path_to_csv, filename)

        combinations = pd.read_csv(path_to_csv, sep=',', names=columns)

        return pd.DataFrame(combinations)

    @staticmethod
    def add_user_preference(
            user_id,
            items_string,
            rating,
            self
    ):
        df = self.get_data_frame('pref')
        combination_id = CombinationController.get_combination_id(items_string)
        new_combination = {'user_id': user_id, 'combination_id': combination_id, 'rating': rating}

        df = df.append([].append(new_combination))

        df.to_csv(r'/tmp/preferences.csv', sep=',', columns=['user_id', 'combination_id', 'rating'])

        Storage.upload_file(self.PREFERENCES_PATH, 'preferences.csv')

        return new_combination

    @staticmethod
    def get_user_preferences(
            user_id,
            self
    ):
        pref_df = self.get_data_frame('pref')
        comb_df = self.get_data_frame('comb')

        ratings_frame = SFrame(pd.merge(pref_df, comb_df, on='combination_id'))

        item_sim_model = item_similarity_recommender.create(
            ratings_frame,
            user_id='user_id',
            item_id='combination_id',
            target='rating',
            similarity_type='cosine'
        )

        return item_sim_model.recommend(users=[].append(user_id), k=10).to_dataframe().values
