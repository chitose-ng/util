import numpy as np
import pandas as pd

import xlrd
import os
import re
import sqlalchemy
import json
import pprint
from tqdm import tqdm

# Reference from tvi

class DataExtrator:
  @classmethod
  def from_json(cls, config_path='~/.login/info.json'):
    
    with open(os.path.expanduser(config_path), 'r') as f:
      db_info = json.load(f).get('db')
      
    return cls(db_info['user'], db_info['password'])
  
  def __init__(self, user, password):
    
    config={'host': 'localhost',
            'user': user,
            'password': password,
            'port': '5439',
            'database': 'prod'}
    
    db_conf = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(**config)
    self.con = sqlalchemy.create_engine(db_conf, connect_args={'connect_timeout': 100}).connect()
    
  def _read_query(self, query_path):
    
    with open(query_path, 'r') as f:
      query = f.read()
      
    return query
  
  def _replace_parameters(self, query, params_to_replace):
    
    _query = query
    for k, v in params_to_replace.items():
      _query = _query.replace(k, v)
      
    return re.sub('%', '%%', _query)
  
  def _get_convered_query(self, query_path, params_to_replace):
    
    query = self._read_query(query_path)
    query = self._replace_parameters(query, params_to_replace)
    
    return query
  
  def _extract(self, query_path, params_to_replace={}):
      
    query = self._get_convered_query(query_path, params_to_replace)

    df = pd.read_sql(query, con=self.con, parse_dates=True)
    return df

  @staticmethod
  def save(df, file_path, index=False):
    if file_path.split('.')[-1] == 'csv':
      df.to_csv(file_path, encoding='utf-8', index=index)
    elif file_path.split('.')[-1] in ['pq', 'parquet']:
      df.to_parquet(file_path, index=index)
    else:
      raise NotImplementedError('Only csv or parquet file suppored')
      
    print('Data file saved to {}'.format(file_path))
    return 
  
  @staticmethod
  def load(file_path):
    if file_path.split('.')[-1] == 'csv':
      df = pd.read_csv(file_path, encoding='utf-8', parse_dates=True)
    elif file_path.split('.')[-1] in ['pq', 'parquet']:
      df = pd.read_parquet(file_path)
    else:
      raise NotImplementedError('Only support csv or parquet file')
    return df

  @staticmethod
  def params_df_to_list(df, params_base=False, param_identifier=':'):
    # パラメータにするため全てシングルコーテーション付きの文字列にする
    df = df.apply(lambda x: "'" + x.astype(str) + "'")
    # 列名をパラメータ化
    df = df.add_prefix(param_identifier)

    ls_params = list()
    for i in range(len(df)):
        param = df.iloc[i].to_dict()
        ls_params.append(param)

    # base_paramが存在する場合はパラメータに追加
    if params_base != False:
        [x.update(params_base) for x in ls_params]
    return ls_params
    
  @staticmethod
  def fetch_param_sql(path, params):
    res = []
    for param in tqdm(params):
        extracted_df = self._extract(path, param)

        # クエリ結果が空のparamを表示
        if extracted_df.empty:
            pprint.pprint(param)

        res.append(extracted_df)

    return res