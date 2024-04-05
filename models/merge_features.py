import numpy as np
import pycountry_convert as pc
import pandas as pd

class MergeFeatures(object):

    def __init__(self, co2_df, forest_df, land_df, temp_df):
        self.co2_df = co2_df
        self.forest_df = forest_df
        self.land_df = land_df
        self.temp_df = temp_df

    @staticmethod
    def map_country_to_continent(entity):
        try:
            country_code = pc.country_name_to_country_alpha2(entity)
            continent_code = pc.country_alpha2_to_continent_code(country_code)
            continent_name = pc.convert_continent_code_to_continent_name(continent_code)
            custom_mapping = {
                'Asia': 'Asia and Pacific',
                'Europe': 'Europe and Central Asia',
                'Africa': 'Africa',
                'North America': 'North America',
                'South America': 'Latin America and the Caribbean',
                'Oceania': 'Asia and Pacific',
                'Antarctica': 'World'
            }
            mapped_continent = custom_mapping.get(continent_name, continent_name)
            return [mapped_continent, 'World'] if mapped_continent != 'World' else ['World']
        except:
            return None
    
    def merge(self):
        self.co2_df['Entity'] = 'World'

        # merge forest area
        self.forest_df['Custom Continent'] = self.forest_df['Entity'].apply(MergeFeatures.map_country_to_continent)
        expanded_rows = []
        for _, row in self.forest_df.iterrows():
            categories = row['Custom Continent']
            if categories:
                for category in categories:
                    expanded_row = row.to_dict()
                    expanded_row['Custom Continent'] = category
                    expanded_rows.append(expanded_row)

        expanded_forest_df = pd.DataFrame(expanded_rows)
        forest_continent_aggregated = expanded_forest_df.groupby(['Custom Continent', 'Year'])['Forest area'].sum().reset_index()
        merged_df = pd.merge(self.co2_df, forest_continent_aggregated, left_on=['Entity', 'Year'], right_on=['Custom Continent', 'Year'], how='inner')
        merged_df = merged_df.drop(columns=['Custom Continent'])

        # merge land use
        self.land_df['Custom Continent'] = self.land_df['Entity'].apply(MergeFeatures.map_country_to_continent)
        expanded_rows = []
        for _, row in self.land_df.iterrows():
            categories = row['Custom Continent']
            if categories:
                for category in categories:
                    expanded_row = row.to_dict()
                    expanded_row['Custom Continent'] = category
                    expanded_rows.append(expanded_row)

        expanded_land_df = pd.DataFrame(expanded_rows)
        land_continent_aggregated = expanded_land_df.groupby(['Custom Continent', 'Year']).agg({
            'Land use: Built-up area': 'sum',
            'Land use: Grazingland': 'sum',
            'Land use: Cropland': 'sum'
        }).reset_index()
        merged_df = pd.merge(merged_df, land_continent_aggregated, left_on=['Entity', 'Year'], right_on=['Custom Continent', 'Year'], how='inner').drop(columns=['Custom Continent'])

        # merge temperature anomaly
        self.temp_df['Custom Continent'] = self.temp_df['Entity'].apply(MergeFeatures.map_country_to_continent)
        expanded_rows = []
        for _, row in self.temp_df.iterrows():
            categories = row['Custom Continent']
            if categories:
                for category in categories:
                    expanded_row = row.to_dict()
                    expanded_row['Custom Continent'] = category
                    expanded_rows.append(expanded_row)

        expanded_temp_df = pd.DataFrame(expanded_rows)
        temp_continent_aggregated = expanded_temp_df.groupby(['Custom Continent', 'Year'])['Temperature anomaly'].mean().reset_index()
        merged_df = pd.merge(merged_df, temp_continent_aggregated, left_on=['Entity', 'Year'], right_on=['Custom Continent', 'Year'], how='inner')
        merged_df = merged_df.drop(columns=['Custom Continent'])
        
        return merged_df