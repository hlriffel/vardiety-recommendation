from pathlib import Path

import pandas as pd
import os

from ..storage import Storage


class CombinationController:
    @staticmethod
    def get_data_frame():
        path_to_csv = '/tmp/combinations.csv'
        csv = Path(path_to_csv)

        if csv.is_file():
            os.remove(path_to_csv)

        Storage.download_file(path_to_csv, 'combinations.csv')

        combinations = pd.read_csv(path_to_csv, sep=',', names=['combination_id', 'items'])

        return pd.DataFrame(combinations)

    @staticmethod
    def get_combination_id(
            items_string,
            self
    ):
        df = self.get_data_frame()

        combination = df.loc(df['items'] == items_string, ['combination_id'])

        if combination.count() > 0:
            return combination['combination_id']
        else:
            return self.add_combination(items_string)

    @staticmethod
    def add_combination(
            items_string,
            self
    ):
        df = self.get_data_frame()
        combination_id = df['combination_id'].max() + 1

        df = df.append([].append({'combination_id': combination_id, 'items': items_string}))

        df.to_csv(r'/tmp/combinations.csv', sep=',', columns=['combination_id', 'items'])

        Storage.upload_file('/tmp/combinations.csv', 'combinations.csv')

        return combination_id
