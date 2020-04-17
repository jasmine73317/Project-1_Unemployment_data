import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def  visualization():
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"content-type": "application/json"}

    target_series = ["LNS14000000", "LNS14000001", "LNS14000002", "LNS14000003", "LNS14000006", "LNS14032183", "LNS14000009",
         "LNS14027659", "LNS14027660", "LNS14027689", "LNS14027662", "LNS14024887", "LNS14000089", "LNS14000091",
                "LNS14000093", "LNS14024230"]

    start_year = "2006"
    end_year = "2018"

    parameters = json.dumps({"seriesid": target_series,
             "startyear": start_year,
             "endyear": end_year,
             "registrationkey": bls_api_key})

    p = requests.post(url, data=parameters, headers=headers)

    json_data = json.loads(p.text)
    years = []

    months = []



    for data_point in np.arange(len(json_data["Results"]["series"][0]["data"])):

        years.append(json_data["Results"]["series"][0]["data"][data_point]["year"])

        months.append(json_data["Results"]["series"][0]["data"][data_point]["periodName"])
        
    unemployment_df = pd.DataFrame({"Year": years,
                                "Month": months,
                                "LNS14000000" : "",
                                "LNS14000001" : "",
                                "LNS14000002" : "",
                                "LNS14000003" : "",
                                "LNS14000006" : "",
                                "LNS14032183" : "",
                                "LNS14000009" : "",
                                "LNS14027659" : "",
                                "LNS14027660" : "",
                                "LNS14027689" : "",
                                "LNS14027662" : "",
                                "LNS14024887" : "",
                                "LNS14000089" : "",
                                "LNS14000091" : "",
                                "LNS14000093" : "",
                                "LNS14024230" : ""})
    unemployment_df
    
    # Gender Statistics
    #Create gender df
    gender_unemployment_df= unemployment_df[["Year", "Month","Unemployment Rate for Men 16yo and over",
                                 "Unemployment Rate for Women 16yo and over",
                                 "Unemployment Rate for 16yo and over"
                               ]]
#Variables to convert into int/float

    years= gender_unemployment_df["Year"].astype(int)
    male_data= gender_unemployment_df["Unemployment Rate for Men 16yo and over"].astype(float)
    female_data= gender_unemployment_df["Unemployment Rate for Women 16yo and over"].astype(float)
    full_data= gender_unemployment_df["Unemployment Rate for 16yo and over"].astype(float)

#New clean DF
    gender_unemployment_df= pd.DataFrame({"Year": years, "Month": unemployment_df["Month"],
                                      "Male Unemployment Rate": male_data,
                                      "Female Unemployment Rate": female_data,
                                 "Unemployment Rate (Both Sexes)": full_data})

    gender_unemployment_df.sort_values(by= "Year", ascending= True).reset_index(drop=True)
    annual_data= gender_unemployment_df.groupby(["Year"])
#annual_data["Unemployment Rate for Men 16yo and over"].head()
    annual_data= annual_data.mean().reset_index()
    
    tidy_annual_df= pd.melt(annual_data, id_vars=['Year'], value_vars=['Male Unemployment Rate',
                                                   "Female Unemployment Rate", "Unemployment Rate (Both Sexes)"],

        var_name='Group', value_name='Unemployment Rate')
    #Bar plot unemployment 06 thru 18 for different genders
    ax = sns.catplot(kind="bar",x="Year", y="Unemployment Rate", hue= "Group",
                 data=tidy_annual_df,palette= "tab10", height= 5,aspect= 2)
    plt.title("U.S. Unemployment Rate (2006 to 2018)")
    plt.ylabel("Unemployment Level (%)")
#plt.grid()
    plt.xlim(-.75,len("Year")+8.75)
    
    #multiplot for unemployment 06'thru 18' for different genders(subplots?)
    plt.figure(figsize=(12,8))
    sns.set(font_scale=1.5)

    with sns.axes_style("whitegrid",{"figure.facecolor":"white"}):

        sns.lineplot(x= "Year", y= "Unemployment Rate", hue="Group", data=tidy_annual_df,
             palette="tab10", linewidth=2.5)

    plt.ylabel("Avg Unemployment Rate (%)")
    plt.xlim(2006,2018)
    
    # Race Statistics
    
    #Create race df
    race_unemployment_df= unemployment_df[["Year", "Month","Unemployment Rate for 16yo and over",
                                       "Unemployment Rate for White people 16yo and over",
                                       "Unemployment Rate for African Americans 16yo and over",
                                       "Unemployment Rate for Asian people 16yo and over",
                                       "Unemployment Rate for Hispanic people 16yo and over"]]

#Resort values and dtypes for data


    r_years= race_unemployment_df["Year"].astype(int)
    r_full_data= race_unemployment_df["Unemployment Rate for 16yo and over"].astype(float)
    caucasian_data= race_unemployment_df["Unemployment Rate for White people 16yo and over"].astype(float)
    black_data= race_unemployment_df["Unemployment Rate for African Americans 16yo and over"].astype(float)
    asian_data= race_unemployment_df["Unemployment Rate for Asian people 16yo and over"].astype(float)
    hispanic_data= race_unemployment_df["Unemployment Rate for Hispanic people 16yo and over"].astype(float)

#New clean df
    race_unemployment_df= pd.DataFrame({"Year": r_years,"Unemployment (All)": r_full_data, "Caucasian": caucasian_data,
                                   "Black or African American": black_data,
                                   "Asian": asian_data, "Hispanic": hispanic_data})
#Groupby year to gather mean
    race_unemployment_df
    race_unemployment_df.sort_values("Year", ascending=True).reset_index(drop=True)
    r_annual_data= race_unemployment_df.groupby("Year")

    unemployment_avg= r_annual_data["Unemployment (All)"].mean()
    avgw_data= r_annual_data["Caucasian"].mean()
    avgb_data= r_annual_data["Black or African American"].mean()
    avga_data= r_annual_data["Asian"].mean()
    avgh_data= r_annual_data["Hispanic"].mean()


    avg_race_df= pd.DataFrame({"Unemployment (All)": unemployment_avg, "Caucasian":avgw_data,
                               "Black or African American": avgb_data,
                     "Asian": avga_data, "Hispanic": avgh_data})
    
    avg_race_df.reset_index(inplace=True)
    
    r_tidy_annual_df= pd.melt(avg_race_df, id_vars=["Year"], value_vars=list(avg_race_df.columns)[1:],
                          var_name="Group",value_name="Unemployment Rate")
    
    r_tidy_annual_df["Unemployment Rate"] = r_tidy_annual_df["Unemployment Rate"].map(lambda x: round(x,2) )
    
    ax = sns.catplot(kind="bar",x="Year", y="Unemployment Rate", hue= "Group",
                 data=r_tidy_annual_df,palette= "tab10" ,aspect= 3)
    
    #multiplot for unemployment 06'thru 18' for different genders(subplots?)
    plt.figure(figsize=(12,8))
    sns.set(font_scale=1.5)

    with sns.axes_style("whitegrid",{"figure.facecolor":"white"}):

        sns.lineplot(x= "Year", y= "Unemployment Rate", hue="Group", data=r_tidy_annual_df,
                 palette="tab10", linewidth=2.5)

    plt.ylabel("Avg Unemployment Rate (%)")
    plt.xlim(2006,2018)