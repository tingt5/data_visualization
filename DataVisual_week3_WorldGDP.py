"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    match_dict = {}
    not_found_in_gdp = set()
    for key, value in plot_countries.items():
        if value in gdp_countries:
            match_dict[key] = value
        else:
            not_found_in_gdp.add(key)

    return match_dict, not_found_in_gdp

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    #read GDP csv file to get gdp data; need to calculate the log (base 10) of GDP value later
    gdp_table = read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'], gdpinfo['separator'], gdpinfo['quote'])

    country_gdp_yr = {}
    not_found_in_gdpfile = set()
    found_no_yr_value = set()
    for key, value in plot_countries.items():
        if value in gdp_table:
            if gdp_table[value][year] != "":
                gdp_yr = gdp_table[value][year]
                log_gdp = math.log10(float(gdp_yr))
                country_gdp_yr[key] = log_gdp
            else:
                found_no_yr_value.add(key)
        else:
            not_found_in_gdpfile.add(key)

    return country_gdp_yr, not_found_in_gdpfile, found_no_yr_value
