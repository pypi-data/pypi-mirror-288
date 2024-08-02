# databuff

Python Lib for data analysis

## Features

| Feature                 | Status            |
| ----------------------- | ----------------- |
| Verify Dataframe        | &#9745; Completed |
| Verify Column           | &#9745; Completed |
| Max value of a column   | &#9745; Completed |
| Min value of a column   | &#9745; Completed |
| First value of a column | &#9745; Completed |
| Last value of a column  | &#9745; Completed |
| Mean value of a column  | &#9745; Completed |
| Delta Time Computation  | &#9745; Completed |
| Timeseries Integration  | &#9745; Completed |
| Cumulative Sum          | &#9745; Completed |
| Integration Multiplier  | &#9745; Completed |
| Manipulate a Column     | &#9745; Completed |
| Standard Deviation of a column  | &#9744; Completed     |
| 'X' Quantile of a column  | &#9744; Completed     |
| Conditional Filtering   | &#9744; Completed     |
| Timeseries Subsampling  | &#9744; Completed     |


## Folder Structure

**ion_analytics/ion_analytics:** Contains Functions and definition

**ion_analytics/tests:** Contains Unit Test Case and dummy timeseries dataset

## Installation

#### Install Python Dependency Manager

Refer : https://python-poetry.org/docs/


#### Install Local Dependencies
This should create a local env variable and install all the libs
```
cd ion-analytics
poetry install
```

#### Build Package
This should create *tar or *whl for us to invoke in any application under ```dist``` directory 
```
poetry build
```

#### Test Package
Local Test of the package
```
poetry run pytest
```

## Usage

#### Using the poetry env to use for Jupyter
Get the env variable name
```
poetry env info
```
- Use this variable for your py-kernel when you launch your jupyter instance in vscode. 
- If you cant find this, then:
- Ctrl/Cmd + P
- Select Python Interpreter
- Enter Interpreter Path
- Use the path as per ```poetry env info``` to add your ``venv`` to vs code

...

## Contributing

...