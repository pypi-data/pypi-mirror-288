import numpy as np
import pandas as pd
from IPython.display import display
from sklearn.preprocessing import LabelEncoder
# data reading
def read_file(pathOfFile,typeOfFile):
    '''
    It's a function in my own package to read file using pandas package 
    data maybe csv, Fixed-Width Text File (fwf), JSON, HTML , XML , clipboard,
    Excel, HDF5 (hdf), feather, Parquet, orc , stata and SQL
    '''
    if typeOfFile == "csv":
        data = pd.read_csv(pathOfFile)
    elif typeOfFile == "fwf":
        data = pd.read_fwf(pathOfFile)
    elif typeOfFile == "JSON":
        data = pd.read_json(pathOfFile)
    elif typeOfFile == "HTML":
        data = pd.read_html(pathOfFile)
    elif typeOfFile == "XML":
        data = pd.read_xml(pathOfFile)
    elif typeOfFile == "clipboard":
        data = pd.read_clipboard(pathOfFile)
    elif typeOfFile == "Excel":
        data = pd.read_excel(pathOfFile)
    elif typeOfFile == "HDF5":
        data = pd.read_hdf(pathOfFile)
    elif typeOfFile == "feather":
        data = pd.read_feather(pathOfFile)
    elif typeOfFile == "Parquet":
        data = pd.read_parquet(pathOfFile)
    elif typeOfFile == "orc":
        data = pd.read_orc(pathOfFile)
    elif typeOfFile == "stata":
        data = pd.read_stata(pathOfFile)
    elif typeOfFile == "SQL":
        data = pd.read_sql(pathOfFile)
    else:
        data = pd.DataFrame([])
        help (read_file)
    return data
#data summary
def Data_Summary(data : pd.DataFrame):
    '''
    It's a function in my own package print data summary (categorical & numerical)
    '''
    display(data.describe(include = ['object','bool'])) , display(data.describe())
#Handling missing values
def handle_missing_values(data : pd.DataFrame,remove=False, **methods):
    '''
    It's a function in my own package to handle missing values >>In Place<<
    remove nulls --> remove = True
    data_method --> specific --> if you need specific word or number
    data_method --> org -- if you need a method from next
    replace nulls with mean,median,ffill,bfill
    ffill --> method is set as ffill and hence the value in the same column replaces the null value from up to down
    bfill --> method is set as ffill and hence the value in the same column replaces the null value from down to up
    ex:data_method='org', method = 'ffill'
    '''
    if remove:
        data.dropna(inplace=True)
        return
    if methods['data_method'] == 'specific':
        data.fillna( methods['value'], inplace = True)
    elif methods['data_method'] == 'org':
        data.fillna( method=methods['method'] , inplace = True)
def encoding (data: pd.DataFrame , method, cols : list):
    '''
    It's a function in my own package to encode categorical columns 
    method is LabelEncoder or oneHotEncoder
    cols is the list of columns
    '''
    if method == 'LabelEncoder':
        labelencoder = LabelEncoder()
        data[cols] = data[cols].apply(labelencoder.fit_transform)
        return data
    elif method == 'oneHotEncoder':
        if len(cols)>1:
            new_data = pd.get_dummies(data, columns=cols, prefix=cols)
            return new_data
        new_data = pd.get_dummies(data, columns=cols, prefix=cols)
        return new_data
    else :
        raise ValueError("Enter oneHotEncoder or LabelEncoder")
