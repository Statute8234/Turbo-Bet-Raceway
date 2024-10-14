import pandas as pd
data = pd.read_csv('dataFiles\car_db_metric.csv', header=0, usecols=['model','make','year_from','year_to','body_type','length_mm','width_mm','height_mm','front_track_mm','rear_track_mm','curb_weight_kg','engine_type','engine_hp','transmission','max_speed_km_per_h','car_class'])
print(data.head())