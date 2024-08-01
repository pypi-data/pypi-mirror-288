"""Create the usage information string for the CLI."""

import json
import os
from pathlib import Path

from soil_moisture_prediction.pydantic_models import InputParameters

information = """The cli-tool takes the path to a directory containing a JSON file with input parameters. The input files can be put in the same directory as the parameters file or must be given as an absolute path.

## Directory structure
This is an example of this directory structure:

```
soil_moisture_prediction/test_data/
{directory_tree}
```

## Input parameters
The parameters.json file in this example directory contains the following content:

```
$ cat soil_moisture_prediction/test_data/parameters.json
{parameter_content}
```

## Input data
If the keys of "predictors" and "soil_moisture_data" are not a path to a file, the file is assumed to be in the same directory as the parameters.json file. So instead of:

```
{example_file_name_predictor}
```

The predicotrs could be written as:

```
{example_path_predictor}
```

The predictor data looks like this:
```
$ head -n {head_n} soil_moisture_prediction/test_data/predictor_data.csv
{predictor_data}
```

The predictor can have a head starting with a #. After the #, a json must be given with the same information as the parameters.json file. This is a redundant way of giving the parameters and is used for programmatic reading with out a parameters.json file.

The soil moisture data looks like this:
```
$ head -n {head_n} soil_moisture_prediction/test_data/soil_moisture_data.csv
{soil_moisture_data}
```

The soil moisture data can have a header with the column names.

## Pydantic model
This is a description of the input parameters model:
{pydantic_model_information}"""  # noqa

# Used for tree representation of directory structure:
space = "    "
branch = "│   "
tee = "├── "
last = "└── "

file_exeptions = [
    "predictor_5_nan_in_training.csv",
    "predictor_5_wrong_nan.csv",
    "predictor_1_no_deviation.csv",
    "predictor_1_to_many_columns.csv",
]
current_dir = os.path.dirname(os.path.abspath(__file__))
test_data_dir = os.path.join(current_dir, "test_data")

head_n = 5


def tree(dir_path: Path, prefix: str = ""):
    """Like gnu tree.

    Found at https://stackoverflow.com/questions/9727673
    """
    contents = sorted([o for o in dir_path.iterdir() if o.name not in file_exeptions])

    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir():  # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix + extension)


def compile_information():
    """Compile the information string."""
    directory_tree = "\n".join(list(tree(Path(test_data_dir))))

    with open(os.path.join(test_data_dir, "parameters.json"), "r") as f_handle:
        parameters = json.loads(f_handle.read())
        parameter_content = json.dumps(parameters, indent=2)

    predictors_file = {
        pred: pred_data
        for pred, pred_data in parameters["predictors"].items()
        if pred == "predictor_1.csv"
    }

    # Some text formatting for the example predictor file
    example_predictor_template = '"predictors": {0},\n  ...\n}}'

    example_file_name_predictor = example_predictor_template.format(
        json.dumps(predictors_file, indent=2)[:-2]
    )

    predictors_file["/abs/path/to/predictor_1.csv"] = predictors_file.pop(
        "predictor_1.csv"
    )

    example_path_predictor = example_predictor_template.format(
        json.dumps(predictors_file, indent=2)[:-2]
    )

    predictor_data = ""
    with open(os.path.join(test_data_dir, "predictor_1.csv"), "r") as f_handle:
        for _ in range(head_n):
            predictor_data += f_handle.readline()
    predictor_data = predictor_data[:-1]

    soil_moisture_data = ""
    with open(os.path.join(test_data_dir, "crn_soil-moisture.csv"), "r") as f_handle:
        for _ in range(head_n):
            soil_moisture_data += f_handle.readline()
    soil_moisture_data = soil_moisture_data[:-1]

    pydantic_model_information = ""
    for field_name, field in InputParameters.model_fields.items():
        pydantic_model_information += f"{field_name}:\n  {field.description}\n\n"
    pydantic_model_information = pydantic_model_information[:-2]

    return information.format(
        directory_tree=directory_tree,
        parameter_content=parameter_content,
        head_n=head_n,
        predictor_data=predictor_data,
        soil_moisture_data=soil_moisture_data,
        pydantic_model_information=pydantic_model_information,
        example_file_name_predictor=example_file_name_predictor,
        example_path_predictor=example_path_predictor,
    )


if __name__ == "__main__":
    with open("README_template.md", "r") as f_handle:
        readme_template = f_handle.read()

    with open("README.md", "w") as f_handle:
        f_handle.write(
            readme_template.replace("usage_information_here", compile_information())
        )

    print(compile_information())
