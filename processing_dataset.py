import sys
import numpy as np
import pandas as pd

def main():
    if(len(sys.argv) != 2):
        print("Usage: processing_dataset.py dataset_file.csv")
    else:
        file_name = sys.argv[1]
    
    print(f'Dataset Filename: {file_name}')

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

    # Read selected columns
    selected_cols = ['ADDR_PCT_CD', 'OFNS_DESC', 'PD_DESC', 'CRM_ATPT_CPTD_CD', 'LAW_CAT_CD', 'BORO_NM', 'PREM_TYP_DESC', 'SUSP_AGE_GROUP', 'SUSP_RACE', 'SUSP_SEX', 'VIC_AGE_GROUP', 'VIC_RACE', 'VIC_SEX']
    df = pd.read_csv(file_name, nrows=10000, usecols = selected_cols)

    # Replace UNKNOWN fields with empty string
    df.loc[df['VIC_AGE_GROUP'].isin(['UNKNOWN']),'VIC_AGE_GROUP'] = ''
    df.loc[df['VIC_RACE'].isin(['UNKNOWN']),'VIC_RACE'] = ''
    df.loc[df['VIC_SEX'].isin(['UNKNOWN']),'VIC_SEX'] = ''
    df.loc[df['SUSP_AGE_GROUP'].isin(['UNKNOWN']),'SUSP_AGE_GROUP'] = ''
    df.loc[df['SUSP_RACE'].isin(['UNKNOWN']),'SUSP_RACE'] = ''
    df.loc[df['SUSP_SEX'].isin(['UNKNOWN']),'SUSP_SEX'] = ''
    
    # Replace empty string fields with NaN
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    
    print(df)

    # Drop rows containing NaN
    df2 = df.dropna()
    
    # Add tags to victim info columns and suspect info columns
    df2['VIC_AGE_GROUP'] = 'V-'+df2['VIC_AGE_GROUP'].astype(str)
    df2['VIC_RACE'] = 'V-'+df2['VIC_RACE'].astype(str)
    df2['VIC_SEX'] = 'V-'+df2['VIC_SEX'].astype(str)
    df2['SUSP_AGE_GROUP'] = 'S-'+df2['SUSP_AGE_GROUP'].astype(str)
    df2['SUSP_RACE'] = 'S-'+df2['SUSP_RACE'].astype(str)
    df2['SUSP_SEX'] = 'S-'+df2['SUSP_SEX'].astype(str)
    
    print(df2)
    df2.to_csv('csv_file.csv' , index = False)

if __name__ == '__main__':
    main()