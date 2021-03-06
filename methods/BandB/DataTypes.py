'''
MIT License

Copyright (c) [2018] [Ji Zhang]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.
'''

import random
import pandas as pd
import numpy as np


def infer_feature_type(feature):
    """Infer data types for the given feature using simple logic.
    Possible data types to infer: boolean, category, date, float, integer
    Feature that is not either a boolean, a date, a float or an integer,
    is classified as an object.
    Parameters
    ----------
    feature : array-like
        A feature/attribute vector.
    Returns
    -------
    data_type : string
        The data type of the given feature/attribute.
    """

    types = ["datetime64[ns]", "float64", "int64", "object"]
    weights = [0, 0, 0, 0]  # Weights corresponding to the data types
    feature_len = len(feature)

    indices_number = int(0.1 * feature_len)  # Number of different values to check in a feature
    indices = random.sample(range(0, feature_len), min(indices_number, feature_len))  # Array of random indices

    # If the feature only contains two different unique values, then infer it as boolean
    if len(pd.unique(feature)) == 2:
        try:
            int(feature[0])
            data_type = "bool"
        except:
            data_type = "category"
    elif len(pd.unique(feature)) < 10:
        data_type = "category"
    else:
        for i in indices:
            try:
                if (len(feature[i]) <= 10
                    and (((feature[i][2:3] == '-' or feature[i][2:3] == '/')
                          and (feature[i][5:6] == '-' or feature[i][5:6] == '/'))
                         or ((feature[i][4:5] == '-' or feature[i][4:5] == '/')
                             and (feature[i][7:8] == '-' or feature[i][7:8] == '/')))):
                    weights[0] += 1  # Date
                else:
                    weights[3] += 1  # Object
            except (TypeError, ValueError, IndexError):
                try:
                    int(feature[i])  # numeric
                    if ('.' in str(feature[i])):
                        if isinstance(feature[i], np.float64):
                            if feature[i].is_integer():
                                weights[2] += 1  # Integer
                            else:
                                weights[1] += 1  # Float
                        else:
                            weights[1] += 1  # Float
                    else:
                        weights[2] += 1  # Integer
                except (TypeError, ValueError, IndexError):
                    weights[3] += 1  # Object
        # For debugging
        # print ("Date: {}, Float64: {}, Int64: {},
        # String: {}".format(weights[0],weights[1],weights[2],weights[3]))
        data_type = types[weights.index(max(weights))]

    return data_type


def discover_type_heuristic(df):
    """Infer data types for each feature using simple logic
    Parameters
    ----------
    data : dataframe

    Returns
    -------
    result : list
        List of data types.
    """

    result = []
    for column in df.columns:
        df_ = df[column]
        df_.dropna(inplace=True)
        df_.reset_index(drop=True, inplace=True)
        type_inferred = infer_feature_type(df_)
        result.append(type_inferred)
    return result
