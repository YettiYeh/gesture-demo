import numpy as np
import pandas as pd
from sklearn import preprocessing
scaler = preprocessing.MinMaxScaler()

QUATERNION_SCALE = (1.0 / (1 << 14))

def get_features(series, generate_feature_names=False):
    if generate_feature_names:
        return ['max', 'min', 'range', 'mean', 'std']
    features = []
    features.append(max(series))
    features.append(min(series))
    features.append(max(series) - min(series))
    features.append(series.mean())
    features.append(series.std())
    return features

def get_model_features(trace, generate_feature_names=False):
    features = []
    trace["accel"] = np.linalg.norm(
        (trace["accel_ms2_x"], trace["accel_ms2_y"], trace["accel_ms2_z"]),
        axis=0)
    trace["gyro"] = np.linalg.norm(
        (trace['gyro_degs_x'], trace['gyro_degs_y'], trace['gyro_degs_z']),
        axis=0)

    for sensor in ['accel', 'gyro']:
        features_temp = get_features(trace[sensor], generate_feature_names)
        if generate_feature_names:
            features.extend([x + '_' + sensor for x in features_temp])
        else:
            features.extend(features_temp)

    # if generate_feature_names:
    #     features.append("gyro_y_z_similarity")
    # else:
    #     scaled_df = pd.DataFrame(
    #         scaler.fit_transform(trace[['gyro_degs_y', 'gyro_degs_z']]),
    #         columns=['gyro_degs_y', 'gyro_degs_z'])
    #
    #     sim = sum(scaled_df['gyro_degs_y'] * scaled_df['gyro_degs_z'])
    #
    #     features.append(sim)
    return features


def get_sensor_headers():
    header = []
    for sensor in ["accel_ms2", "mag_uT", "gyro_degs", "euler_deg",
                   "quaternion",
                   "lin_accel_ms2", "gravity_ms2"]:
        if sensor is "quaternion":
            header.append(sensor + "_w")
        header.append(sensor + "_x")
        header.append(sensor + "_y")
        header.append(sensor + "_z")
    return header


