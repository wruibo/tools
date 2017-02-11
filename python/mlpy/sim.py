#!/usr/bin/env python3
import math

'''
    compute item similarity with collaborative filtering.
    
    distance computing method:
        1.cosine distance
        2.euclidean distance
        3.pearson correlation
        4.tanimoto correlation(generalized jaccard)
    
    method input & output:
        input: @item_users, {item id:{user id:score, user id:score,...}, ...}
        ouput: @item_items, {item id:{item id:similarity, item id:similarity,...}, ...}
        
    @author
        by wangruibo @2013.1.9
'''

class sim:
  
    #build user 2 items from the input of item 2 users
    def build_user2items(self, item_users):
        #user with items relate for return
        user_items = {}  
        #build the user 2 items data structure
        for item_id in item_users.keys():
            for user_id in item_users[item_id].keys():
                if user_id not in user_items:
                    user_items[user_id] = {}
                user_items[user_id][item_id] = item_users[item_id][user_id]
        return user_items
    
    #compute item similarity with cosine distance
    def cosine_distance_cf(self, item_users):
         #similarity of item 2 items for return
        item_items = {}
        
        #build the user2items data structure
        user_items = self.build_user2items(item_users)

         
        #process each item, compute the similarity with other items
        for item_a_id in item_users.keys():
            #add item a to result if not exist
            if item_a_id not in item_items:
                item_items[item_a_id] = {}
                
            #compute length a
            len_a = 0.0
            for score in item_users[item_a_id].values():
                len_a += score*score
            len_a = math.sqrt(len_a)
            
            #process each user who has relation with item a
            for user_id in item_users[item_a_id].keys():
                #process each item b which has the same user with item a, compute similarity of a and b
                for item_b_id in user_items[user_id].keys():
                    #check if the similarity of a and b has computed
                    if item_b_id in item_items[item_a_id]:
                        continue
                    
                    #compute length b
                    len_b = 0.0
                    for score in item_users[item_b_id].values():
                        len_b += score*score
                    len_b = math.sqrt(len_b)
                    
                    #compute a.b
                    dot_product_ab = 0.0
                    for user_a_id in item_users[item_a_id].keys():
                        if user_a_id in item_users[item_b_id]:
                            dot_product_ab += item_users[item_a_id][user_a_id]*item_users[item_b_id][user_a_id]
                    
                    #compute similitary in cosine distance of item a and item b
                    sim = dot_product_ab/(len_a*len_b);
                    
                    #put the similitary to result
                    item_items[item_a_id][item_b_id] = sim
        
        return item_items
    
    #compute item similarity with euclidean distance    
    def euclidean_distance_cf(self, item_users):
         #similarity of item 2 items for return
        item_items = {}
        
        #build the user2items data structure
        user_items = self.build_user2items(item_users)

        #process each item, compute the similarity with other items
        for item_a_id in item_users.keys():
            #add item a to result if not exist
            if item_a_id not in item_items:
                item_items[item_a_id] = {}
                
            #process each user who has relation with item a
            for user_id in item_users[item_a_id].keys():
                #process each item b which has the same user with item a, compute similarity of a and b
                for item_b_id in user_items[user_id].keys():
                    #check if the similarity of a and b has computed
                    if item_b_id in item_items[item_a_id]:
                        continue
                    
                    #compute euclidean distance between a and b
                    ed_ab = 0.0
                    for user_a_id in item_users[item_a_id].keys():
                        if user_a_id in item_users[item_b_id]:
                            ed_ab += pow(item_users[item_a_id][user_a_id]-item_users[item_b_id][user_a_id], 2)
                    
                    #compute similitary in euclidean distance of item a and item b
                    sim = math.sqrt(ed_ab)
                    
                    #put the similitary to result
                    item_items[item_a_id][item_b_id] = sim
        
        return item_items
    
    #compute item similarity with pearson correlation score
    def pearson_correlation_cf(self, item_users):
         #similarity of item 2 items for return
        item_items = {}
        
        #build the user2items data structure
        user_items = self.build_user2items(item_users)

        #process each item, compute the similarity with other items
        for item_a_id in item_users.keys():
            #add item a to result if not exist
            if item_a_id not in item_items:
                item_items[item_a_id] = {}
                
            #process each user who has relation with item a
            for user_id in item_users[item_a_id].keys():
                #process each item b which has the same user with item a, compute similarity of a and b
                for item_b_id in user_items[user_id].keys():
                    #check if the similarity of a and b has computed
                    if item_b_id in item_items[item_a_id]:
                        continue
                    
                    #compute pearson correlation score between a and b
                    same_user_num = 0
                    pc_sum_a = pc_sum_b = pc_sum_a2 = pc_sum_b2 = pc_sum_ab = 0.0
                    for user_a_id in item_users[item_a_id].keys():
                        if user_a_id in item_users[item_b_id]:
                            same_user_num += 1
                            pc_sum_a += item_users[item_a_id][user_a_id]
                            pc_sum_b += item_users[item_b_id][user_a_id]
                            pc_sum_a2 += pow(item_users[item_a_id][user_a_id], 2)
                            pc_sum_b2 += pow(item_users[item_b_id][user_a_id], 2)
                            pc_sum_ab += item_users[item_a_id][user_a_id] * item_users[item_b_id][user_a_id]
                    
                    #compute similitary in correlation score of item a and item b
                    pearson_numerator = same_user_num*pc_sum_ab - pc_sum_a*pc_sum_b
                    pearson_denominator = math.sqrt((same_user_num*pc_sum_a2-pow(pc_sum_a, 2))) * math.sqrt(same_user_num*pc_sum_b2-pow(pc_sum_b,2))
                    sim = pearson_numerator / pearson_denominator
                    
                    #put the similitary to result
                    item_items[item_a_id][item_b_id] = sim
        
        return item_items

    #compute item similarity with tanimoto(generalized jaccard) correlation
    def tanimoto_correlation_cf(self, item_users):
         #similarity of item 2 items for return
        item_items = {}
        
        #build the user2items data structure
        user_items = self.build_user2items(item_users)

        #process each item, compute the similarity with other items
        for item_a_id in item_users.keys():
            #add item a to result if not exist
            if item_a_id not in item_items:
                item_items[item_a_id] = {}
            
            #compute pow 2 of length a
            len_a_pow2 = 0.0
            for score in item_users[item_a_id].values():
                len_a_pow2 += score*score
            
            #process each user who has relation with item a
            for user_id in item_users[item_a_id].keys():
                #process each item b which has the same user with item a, compute similarity of a and b
                for item_b_id in user_items[user_id].keys():
                    #check if the similarity of a and b has computed
                    if item_b_id in item_items[item_a_id]:
                        continue
                    
                    #compute pow 2 oflength b
                    len_b_pow2 = 0.0
                    for score in item_users[item_b_id].values():
                        len_b_pow2 += score*score
                    
                    
                    #compute inner product of a and b
                    inner_product_ab = 0.0
                    for user_a_id in item_users[item_a_id].keys():
                        if user_a_id in item_users[item_b_id]:
                           inner_product_ab += item_users[item_a_id][user_a_id] * item_users[item_b_id][user_a_id]
                    
                    #compute similitary in tanimoto correlation score between of item a and item b
                    tanimoto_sim = inner_product_ab / (len_a_pow2+len_b_pow2-inner_product_ab)
                    
                    #put the similitary to result
                    item_items[item_a_id][item_b_id] = tanimoto
        
        return item_items
