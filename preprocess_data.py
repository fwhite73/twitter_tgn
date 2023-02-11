####################################################################################################################
# sostituire al file utils/preprocess_data.py nel progetto github https://github.com/twitter-research/tgn
####################################################################################################################

import json
import numpy as np
import pandas as pd
from pathlib import Path
import argparse


def preprocess(data_name, data_percentage):
  u_list, i_list, ts_list, label_list = [], [], [], []
  feat_l = []
  idx_list = []

  with open(data_name) as f:
    s = next(f)
    for idx, line in enumerate(f):
      e = line.strip().split(',')
      u = int(e[0])
      i = int(e[1])

      ts = float(e[2])
      label = float(e[3])  # int(e[3])

      feat = np.array([float(x) for x in e[4:]])

      u_list.append(u)
      i_list.append(i)
      ts_list.append(ts)
      label_list.append(label)
      idx_list.append(idx)

      feat_l.append(feat)
  df= pd.DataFrame({'u': u_list,
                       'i': i_list,
                       'ts': ts_list,
                       'label': label_list,
                       'idx': idx_list})
  index = int(df.shape[0]*float(data_percentage))
  return df.iloc[:index], np.array(feat_l)

def preprocessNode(max_idx, data_name):
  node_features_dataframe = pd.DataFrame(columns=['user_idx', 'features'])
  feat_n = []
 
  with open(data_name) as f:
    s = next(f)
    for idx, line in enumerate(f):
      e = line.strip().split(',')
      u = e[0]
      feat = np.array([float(x) for x in e[1:]])
      # save node<->features correspondance
      node_features_dataframe.loc[len(node_features_dataframe)] = [u, feat]
  
  for i in range(0, max_idx+1):
      # if node's features are present add them to the list, else add a list of zeros
      if(len(node_features_dataframe[node_features_dataframe['user_idx']==str(i)])>0):
        feat_n.append(node_features_dataframe[node_features_dataframe['user_idx']==str(i)]['features'].values[0])
      else:
        feat_n.append(np.array([0 for _ in range(0, 172)]))
      
  return np.array(feat_n)

def reindex(df, bipartite=True):
  new_df = df.copy()
  if bipartite:
    assert (df.u.max() - df.u.min() + 1 == len(df.u.unique()))
    assert (df.i.max() - df.i.min() + 1 == len(df.i.unique()))

    upper_u = df.u.max() + 1
    new_i = df.i + upper_u

    new_df.i = new_i
    new_df.u += 1
    new_df.i += 1
    new_df.idx += 1
  else:
    new_df.u += 1
    new_df.i += 1
    new_df.idx += 1

  return new_df


def run(data_name, bipartite=True, data_percentage=1):
  Path("data/").mkdir(parents=True, exist_ok=True)
  PATH = './data/{}.csv'.format(data_name)
  NODES_PATH = './data/{}_nodes.csv'.format(data_name)
  OUT_DF = './data/ml_{}.csv'.format(data_name)
  OUT_FEAT = './data/ml_{}.npy'.format(data_name)
  OUT_NODE_FEAT = './data/ml_{}_node.npy'.format(data_name)

  df, feat = preprocess(PATH, data_percentage)
  new_df = reindex(df, bipartite)

  empty = np.zeros(feat.shape[1])[np.newaxis, :]
  feat = np.vstack([empty, feat])

  max_idx = max(new_df.u.max(), new_df.i.max())

  # node features (vectors must have size: 172)
  node_feat = preprocessNode(max_idx, NODES_PATH)
  # comment the row above and uncomment the row below to disable node representation
  #node_feat = np.zeros((max_idx + 1, 172))

  new_df.to_csv(OUT_DF)
  np.save(OUT_FEAT, feat)
  np.save(OUT_NODE_FEAT, node_feat)

parser = argparse.ArgumentParser('Interface for TGN data preprocessing')
parser.add_argument('--data', type=str, help='Dataset name (eg. wikipedia or reddit)',
                    default='wikipedia')
parser.add_argument('--bipartite', action='store_true', help='Whether the graph is bipartite')
parser.add_argument('--dp', help='Data percentage to be used')

args = parser.parse_args()

run(args.data, bipartite=args.bipartite, data_percentage=args.dp)