from joblib import dump, load
import pandas as pd
import pyarrow.parquet as pq
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


class dota_ai():
    def __init__(self):
        table = pq.read_table('dota2_matches.parquet')
        self.df = table.to_pandas()

        self.df_player_name = pd.DataFrame()
        self.df_player_id = pd.DataFrame()
        self.df_hero = pd.DataFrame()
        self.df_hero_id = pd.DataFrame()
        self.df_team = pd.DataFrame()
        self.df_team_id = pd.DataFrame()
        self.df_team = pd.concat([self.df_team, self.df['radiant_team_name']], ignore_index=True).drop_duplicates()
        self.df_team = pd.concat([self.df_team, self.df['dire_team_name']], ignore_index=True).drop_duplicates()
        self.df_team_id = pd.concat([self.df_team_id, self.df['radiant_team_id']], ignore_index=True).drop_duplicates()
        self.df_team_id = pd.concat([self.df_team_id, self.df['dire_team_id']],ignore_index=True).drop_duplicates()

        for i in range(1,6):
            self.df_player_name = pd.concat([self.df_player_name, self.df[f'radiant_player_{i}_name']],ignore_index=True).drop_duplicates()
            self.df_player_name = pd.concat([self.df_player_name, self.df[f'dire_player_{i}_name']], ignore_index=True).drop_duplicates()
            self.df_player_id = pd.concat([self.df_player_id, self.df[f'radiant_player_{i}_id']],ignore_index=True).drop_duplicates()
            self.df_player_id = pd.concat([self.df_player_id, self.df[f'dire_player_{i}_id']], ignore_index=True).drop_duplicates()
            self.df_hero = pd.concat([self.df_hero, self.df[f'radiant_player_{1}_hero']], ignore_index=True).drop_duplicates()
            self.df_hero = pd.concat([self.df_hero, self.df[f'dire_player_{1}_hero']], ignore_index=True).drop_duplicates()
            self.df_hero_id = pd.concat([self.df_hero_id, self.df[f'radiant_player_{1}_hero_id']], ignore_index=True).drop_duplicates()
            self.df_hero_id = pd.concat([self.df_hero_id, self.df[f'dire_player_{1}_hero_id']], ignore_index=True).drop_duplicates()


        mas_del = ['league', 'league_id', 'league_start_date_time', 'league_end_date_time', 'league_region',
                   'series_id', 'series_type', 'match_id',
                   'match_start_date_time', 'radiant_team_name', 'dire_team_name',
                   'radiant_player_1_hero', 'radiant_player_1_position', 'radiant_player_1_lane',
                   'radiant_player_1_role', 'radiant_player_1_name',
                   'radiant_player_2_hero', 'radiant_player_2_position', 'radiant_player_2_lane',
                   'radiant_player_2_role', 'radiant_player_2_name',
                   'radiant_player_3_hero', 'radiant_player_3_position', 'radiant_player_3_lane',
                   'radiant_player_3_role', 'radiant_player_3_name',
                   'radiant_player_4_hero', 'radiant_player_4_position', 'radiant_player_4_lane',
                   'radiant_player_4_role', 'radiant_player_4_name',
                   'radiant_player_5_hero', 'radiant_player_5_position', 'radiant_player_5_lane',
                   'radiant_player_5_role', 'radiant_player_5_name',
                   'dire_player_1_hero', 'dire_player_1_position', 'dire_player_1_lane', 'dire_player_1_role',
                   'dire_player_1_name',
                   'dire_player_2_hero', 'dire_player_2_position', 'dire_player_2_lane', 'dire_player_2_role',
                   'dire_player_2_name',
                   'dire_player_3_hero', 'dire_player_3_position', 'dire_player_3_lane', 'dire_player_3_role',
                   'dire_player_3_name',
                   'dire_player_4_hero', 'dire_player_4_position', 'dire_player_4_lane', 'dire_player_4_role',
                   'dire_player_4_name',
                   'dire_player_5_hero', 'dire_player_5_position', 'dire_player_5_lane', 'dire_player_5_role',
                   'dire_player_5_name',
                   'game_version_id', 'league_tier']

        for i in mas_del:
            del self.df[i]

    # Обучение модели
    def train(self,n):

        df = self.df.head(n)

        # Заполнение пропусков
        for column in df.columns:
            if df[column].dtype == 'object':  # Если это строка
                df[column].fillna('Unknown', inplace=True)
            elif pd.api.types.is_numeric_dtype(df[column]):  # Если это числовой тип
                df[column].fillna(0, inplace=True)
            elif pd.api.types.is_datetime64_any_dtype(df[column]):  # Если это datetime
                df[column].fillna(pd.NaT, inplace=True)

        # Целевая переменная
        X = df.drop(['winner_id'], axis=1)  # Все столбцы, кроме winner_id
        y = df['winner_id']  # Целевая переменная

        # Разделение данных на обучающую и тестовую выборки
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.X_test = df.drop(['winner_id'], axis=1)
        self.y_test = df['winner_id']

        # Обучение модели
        model = RandomForestClassifier(random_state=42)
        self.s = model.fit(X_train, y_train)

    # Сохранение обучения модели
    def save_model(self):
        dump(self.s, 'D:/model/model_fit.joblib')

    # Загрузка обученной модели
    def load_model(self):
        self.s = load('D:/model/model_fit.joblib')

    # Тестовая хуета хз надо ли оно будет потом
    def result(self, data):
        pred = self.s.predict(data)
        return pred

    def search_id(self, data):
        #тестовая хуеверть
        data = {'radiant_team_name',
                'dire_team_name',
                'radiant_player_1_hero',
                'radiant_player_1_name',
                'radiant_player_2_hero',
                'radiant_player_2_name',
                'radiant_player_3_hero',
                'radiant_player_3_name',
                'radiant_player_4_hero',
                'radiant_player_4_name',
                'radiant_player_5_hero',
                'radiant_player_5_name',
                'dire_player_1_hero',
                'dire_player_1_name',
                'dire_player_2_hero',
                'dire_player_2_name',
                'dire_player_3_hero',
                'dire_player_3_name',
                'dire_player_4_hero',
                'dire_player_4_name',
                'dire_player_5_hero',
                'dire_player_5_name'}





    
