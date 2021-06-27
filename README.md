## About

This is a data visualization/forecasting web app I created for my research team using python and the [streamlit](https://streamlit.io/) library.  

The purpose of the project is to provide a light and easy-to-navigate web app for the child support field workers to work on their contact list. 

I have deployed the app to heroku. Click [this link](https://child-support-dashboard.herokuapp.com/) to check out the app.

## Functions
The app has two panels, one for case overview and another for working on specific cases.  
1. The case overview panel shows the text and visual summary of the selected field worker's cases.  
2. The working on cases panel provide the whole contact list.  
   
The contact list can be filtered and downloaded. The worker can also choose a specific case to work on. Once a case is entered, the app will first generate a text summary of this case. Certain information will only be shown when it's in the target category. For example, only when a payor was in the prison, the information will be shown here, otherwise not.  
  
Then, the app will generate a line chart to show the past payment record of this case. If the user hovers their mouse on the line chart, the monthly payment info will be shown.  
  
Since the monthly payment information is time-series data, I use a package called [prophet](https://facebook.github.io/prophet/) to forecast the payment in the next 6 months. Prophet is a procedure for forecasting time series data and it is developed by the Facebook Core Data Science team. Basically, this procedure will decompose the pattern in the time series data into trend, seasonality, and noise, and then make some predictions.  

The app will also generate a chart to show dots as the actual payments, and a line as the predicted payment.  
Finally, the app will generate two charts deriving from the prophet procedure, one for the trend and another for the yearly pattern.

## Requirements
- Python 3.9 or higher
- streamlit 0.83.0
- pandas 1.2.4
- matplotlib 3.4.2
- plotly 4.14.3
- fbprophet 0.7.1

## Installation
To run the app locally, the user need to install Python 3.9 and all the libraries listed above. 
To deploy the app online, please refer to [this link](https://discuss.streamlit.io/t/streamlit-deployment-guide-wiki/5099).

## Usage
Put the example_list.csv and dashboard.py in the same directory and then run the command below in your terminal to start the app.

`$ streamlit run dashboard.py`

## Known issues
Currently none.

## Next steps
This app is in beta stage. Will add more features upon request.
