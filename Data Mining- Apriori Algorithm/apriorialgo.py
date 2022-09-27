import math
from time import process_time

# function to calculate the support value for item and itemsets
def itemsupport(total_transaction = 0, matching_transaction = 0):
    return ((matching_transaction/total_transaction)*100)

# function to calculate the confidence value for rules
def itemconfidence(matching_itemset = 0, matching_left_item = 0):
    return((matching_itemset/matching_left_item)*100)

def apriori_algorithm():
    t1_start = process_time()
    #dictionary containing transaction from the user created file
    original_transactions = {} 
    # list of unique items from all transactions
    unique_items = [] 

    file_path= input("\n Enter transaction filename including extension of the file : ")
    transaction_file=open(file_path,"r")

    k=0
    for items in transaction_file:
        original_transactions[k] = [temp.strip() for temp in (items.split(','))]
        
        for element in original_transactions[k]:
            if(element not in unique_items):
                unique_items.append(element)
        k+=1

    print("\n****************Transactions****************\n")
    temp = 0

    for items in original_transactions:
        print("\nTransaction " + str(temp) + ": " + str(original_transactions[items]) + " ")
        temp+=1

    min_support = int(input("\nMinimum support value: "))
    min_confidence = int(input("\nMinimum confidence value: "))

    #list of combinations of items that satify minimum support
    candidate_list=[]
    temp_queue1=[]

    for item in unique_items:
        # adding item in temp queue as a list of lists
        temp_queue1.append([item])

    exit_flag =0

    # This loop will find candidate sets satisfying minimum support for the association rule
    while(len(temp_queue1)>=2):
        temp_queue2=[]
        #resetting exit flag inside the loop
        exit_flag=0 

        for item in temp_queue1:
            # variable to keep track of number of item sets
            count=0
            for element in original_transactions:
                if(all(data in original_transactions[element] for data in item)):
                    count = count + 1

            #ignore if the support for the itemset is less than minimum support given by user
            if(itemsupport(k,count))<min_support:
                continue 

            # if support of itemset is more than user given support then append the item in candidate queue and temp2 queue
            candidate_list.append(item)
            temp_queue2.append(item)

        #checking for case where item set is 1 
        if(len(temp_queue2))<2:
            temp_queue1=temp_queue2
            continue
        else:
            temp_queue1=[]

        # Generating possible combinations of itemsets 
        for i in range(0,len(temp_queue2)-1):
            for j in range(i+1,len(temp_queue2)):
                queue1=temp_queue2[i].copy()
                queue1.extend(temp_queue2[j])
                queue1=list(dict.fromkeys(queue1))

                # checking fro redundancy
                duplicate_flag1=0
                for index in range(0,len(temp_queue1)):
                    if(len(queue1)==len(temp_queue1[index]) and all (data in temp_queue1[index] for data in queue1)):
                        duplicate_flag1=1 # set duplicate flag to one if one combination is repeated in queue1
                        break

                if duplicate_flag1 == 0:
                    temp_queue1.append(queue1)
                    exit_flag=1 # setting exit flag to come out of the loop if no duplicate found

    if exit_flag ==1: # if no duplicates found then enter the below loop
        for item in temp_queue1:
            count=0 # calculating the number of item sets in order to find out the support of the set
            for element in original_transactions:
                if(all(data in original_transactions[element] for data in item)):
                    count += 1

            if(itemsupport(k,count))<min_support:
                break

            # If Itemset matches minimum support criteria update the candidate queue
            candidate_list.append(item)

    # Printing candidate for association rule.
    print("\nCandidate list: \n")
    for data in candidate_list:
        print(data)

    # maintiaining a dictionary for the resulting association rules from frequent itemsets
    # key will be left hand side of rule and value will be right hand side of rule.
    rules={} 

    for candidate in candidate_list:
        # since we can not take itemset with length less than 2 for creating association rules 
        if(len(candidate))<2:
            continue 

        # Each iteration  of 'i' specifies the items on left hand side.
        for i in range(1,len(candidate)):
            # to store the left hand side of the association rule
            rule_LHS= []
            # to store the right hand side of the association rule 
            rule_RHS= []
            # to store the current index of the item of LHS of the rule
            current_item_index= [] 

            for j in range(i):
                current_item_index.append(j)

            for j in current_item_index:
                rule_LHS.append(candidate[j])

            for j in range(len(candidate)):
                if j not in current_item_index:
                    rule_RHS.append(candidate[j])

            #count of total number of transaction itemsets in all
            count_all=0
            # count of number of appeareance of left hand side item set in transaction
            count_left=0

            for element in original_transactions:
                if(all(data in original_transactions[element] for data in rule_LHS)):
                    count_left+=1
                    if(all(data in original_transactions[element] for data in rule_RHS)):
                        count_all+=1

            #Calculating confidence of the rule
            if(itemconfidence(itemsupport(k,count_all), itemsupport(k,count_left))) >= min_confidence:
                # Storing association rules if minimum confidence criteria is achieved.
                key = ""
                value = ""
                rule_confidence = round(itemconfidence(itemsupport(k,count_all), itemsupport(k,count_left)),2)

                for j in rule_LHS:
                    key = key + " " + j
                        
                key = key.strip()

                for j in rule_RHS:
                    value = value + " " + j

                value = value.strip()

                if key in rules.keys():
                    rules[key].append([value,rule_confidence])

                else: 
                    temp=[]
                    temp.append([value,rule_confidence])
                    rules[key]=temp
            
            # last index position from list of items currently referred to
            last_index_position=len(current_item_index)-1 

            # Calculating possible combinations.
            item_combinations= math.factorial(len(candidate))/math.factorial(i)

            while(item_combinations>0):
                # Resetting LHS and RHS variables
                rule_LHS=[]
                rule_RHS=[]

                for j in range(i-1,-1,-1):
                    if(current_item_index[j] < (len(candidate))-(last_index_position-j)-1):
                        temp_position= current_item_index[j] + 1

                        for m in range(j,i):
                            current_item_index[m] = temp_position
                            temp_position = temp_position + 1
                        break
                    else:
                        continue
                
                # Storing left hand side items of association rules
                for j in current_item_index:
                    rule_LHS.append(candidate[j])

                # Storing right hand side items of association rules
                for j in range(len(candidate)):
                    if j not in current_item_index:
                        rule_RHS.append(candidate[j])
                
                # Checking confidence constraint.
                # calculating number of transaction items set in whole
                count_all = 0
                # calculating number of transaction items set on left
                count_left = 0 
                for element in original_transactions:
                    if(all(data in original_transactions[element] for data in rule_LHS)):
                        count_left += 1
                        if(all(data in original_transactions[element] for data in rule_RHS)):
                            count_all += 1
                
                if (itemconfidence(itemsupport(k, count_all),itemsupport(k, count_left)) < min_confidence):
                    item_combinations = item_combinations - 1
                    continue
                
                # Storing association rules if minimum confidence criteria is achieved.
                key = ""
                value = ""
                for j in rule_LHS:
                    key = key + " " + j

                key = key.strip()

                for j in rule_RHS:
                    value = value + " " + j

                value = value.strip()

                rule_confidence = round(itemconfidence(itemsupport(k,count_all), itemsupport(k,count_left)),2)

                if key in rules.keys():
                    if (value not in [item[0] for item in rules[key]]):
                        rules[key].append([value,rule_confidence])
                    
                else:
                    temp = []
                    temp.append([value,rule_confidence])
                    rules[key] = temp

                item_combinations = item_combinations - 1
            
    print("\nAll the possible association rules along with their confidence (%) are as follows: \n")
    for key in rules:
        for value in rules[key]:
            print("{" + key + "} -> {" + value[0] + "} " + str(value[1]))

    t1_stop = process_time()
    print("\n Elapsed time during the whole program in seconds:",t1_stop-t1_start,"\n")

apriori_algorithm()