import numpy as np
import pycountry_convert as pc
import pandas as pd

class MergeFeatures(object):

    def __init__(self, co2_df, forest_df, land_df, temp_df):
        self.co2_df = co2_df
        self.forest_df = forest_df
        self.land_df = land_df
        self.temp_df = temp_df
        self.entities = ['Africa', 'Asia and Pacific', 'Europe and Central Asia', 'Latin America and the Caribbean', 'North America', 'Freshwater', 'World']

    @staticmethod
    def map_country_to_continent(entity):
        # Your existing mapping logic...
        # Return a single continent or region for simplicity in this context
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
            return custom_mapping.get(continent_name)
        except:
            return None

    def expand_co2_to_entities(self):
        # Create a copy of the CO2 dataframe for each entity
        co2_expanded_list = []
        for entity in self.entities:
            temp_co2 = self.co2_df.copy()
            temp_co2['Entity'] = entity
            co2_expanded_list.append(temp_co2)
        return pd.concat(co2_expanded_list)

    def process_dataframe(self, df):
        # Apply continent mapping and expand rows for each entity
        df['Entity'] = df['Entity'].apply(MergeFeatures.map_country_to_continent)
        return df

    def merge(self):
        co2_expanded = self.expand_co2_to_entities()

        # Process forest, land, and temperature dataframes
        forest_processed = self.process_dataframe(self.forest_df)
        land_processed = self.process_dataframe(self.land_df)
        temp_processed = self.process_dataframe(self.temp_df)

        # Start merging
        merged_df = co2_expanded
        for df in [forest_processed, land_processed, temp_processed]:
            merged_df = pd.merge(merged_df, df, on=['Entity', 'Year'], how='outer')

        # Fill NaN values that might have been introduced during the merge
        merged_df = merged_df.fillna(method='ffill').fillna(method='bfill')

        return merged_df
