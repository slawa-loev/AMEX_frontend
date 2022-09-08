import pandas as pd
import numpy as np
import shap
import joblib
from sklearn.preprocessing import OrdinalEncoder

# aggregatre data
def get_difference(data, num_features):
    df1 = []
    customer_ids = []
    for customer_id, df in data.groupby(['customer_ID']):
        # Get the differences
        diff_df1 = df[num_features].diff(1).iloc[[-1]].values.astype(np.float32)
        # Append to lists
        df1.append(diff_df1)
        customer_ids.append(customer_id)
    # Concatenate
    df1 = np.concatenate(df1, axis = 0)
    # Transform to dataframe
    df1 = pd.DataFrame(df1, columns = [col + '_diff1' for col in df[num_features].columns])
    # Add customer id
    df1['customer_ID'] = customer_ids
    return df1

def data_agg(df): ## pass uploaded data

    ## get all feature names, except customer_ID and dates
    features = df.drop(['customer_ID', 'S_2'], axis = 1).columns.to_list()

    ## list of categorical features
    cat_vars = ['B_30',
            'B_38',
            'D_114',
            'D_116',
            'D_117',
            'D_120',
            'D_126',
            'D_63',
            'D_64',
            'D_66',
            'D_68']

    ## list of numerical features
    num_features = [feature for feature in features if feature not in cat_vars]

    train_num_agg = df.groupby("customer_ID")[num_features].agg(['mean', 'std', 'min', 'max', 'last']) # give summary statistics for each numerical feature
    train_num_agg.columns = ['_'.join(x) for x in train_num_agg.columns] # join the column name tuples to a single name
    train_num_agg.reset_index(inplace = True) # get the customer_ID in as a column again and reset index

    ## get lag difference data for numerical features
    train_diff = get_difference(df, num_features)

    ## categorical feature aggregation
    train_cat_agg = df.groupby("customer_ID")[cat_vars].agg(['count', 'last', 'nunique']) # give summary statistics for each categrocial feature
    train_cat_agg.columns = ['_'.join(x) for x in train_cat_agg.columns] # join the column name tuples to a single name
    train_cat_agg.reset_index(inplace = True) # get the customer_ID in as a column again and reset index

    ## merge dfs
    df_agg = train_num_agg.merge(train_cat_agg, how = 'inner', on = 'customer_ID').merge(train_diff, how = 'inner', on = 'customer_ID')

    ## ordinal encode cat_features
    cat_features = [f"{cf}_last" for cf in cat_vars]
    encoder = OrdinalEncoder()
    df_agg[cat_features] = encoder.fit_transform(df_agg[cat_features])

    ## add last - mean feature (only numerical features have means)
    num_cols_mean = [col for col in df_agg.columns if 'mean' in col]
    num_cols_last = [col for col in df_agg.columns if 'last' in col and col not in cat_features]

    for col in range(len(num_cols_last)):
        try:
            df_agg[f'{num_cols_last[col]}_mean_diff'] = df_agg[num_cols_last[col]] - df_agg[num_cols_mean[col]]
        except:
            pass

    return df_agg


# make shap plot
def make_shap_plot(customer_data):
    data = pd.read_csv('uploaded csv file')
    X_pred_agg = data_agg(data).drop(columns=['customer_ID'])

    #load the explainer - sent as a separate file, to be loaded in repository
    ex_filename = 'explainer.bz2'
    ex2 = joblib.load(filename=ex_filename)

    shap_values = ex2(X_pred_agg,check_additivity=False)

    return shap.plots.waterfall(shap_values[0])
