from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np


def get_genres_dummies(df: pd.DataFrame) -> pd.DataFrame:

    binarizer = MultiLabelBinarizer()

    return pd.DataFrame(
        binarizer.fit_transform(df["genres"]),
        columns=binarizer.classes_,
        index=df.index,
    )


def encode_column(df: pd.DataFrame, ml_df: pd.DataFrame) -> pd.DataFrame:

    label_encoder = LabelEncoder()
    label_encoder.fit(df["certificate"].unique())
    ml_df["certificate"] = label_encoder.transform(df["certificate"])

    return ml_df


def model_df(df: pd.DataFrame) -> pd.DataFrame:

    ml_df = get_genres_dummies(df)
    ml_df = encode_column(df, ml_df)

    return pd.concat([ml_df, df["imdb_score"].astype(float)], axis=1)


def get_clusters(ml_df: pd.DataFrame) -> pd.DataFrame:

    clusters = KMeans(n_clusters=8, random_state=0)
    _ = clusters.fit(ml_df.copy())
    ml_df["labels"] = clusters.labels_

    return ml_df


def knn_model(ml_df: pd.DataFrame, idx: int) -> np.array:

    x = ml_df.loc[:, ml_df.columns != "labels"]
    y = ml_df["labels"]

    knn = KNeighborsClassifier(n_neighbors=13, metric="euclidean")
    knn.fit(x, y)

    model_data = x.iloc[idx].tolist()

    return knn.kneighbors([model_data])[1]


def get_predictions(df: pd.DataFrame, idx: int) -> np.array:

    ml_df = model_df(df)
    ml_df = get_clusters(ml_df)

    return knn_model(ml_df, idx)
