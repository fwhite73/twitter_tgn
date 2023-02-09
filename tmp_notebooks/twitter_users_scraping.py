
import twint
import time
import pandas as pd
import os.path

def scrape(range_idxs):
    print(range_idxs)
    #read df with author_ids
    df_raw = pd.read_json('df_qatar260k_nonormalize_withauthorid.json')

    #df with author_id to username correspondance
    df_users = pd.read_json("df_authors_username_qatar.json")
    df_users = df_users.drop_duplicates()

    #get users' indexes used in the final dataframe
    count = 0
    user_idxs = {}
    for user_id in df_raw['author_id']:
        user_idxs[user_id] = count
        count+=1

    errors = 0
    counter = 0
    start = time.time()

    start_index = int(range_idxs[0]) #>
    end_index = int(range_idxs[1]) #<

    df_authorid = df_raw['author_id'].drop_duplicates()

    for author_id in df_authorid[df_authorid.index>start_index][:end_index-start_index]:
        try:
            if os.path.exists("tweets/tweets-"+str(user_idxs[author_id])+".json"):
                counter+=1
                continue
            username = df_users[df_users['user_id']==author_id].drop_duplicates()['username'].values[0]
            c = twint.Config()
            c.Username = username
            c.Limit = 100
            c.Output = "tweets/tweets-"+str(user_idxs[author_id])+".json"
            c.Store_json = True
            twint.run.Search(c)
            counter+=1
            print(username + "saved")
        except Exception as e:
            print(author_id)
            print(e)
            errors +=1

    print("Time elapsed: "+ str(time.time() - start))
    print("Saved:" + str(counter))
    print("Errors:" + str(errors))

def scrapeByIds(list_idxs):
    errors = 0
    counter = 0
    start = time.time()

    #read df with author_ids
    df_raw = pd.read_json('df_qatar260k_nonormalize_withauthorid.json')

    #df with author_id to username correspondance
    df_users = pd.read_json("df_authors_username_qatar.json")
    df_users = df_users.drop_duplicates()

    #get users' indexes used in the final dataframe
    count = 0
    user_idxs = {}
    for user_id in df_raw['author_id']:
        user_idxs[user_id] = count
        count+=1

    errors = 0
    counter = 0
    start = time.time()

    # list out keys and values separately
    key_list = list(user_idxs.keys())
    val_list = list(user_idxs.values())
    
    for author_idx in list_idxs:
        try:
            # print key with val 100
            position = val_list.index(author_idx)
            author_id = key_list[position]
            print(author_id)
            username = df_users[df_users['user_id']==author_id].drop_duplicates()['username'].values[0]
            c = twint.Config()
            c.Username = username
            c.Limit = 100
            c.Output = "tweets/tweets-"+str(author_idx)+".json"
            c.Store_json = True
            twint.run.Search(c)
            counter+=1
            print(username + "saved")
        except Exception as e:
            print(author_idx)
            print(e)
            errors +=1

    print("Time elapsed: "+ str(time.time() - start))
    print("Saved:" + str(counter))
    print("Errors:" + str(errors))

scrapeByIds([261760, 254977, 240899, 206725, 261639, 240904, 259336, 184200, 261514, 261644, 261645, 262027, 241171, 261779, 60950, 261662, 261155, 261668, 261795, 261544, 259628, 261804, 143276, 261552, 261688, 260538, 261562, 260798, 260542, 261698, 193218, 261572, 260677, 260808, 261576, 261582, 181327, 199759, 259414, 261723, 258395, 238173, 260575, 93665, 251110, 256743, 252775, 259046, 258794, 246763, 261743, 198386, 262002, 262007, 261624, 261626, 261628, 259838])