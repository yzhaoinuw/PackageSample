## Overview
This is a sample repo to show the structure my MFJ repo (renamed here as "PackageSample") and how to set up the package so that a user can install the package to their Python libraries. There are two concepts. The first is the repo, you can use git clone to download this repo to your local directory. The second is the actual Python package that will be installed to your Python libraries. Since I did not publish the MFJ package on PyPI, which is a store where you can download Python package from, you cannot pip install the MFJ package right away. You need to first clone the repo from GitHub to your computer, then install the package locally. The steps are:

1. Open terminal or command line
2. Inside terminal, clone the repo from GitHub to directory of your choice, for example, /Desktop. This can be done by typing 
```
git clone 
```









1. Download this repo to your working directory. 
2. Create/Open a virtual environment.
3. cd to this repo.
4. In terminal, type 
```
pip install .
```
This will install the package into PYTHONPATH, while also installing all the required packages.

## Example Usage

### Task 1
Let's parse a name using the name_parser module. A name can be entered in any of the following five formats:
1. Last, First Middle, Suffix
2. Last First Middle Sufix
3. Last Suffix, First Middle
4. Last, First Middle Suffix
5. First Middle Last Suffix

The parsing results will be presented in a dictionary, where the keys are the name parts and the values are tuples of corresponding names followed by a confidence score. Note during parsing, the names are lower-cased, and as such, the results are presented in lower case.

```python
from MFJ.name_parser import NameParser

# Chose the model to load, or you can leave the model name blank to use the default model,
# which is trained on over two million person's names and over four hundred thousand business names.
 
#model_name = 'name_parser_elmo_noncrf'
#parser = NameParser(model_name)
parser = NameParser()

#name = "Donald Enrico De la Rosa"
#name = "Mary-Ann Robinson"
#name = "capital offense"
name = "Alexis Franco Charles Van der Whorf II"

print (parser.parse_name(name))

# output
# {'FIRST': ['alexis', 0.9877199530601501], 'MIDDLE': ['franco charles', 0.4598486125469208], 'LAST': ['van der whorf', 0.7886182069778442], 'SUFFIX': ['ii', 0.9922061562538147]}
```

### Task 2
Let's try to query an address against a homeless shelter directory to determine if the address belongs to a shelter. 

```python
from MFJ.shelter_detection import query_address

db = query_address.ConnectDB()

# You can either enter the address as a string,
address = '1000 N 19th St, St.Louis, MO 63016'

# or enter the address as a dictionary that include four fileds: 'StateName', 'ZipCode', 'PlaceName',
# and 'StreetAddress'. The name of the four fields must match exactly. If any field is not available,
# you can leave it out or enter a empty string as its value.

address = {'StateName':'Missouri', 'ZipCode':'63016',
           'PlaceName':'St.Louis', 'StreetAddress':'1000 N 19th St'}

print (db.is_shelter(address))

# output
# True

```

## Updating a name parser model
If you find the name parser model struggles to parse some group of names, for example, person names from a particular ethnic group, you can update the model on an annotated name dataset of that group. You can also create a business name dataset to imporve the name parser's performance on recognizing business names. Make sure you only put person's name person name data and business name in business data and do NOT mix the two since the annotation methodology is different for the two. There are three steps you need to follow to continue train a name parser model. 

1. Create person's name dataset
First, prepare a csv file of the names you would like the model to learn. The csv file should have only ONE column and should NOT have a header. Each row of the csv file is a person's full name presented in this order: last, first, middle, suffix. Each name part is separated by '&'. So for example, the content of the csv file may look like this:

```
De La Rosa&Maria&Ana&
Howard&ronald&julian&jr
morgan&chase&randal&
barber&luke&cameron&
turner&bob&john&
potter&harry&gary&II
```
You don't need to worry about upper-casing or lower-casing the names. Once you have the name csv file ready, cd to the path of the MFJ repo, then run the following python script from command line:

```shell
export CSV_PATH=/path/to/csv
export DATASET_PATH=/path/to/dataset/folder
python ./experiments/create_dataset.py \
    $CSV_PATH \
    $DATASET_PATH \
    --name_type person_name
``` 
This command will make train.txt, dev.txt, and test.txt from the csv file in the DATASET_PATH folder. 

2. Create business name dataset
To create dataset for new business names, create a csv file that has only one column with no header. Put in each row a business name. For example:

```
apple inc
banana inc
orange co
``` 
then, run in command line 

```shell
export CSV_PATH=/path/to/csv
export DATASET_PATH=/path/to/dataset/folder

python ./experiments/create_dataset.py \
    $CSV_PATH \
    $DATASET_PATH \
    --name_type entity_name
```
You can create person's name dataset right after creating business name dataset or vice versa, using the above command. Make sure to use the same DATA_PATH for both types of names. They will get combined in the dataset. A ratio of at least 100:1 person name to business name ratio is recommended, meaning if you prove a hundred thousand person's names to the dataset, then limit the number of business name under one thousand. 

3. Run continue training
Once you have the dataset created, the nest step is to continue training the name parser on the dataset. In command line, 

```shell
export LOAD_MODEL_PATH=/path/to/current/model
export DATASET_PATH=/path/to/dataset
export SAVE_MODEL_PATH=/path/to/new/model

python experiments/continue_train_model.py $LOAD_MODEL_PATH \
    DATASET_PATH \
    --save_model_path /home/yue/python_projects/MFJ/model/name_parser_elmo_noncrf2/
``` 
The *SAVE_MODEL_PATH* argument is optional. But it is recommended to provide a *SAVE_MODEL_PATH* that is different from *LOAD_MODEL_PATH*. This way, your new model will be save separately. Otherwise, the new model will overwrite the previous model. If you want to use your new model in the name-parser module, you need to cd to the repo in command line and reinstall this package. One way to do this is

```shell
pip uninstall MFJ 
pip install .
```

## Update the shelter address data
The current database is built from the homeless shelter address listed on this [online directory](https://www.homelessshelterdirectory.org/). The directory is crowdsourced and may be updated from time to time. To keep the database up to date, you can re-scrape the directory and build an updated database. To do this, in command line, cd to the MFJ repo and then run the following python script

```shell
python ./experiments/update_db.py
``` 
All the actions will be taken care of in sequence: first the old data will be bundled; then the directory will be scraped; next, csv files are created from the scraped data; last, a new database will be created from the csv files. The whole update process may take up to 5 hours, depending on your internet connection, number of available cores on your cpu. If you want to use the updated database, you need to reinstall this package.

## Run test files
Some python scripts have been prepared to run tests for Task 1 and Task 2. These python scripts are located in tests/ directory. "test_shelter_detection.py" can be run to test shelter detection on the Wisconsin data (wi_extract_addr.csv). "test_name_parser.py" can be run to test name parsing on in-tyler-names files in the IN data.

