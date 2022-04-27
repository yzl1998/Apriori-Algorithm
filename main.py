import sys
import pandas as pd
from collections import defaultdict
from itertools import combinations

def main():
    if(len(sys.argv) != 4):
        print("Usage: main.py [DATASET_FILENAME] [MIN_SUP] [MIN_CONF]")
    else:
        file_name = sys.argv[1]
        min_sup = float(sys.argv[2])
        min_conf = float(sys.argv[3])
    
    print(f'Dataset filename:   {file_name}')
    print(f'Minimum support:    {min_sup}')
    print(f'Minimum confidence: {min_conf}')

    """
    ADDR_PCT_CD：       The precinct in which the incident occurred
    OFNS_DESC：         Description of offense corresponding with key code
    PD_DESC：           Description of internal classification corresponding with PD code (more granular than Offense Description)
    CRM_ATPT_CPTD_CD：  Indicator of whether crime was successfully completed or attempted, but failed or was interrupted prematurely
    LAW_CAT_CD：        Level of offense: felony, misdemeanor, violation
    BORO_NM：           The name of the borough in which the incident occurred
    PREM_TYP_DESC：     Specific description of premises; grocery store, residence, street, etc.
    SUSP_AGE_GROUP：    Suspect’s Age Group
    SUSP_RACE：         Suspect’s Race Description
    SUSP_SEX：          Suspect’s Sex Description
    VIC_AGE_GROUP：     Victim’s Age Group
    VIC_RACE：          Victim’s Race Description
    VIC_SEX：           Victim’s Sex Description
    """

    # read selected columns
    # ['ADDR_PCT_CD', 'OFNS_DESC', 'PD_DESC', 'CRM_ATPT_CPTD_CD', 'LAW_CAT_CD', 'BORO_NM', 'PREM_TYP_DESC', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX']
    selected_cols = ['LAW_CAT_CD', 'BORO_NM', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'VIC_AGE_GROUP', 'VIC_RACE']
    df = pd.read_csv(file_name, usecols = selected_cols)
    num_transactions = len(df)

    itemset = set()
    transactions = []

    large_itemsets = []
    large_itemsets_supports = defaultdict(lambda: 0)

    # create itemset and transactions list
    for _, row in df.iterrows():
        transaction = []
        for i in row.keys():
            itemset.add(row[i])
            transaction.append(row[i])
        transactions.append(transaction)
    
    # item_apperences: number of transactions where an item in itemset appears
    item_apperences = defaultdict(lambda: 0)

    L = set()

    # create all large 1-itemsets
    for transaction in transactions:
        for item in itemset:
            if item in transaction:
                item_apperences[item] += 1
        
    for item in itemset:
        if item_apperences[item] / num_transactions >= min_sup:
            L.add(frozenset([item]))
            
            # add to large_itemsets and update its support
            large_itemsets.append(frozenset([item]))
            large_itemsets_supports[frozenset([item])] = item_apperences[item] / num_transactions

    # main step 1: create all large itemsets through iteration until L is empty
    k = 0
    while len(L) != 0:
        C = set()

        # create candidate itemsets
        if k == 0:
            for p, q in combinations(L, 2):       
                items = p | q
                C.add(items)
        else:
            for p, q in combinations(L, 2):       
                intersection = p & q
                if len(intersection) == k:
                    items = p | q
                    C.add(items)
        
        # prune step: delete all itemsets c in C such that some k-1 subset not in L
        pruned_C = C.copy()
        for c in C:
            subsets = combinations(c, k+1)
            for subset in subsets:
                if frozenset(subset) not in L:
                    pruned_C.remove(c)
                    break

        L = set()
        itemset_apperences = defaultdict(lambda: 0)

        # create (k+2)-itemsets by counting (k+2)-itemsets' apperances
        for transaction in transactions:
            for candidate_itemset in pruned_C:
                if candidate_itemset.issubset(transaction):
                    itemset_apperences[candidate_itemset] += 1

        for candidate_itemset in pruned_C:
            if itemset_apperences[candidate_itemset] / num_transactions >= min_sup:
                L.add(candidate_itemset)
                # add to large_itemsets and update its support
                large_itemsets.append(candidate_itemset)
                large_itemsets_supports[candidate_itemset] = itemset_apperences[candidate_itemset] / num_transactions
        k += 1

    sorted_large_itemsets = sorted(large_itemsets_supports.items(), key=lambda x: x[1], reverse=True)

    # main step 2: compute association rules
    association_rules = []
    association_rules_confidences = defaultdict(lambda: 0)

    for large_itemset in large_itemsets:
        num_items = len(large_itemset)
        if num_items > 1:
            rhs_lists = [frozenset([i]) for i in large_itemset]
            for rhs in rhs_lists: 
                lhs = large_itemset - rhs
                conf = large_itemsets_supports[large_itemset]/large_itemsets_supports[lhs]
                if conf >= min_conf:
                    association_rules.append((lhs, rhs))
                    association_rules_confidences[(lhs, rhs)] = conf
    
    sorted_rules_and_confs = sorted(association_rules_confidences.items(), key=lambda x: x[1], reverse=True)

    # output results to output_file
    with open("output.txt", "w") as output_file:
        print(f'Dataset filename:   {file_name}', file=output_file)
        print(f'Minimum support:    {min_sup}', file=output_file)
        print(f'Minimum confidence: {min_conf}', file=output_file)
        print(f'==Frequent itemsets (min_sup={min_sup*100:,.3f}%)', file=output_file)
        for large_itemset, supp in sorted_large_itemsets:
            print(f'{list(large_itemset)}, {supp * 100:,.3f}%', file=output_file)
        print(f'==High-confidence association rules (min_conf={min_conf*100:,.3f}%)', file=output_file)
        for (lhs, rhs), conf in sorted_rules_and_confs:
            print(f'{list(lhs)} => {list(rhs)} (Conf:{conf * 100:,.3f}%, Supp: {large_itemsets_supports[lhs | rhs]* 100:,.3f}%)', file=output_file)
        output_file.close()


if __name__ == '__main__':
    main()