# SOIL MOISTURE PREDICTION

## Description
This script performs soil moisture prediction using a Random Forest model based on soil properties. Additionally, it allows for incorporating soil moisture uncertainty in the input file and performs a probabilistic prediction using a Monte Carlo approach.

## Usage

The package provides a command line interface `smp_cli` to run the prediction. 

The cli-tool takes the path to a directory containing a JSON file with input parameters. The input files can be put in the same directory as the parameters file or must be given as an absolute path.

## Directory structure
This is an example of this directory structure:

```
soil_moisture_prediction/test_data/
├── crn_soil-moisture.csv
├── parameters.json
├── predictor_1.csv
├── predictor_2.csv
├── predictor_3.csv
├── predictor_4.csv
└── predictor_5.csv
```

## Input parameters
The parameters.json file in this example directory contains the following content:

```
$ cat soil_moisture_prediction/test_data/parameters.json
{
  "geometry": [
    632612,
    634112,
    5739607,
    5741107,
    250
  ],
  "predictors": {
    "predictor_1.csv": {
      "predictor_type": "elevation",
      "unit": "m",
      "std_deviation": true,
      "constant": true,
      "nan_value": ""
    },
    "predictor_2.csv": {
      "predictor_type": "variable predictor",
      "unit": "u",
      "std_deviation": true,
      "constant": false,
      "nan_value": "0.0"
    },
    "predictor_3.csv": {
      "predictor_type": "pred_3",
      "unit": "u",
      "std_deviation": true,
      "constant": true,
      "nan_value": ""
    },
    "predictor_4.csv": {
      "predictor_type": "pred_4",
      "unit": "u",
      "std_deviation": true,
      "constant": true,
      "nan_value": ""
    },
    "predictor_5.csv": {
      "predictor_type": "pred_5",
      "unit": "u",
      "std_deviation": true,
      "constant": true,
      "nan_value": "NaN"
    }
  },
  "soil_moisture_data": "crn_soil-moisture.csv",
  "monte_carlo_soil_moisture": false,
  "monte_carlo_predictors": false,
  "monte_carlo_iterations": 10,
  "predictor_qmc_sampling": false,
  "compute_slope": true,
  "compute_aspect": true,
  "past_prediction_as_feature": true,
  "reset_when_rain_occured": false,
  "average_measurements_over_time": true,
  "allow_nan_in_training": false,
  "what_to_plot": {
    "predictors": true,
    "pred_correlation": true,
    "day_measurements": true,
    "day_predictor_importance": true,
    "day_prediction_map": true,
    "alldays_predictor_importance": true
  },
  "save_results": true
}
```

## Input data
If the keys of "predictors" and "soil_moisture_data" are not a path to a file, the file is assumed to be in the same directory as the parameters.json file. So instead of:

```
"predictors": {
  "predictor_1.csv": {
    "predictor_type": "elevation",
    "unit": "m",
    "std_deviation": true,
    "constant": true,
    "nan_value": ""
  },
  ...
}
```

The predicotrs could be written as:

```
"predictors": {
  "/abs/path/to/predictor_1.csv": {
    "predictor_type": "elevation",
    "unit": "m",
    "std_deviation": true,
    "constant": true,
    "nan_value": ""
  },
  ...
}
```

The predictor data looks like this:
```
$ head -n 5 soil_moisture_prediction/test_data/predictor_data.csv
# { "predictor_type": "elevation", "unit": "m", "std_deviation": true, "constant": true, "nan_value": "" }
632200.0,5741600.0,251.3,5.026
632400.0,5741600.0,241.85,4.837
632600.0,5741600.0,235.02,4.7004
632800.0,5741600.0,229.0,4.58
```

The predictor can have a head starting with a #. After the #, a json must be given with the same information as the parameters.json file. This is a redundant way of giving the parameters and is used for programmatic reading with out a parameters.json file.

The soil moisture data looks like this:
```
$ head -n 5 soil_moisture_prediction/test_data/soil_moisture_data.csv
EPSG_UTM_x,EPSG_UTM_y,Day,soil_moisture,err_low,err_high
633742.2079,5741065.818,20220327,0.26870625,-0.0264875,0.0298375
633694.9659,5741026.54,20220327,0.27261,-0.02075,0.022775
633652.0085,5740981.625,20220327,0.27655625,-0.0171125,0.018425
633613.7622,5740928.489,20220327,0.280341071,-0.01545,0.0165375
```

The soil moisture data can have a header with the column names.

## Pydantic model
This is a description of the input parameters model:
geometry:
  A list of five numbers representing the bounding box. [xmin, xmax, ymin, ymax, resolution].

soil_moisture_data:
  A dictionary with keys as filenames or paths to the CRNS data and values as a list of timesteps (list can be an empty string).

predictors:
  A dictionary with keys as filenames or paths to the predictor data and values as a dictonary of preditor information (predictor_type and unit can be an empty string).

monte_carlo_soil_moisture:
  Whether to use a Monte Carlo Simulation to predict uncertainty for soil moisture.

monte_carlo_predictors:
  Whether to use a Monte Carlo Simulation to predict uncertainty for the predictors.

monte_carlo_iterations:
  Number of iterations for the Monte Carlo Simulation.

allow_nan_in_training:
  Whether to allow NaN values in the training data.

predictor_qmc_sampling:
  Whether to use Quasi-Monte Carlo sampling for the predictors.

reset_when_rain_occured:
  Whether to reset the model when rain occured.

compute_slope:
  Whether to compute the slope from elevation and use as predictor.

compute_aspect:
  Whether to compute the aspect from elevation and use as predictor.

past_prediction_as_feature:
  Whether to use the past prediction as a feature.

average_measurements_over_time:
  Whether to average the measurements over time.

what_to_plot:
  List of which plotting functions should be used.

save_results:
  Dump random as numpy arrays.

## Algorithm
The algorithm trains a random forest regressor (RandomForestRegressor from scikit-learn) with the soil moisture data and the predictor values at the measurements locations.
The trained model is then applied on the whole densely gridded area. 
The output is the a numpy array with the soil moisture values at each grid node. 

## Visualization
In addition to the resulting array(s) (prediction only or prediction and coefficient of dispersion),
the programm offers to plot some results.  
*predictors*: plot all the predictors as color maps after re-gridding them to the project grid.  
*pred\_correlation*: compute and plot the correlation between each predictors and display them as a heatmap. The color intensity indicates the strength and direction of correlation,
ranging from -1 (strong negative correlation) to 1 (strong positive correlation). It can help to remove redundant predictors highly correlated between them.  
*day\_measurements*: plot soil moisture measurements as a scatter plot on an x-y mapfor each day. The measurements are colored according to their corresponding soil moisture values.
If Monte Carlo simulations are enabled, error bands representing the standard deviations are overlaid on the scatter plot.  
*day\_predictor\_importance*: plot histogram of the normalized predictor importances from the random forest model for each day.  
If Monte Carlo simulations are enabled, the plot shows the 5th, 50th (median), and 95th quantiles of the importance values.
*day\_prediction\_map*: plot the map of the densely modelled soil moisture on the project area. If uncertainty are provided
the coefficient of dispersion map is also provided.  
*alldays\_predictor\_importance*: if several days are provided, the predictor importance is computed for each day 
and a curve of the predictor importance along days is plotted for each predictor. The x-axis represents the days, and the y-axis represents the importance values.
