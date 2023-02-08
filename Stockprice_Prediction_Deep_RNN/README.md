# Stockprice_Prediction_RNN
GOOG stock price prediction using RNN algorithm implemented from scratch.

This project demonstrates our approach at building a Recurrent Neural Network (RNN) model from scratch that implements a time-series stock prediction based on Google’s stock price data of the past one year. We use the coefficient of determination, R-squared, to determine the accuracy of our model since it is a reliable measure of the proportion of variation that is explained by regression models.
Keywords — RNN, time-series, stock prediction, forecasting, deep learning

We have utilized a trustworthy data set for training from the Historical Data tab of Yahoo Finance stock quotes. The stock price data is obtained and transformed into a data frame via the Pandas package. The data available is from the dates April 23, 2021 to April 21, 2022.

Overall, we were able to build a model from scratch and train it such that at least 60% of the variation occurring in the real data could be explainable by the RNN algorithm we implemented, and this is an acceptable accuracy in this scenario.
