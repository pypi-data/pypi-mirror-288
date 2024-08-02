import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


class DictToDataFrameTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        account_dicts = []
        for accounts in X:
            for account in accounts:
                account_dict = {
                    "user": account["user"],
                    "label": account["label"],
                    "post_1_likes": account["post_1"]["num_likes"],
                    "post_1_comments": account["post_1"]["num_comments"],
                    "post_1_share": account["post_1"]["num_shares"],
                    "post_2_likes": account["post_2"]["num_likes"],
                    "post_2_comments": account["post_2"]["num_comments"],
                    "post_2_share": account["post_2"]["num_shares"],
                    "post_3_likes": account["post_3"]["num_likes"],
                    "post_3_comments": account["post_3"]["num_comments"],
                    "post_3_share": account["post_3"]["num_shares"],
                    "post_4_likes": account["post_4"]["num_likes"],
                    "post_4_comments": account["post_4"]["num_comments"],
                    "post_4_share": account["post_4"]["num_shares"]
                }
                account_dicts.append(account_dict)
        return pd.DataFrame(account_dicts)


# Custom transformer to calculate mean values
class MeanValueTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_transformed = pd.DataFrame()
        X_transformed["user"] = X["user"]
        X_transformed["label"] = X["label"]
        X_transformed['mean_likes'] = X[['post_1_likes', 'post_2_likes', 'post_3_likes', 'post_4_likes']].astype(
            'float').mean(axis=1)
        X_transformed['mean_comments'] = X[
            ['post_1_comments', 'post_2_comments', 'post_3_comments', 'post_4_comments']].astype('float').mean(axis=1)
        X_transformed['mean_shares'] = X[['post_1_share', 'post_2_share', 'post_3_share', 'post_4_share']].astype(
            'float').mean(axis=1)
        return X_transformed


class convert_to_number_and_drop_non_numeric(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        numeric_columns_float = pd.DataFrame()
        other_data = X[["user", "label"]]
        numeric_columns = X[['post_1_likes', 'post_1_comments', 'post_1_share',
                             'post_2_likes', 'post_2_comments', 'post_2_share', 'post_3_likes',
                             'post_3_comments', 'post_3_share', 'post_4_likes', 'post_4_comments',
                             'post_4_share']]
        for col in numeric_columns:
            numeric_columns_float[col] = X[col].apply(pd.to_numeric, errors='coerce', downcast="float")

        all_data = pd.concat([other_data, numeric_columns_float], axis=1)

        return all_data


pipeline_processor = Pipeline([
    ('dict_to_df', DictToDataFrameTransformer()),
    ('convert to numb and drop_na', convert_to_number_and_drop_non_numeric()),
    ('mean_value', MeanValueTransformer()),
])

