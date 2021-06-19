# Description
This project aims to provide a curated version of the [PULSE](https://www.census.gov/data/experimental-data-products/household-pulse-survey.html) dataset
from the US Census Bureau. Currently, the survey is provided by round as a zip file containing 
raw data, weights (for bootstrapped estimates of response uncertainty), and a data dictionary.
Furthermore, survey questions have changed since its inception back in April 2020. Taken together,
these present obstacles to analysis, which this project aims to ameliorate. Development is ongoing
and ultimately will provide, at minimum, tools to scrape and create a tidy dataset ready for exploration
and analysis - the data will not be hosted on GitHub due to its size.

# Contents
* `data/`
    * `processed/`
    * `raw/`
    * `weights/`
    * `zipped/`
    
* `docs/`
    * `raw/`
    
* `src/`   
    * `data_scraper.py`
        * Collects data
            * Downloads to `../data/zipped`, moves weights to `../data/weights`, 
            dictionaries to `../docs/raw`, raw data to `../data/raw`
              
    * `app.py`
      * An interactive front-end for the data built on `streamlit` and `plotly` to facilitate
        exploration
        
* `README.md`
* `requirements.txt`
* `.gitignore`
    
