# SpaceX-Launch-Tracker


### Setup the venv before installing the 

> python3 -m venv venv

### Activate the venv

> source venv/bin/activate

### install requirements

> pip install -r ../requirements.txt


### To run the project run bellow command

> python3 -m src.main


### To get the statistics run bellow command

> python -m src.main --stats

### For getting only the successfull launches run like bellow

> python -m src.main --filter-success true

### To run with start date and enddate filter run bellow

> python -m src.main --start-date 2022-01-01 --end-date 2023-12-31

### To print success rates execute bellow command

> python -m src.main --success-rates

### Pass specific rocket id to filter by the rocket id

> python -m src.main --filter-rocket "5e9d0d95eda69973a809d1ec"

### For upcoming launches

> python -m src.main --filter-upcoming

### To export to json

> python -m src.main --export json

### To export to csv

> python -m src.main --export csv



## Run tests

> PYTHONPATH=. pytest tests/

