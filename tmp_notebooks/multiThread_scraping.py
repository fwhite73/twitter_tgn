from multiprocessing import Pool
from twitter_users_scraping import scrape

list_ranges = [[61000, 71000], [71000, 81000], [81000, 91000], [101000, 111000]]
#list_ranges = [[111000, 121000], [121000, 131000], [131000, 141000], [141000, 151000]]
#list_ranges = [[151000, 161000], [171000, 181000], [181000, 191000], [191000, 201000]]
#list_ranges = [[201000, 211000], [211000, 221000], [221000, 231000], [231000, 241000]]
#list_ranges = [[241000, 251000], [251000, 262051]]
#list_ranges = [[23000, 25000], [25000, 27000], [27000, 29000], [29000, 31000]]

pool = Pool(processes=len(list_ranges))
  
# map the function to the list and pass 
# function and list_ranges as arguments
pool.map(scrape, list_ranges)