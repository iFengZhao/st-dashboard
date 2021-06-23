## About

This is a data visualization/forecasting web app I created for my research team using python and the streamlit library.  

The purpose of the project is to provide a light and easy-to-navigate web app for the child support field worker to work on their contact list.  
The app has two panels, one for case overview and another for working on specific cases.  
1. The case overview panel shows the text and visual summary of the selected field worker's cases.  
2. The working on cases panel provide the whole contact list. 

## Functions
The list can be filtered and downloaded. On this panel, the worker can also choose a specific case to work on. Once a case is entered, the app will first generate a text summary of this case. Certain information will only be shown when it's in the target category. For example, only when a payor was in the prison, the information will be shown here, otherwise not.  
Then, the app will generate a line chart to show the past payment record of this case. If the user hovers their mouse on the line chart, the monthly payment info will be shown.  
Since the monthly payment information is time-series data, I use a package called [prophet](https://facebook.github.io/prophet/) to forecast the payment in the next 6 months. Prophet is a procedure for forecasting time series data and it is developed by the Facebook Core Data Science team. Basically, this procedure will decompose the pattern in the time series data into trend, seasonality, and noise, and then make some predictions.
As we can see in this chart, this dot is the actual payment, and this is the predicted payment. The predictions are less than ideal and they can provide some references.
This is the trend identified by the procedure, and it is an upward one. 
And this is the yearly pattern.

## Requirements
- Python 3.9 or higher
- streamlit 0.83.0
- pandas 1.2.4
- matplotlib 3.4.2
- plotly 4.14.3
- fbprophet 0.7.1

## Installation
No other package is needed to be installed. 

## Usage
To play the game, make sure the three files above are in the same directory and execute the **play_ghost.py** file.

## Known issues
Currently none.

## Next steps
Save a record for each round of the game.