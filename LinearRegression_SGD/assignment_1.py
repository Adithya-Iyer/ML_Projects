# -*- coding: utf-8 -*-
"""Assignment 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nCUyjfKiR-ms8zWq2aIoJX870jND6PLb

# Part 1: Manual Implementation of SGD Regressor

# CS6375 - Machine Learning

## Assignment 1

## Team:
Siddhant Suresh Medar - SSM200002 and Adithya Iyer - ASI200000

## Dataset used:

Computer Hardware Data Set

## Data Set Information:

The estimated relative performance values were estimated by the authors using a linear regression method. See their article (pp 308-313) for more details on how the relative performance values were set.


## Attribute Information:

1. vendor name: 30
(adviser, amdahl,apollo, basf, bti, burroughs, c.r.d, cambex, cdc, dec,
dg, formation, four-phase, gould, honeywell, hp, ibm, ipl, magnuson,
microdata, nas, ncr, nixdorf, perkin-elmer, prime, siemens, sperry,
sratus, wang)
2. Model Name: many unique symbols
3. MYCT: machine cycle time in nanoseconds (integer)
4. MMIN: minimum main memory in kilobytes (integer)
5. MMAX: maximum main memory in kilobytes (integer)
6. CACH: cache memory in kilobytes (integer)
7. CHMIN: minimum channels in units (integer)
8. CHMAX: maximum channels in units (integer)
9. PRP: published relative performance (integer)
10. ERP: estimated relative performance from the original article (integer)


## Relevant Papers:

Ein-Dor and Feldmesser (CACM 4/87, pp 308-317)

Kibler,D. & Aha,D. (1988). Instance-Based Prediction of Real-Valued Attributes. In Proceedings of the CSCSI (Canadian AI) Conference.

## Target Variable: 

ERP = estimated relative performance from the original article (integer)

# Import required libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.metrics import r2_score, explained_variance_score
from sklearn.linear_model import LinearRegression, SGDRegressor
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
import sys
import io
# %matplotlib inline

"""# Load the dataset"""

columns = ['VENDOR NAME','MODEL NAME','MYCT','MMIN','MMAX','CACH','CHMIN',
           'CHMAX','PRP','ERP']
df = pd.read_csv(
    'https://archive.ics.uci.edu/ml/machine-learning-databases/cpu-performance/machine.data'
    , names = columns)

"""# Peform Exploratory Data Analysis"""

#peek through the data
df.head()

"""## Pre-processing the data"""

#check for NULL values
print (df.isnull().sum())

#remove missing values - no missing values were found
df.dropna( inplace = True )

#drop duplicate items - no duplicate items were found
df.drop_duplicates()

#information about the data
df.info()

#explore data
df.describe()

#explore target variable
df["ERP"].describe()

"""## Feature Engineering"""

#histogram plots for each column
df.hist(bins=8, color='steelblue', edgecolor='black', linewidth=1.0, xlabelsize=8, ylabelsize=8, grid=False)
plt.tight_layout(rect=(0, 0, 1.2, 1.2))

#calculate correlation between the attributes
correlations = df.corr()
print(correlations)

#plot heatmap to visualize the correlation
sns.set(rc = {'figure.figsize':(10,8)})
sns.heatmap(correlations, annot=True,square=True)
plt.show()

#pairplot to check the pairwise relationships in the dataset
sns.set()
sns.pairplot(df, size=3)
plt.show()

"""### Conclusion: We observed during exploratory analysis that the first two attributes - Vendor name and Model Name does not contribute to the end result. 
### Decision : Drop two attributes - Vendor name and Model Name

# PART 1 - Impelementing SGD regressor manually

## Splitting the data into independent and dependent variables - X and y
"""

data = df.iloc[:,2:]

X = data.iloc[:,:-1]
y = data.iloc[:,-1]

# Splitting the data into training and testing samples 
#Using 80/20 split for training and testing respectively
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.20, random_state = 42, shuffle = True)

#shape of X_Train and X_Test
X_train.shape, X_test.shape

#shape of Y_Train and Y_Test
y_train.shape, y_test.shape

#standardize features by removing the mean and scaling to unit variance
sc = StandardScaler()
sc.fit(X_train)

#apply the calculations performed earlier in fit() 
#to every data point in feature using transform()
X_train_sc = sc.transform(X_train)
X_test_sc = sc.transform(X_test)

class ManualSGD:
    def __init__(self,learning_rate=0.001,max_iterations=500,threshold=None): 
        #constructor
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.threshold = threshold
     
    def predict(self,X): 
        #function to predict the values using newly created model
        X=np.insert(X.T,0,np.ones(X.shape[0]),axis=0)
        return np.dot(self.weights,X)

    def Rsquared(self,X,Y): 
        #function to calculate r2 score
        return 1-(((Y - self.predict(X))**2).sum()/((Y - Y.mean())**2).sum())

    def loss_function(self,x,y,category='mse'):
        if category == 'mse':
            loss=np.sum(np.square(x.reshape(-1, 1) - y.reshape(-1, 1)))
            /(2*x.shape[0])
        return np.round(loss,3)
    
    def fit(self,X,y): 
        #function to fit the data on the model
        self.losses=[] #list to track the losses
        self.X=X
        self.y=y
        #initialize weights and biases
        self.weights = np.random.rand(self.X.shape[1]+1).reshape(1,-1)               
        #pad with ones for bias
        self.feature_vector = np.insert(self.X.T, 0,
                                        np.ones(self.X.shape[0]), axis=0)   
        dw=0 
        
        while self.max_iterations>=0:
            self.hyp = np.dot(self.weights,self.feature_vector)
            self.losses.append(self.loss_function(self.hyp,y))
            # @ is matrix multiplication
            dw = (self.feature_vector@(self.hyp-self.y).T) 
            dw /= self.X.shape[0]        #average it
            self.weights -= (self.learning_rate*dw.reshape(1,-1)) 
            #update weights
            self.max_iterations -= 1 #decrement iterations count by 1

#Optimum LR and Itrs
lr, itrs = 0.003, 15000

#create object of class
model = ManualSGD(learning_rate=lr,max_iterations=itrs)

#fit the training data on the model
model.fit(X_train_sc,np.array(y_train))

#predict
y_pred=model.predict(X_test_sc)

loss=list(model.losses)

#visualize loss
plt.plot(loss)
plt.xlabel("Max_iterations")
plt.ylabel("Loss")
plt.show()

r2 = model.Rsquared(X_train_sc,np.array(y_train))
mae = mean_absolute_error(y_test, y_pred[0])
rmse = mean_squared_error(y_test, y_pred[0], squared=False)
evs = explained_variance_score(y_test, y_pred[0])

weights = list(model.weights)
print("Weights: ",weights)

print()
print("For LR: "+str(lr)+", Iterations= "+str(itrs))
print("======================================")
print("R2 Score: ", r2)
print("Mean absolute error: ", mae)
print("Root Mean squared error: ", rmse)
print("Explained Variance Score: ", evs)

file = open("Manual_SGD_log.txt","a")
file.write("LR = " + str(lr) + ", max_iterations = " + str(itrs) + 
           ", R^2 = "+str(r2) + ", MAE = "+str(mae) + ", RMSE = " + str(rmse) +
           ", Explained-Variance = " + str(evs) + " \n")
file.close()
print("Wrote to file sucessfully.")

"""## Observation:
## For a learning rate = 0.003 and n_iterations = 15000, we get a r2 score of 95.71%
## Now increasing iterations to check if it increases the accuracy further
"""

lr,r2_lst = 0.003,[]

itrs = 17500
while itrs<=50000:
    model = ManualSGD(learning_rate=lr,max_iterations=itrs)

    #fit the training data on the model
    model.fit(X_train_sc,np.array(y_train))

    #predict
    y_pred=model.predict(X_test_sc)

    loss=list(model.losses)

    #visualize loss
    plt.plot(loss)
    plt.xlabel("Max_iterations")
    plt.ylabel("Loss")
    plt.show()
    
    r2 = model.Rsquared(X_train_sc,np.array(y_train))
    mae = mean_absolute_error(y_test, y_pred[0])
    rmse = mean_squared_error(y_test, y_pred[0], squared=False)
    evs = explained_variance_score(y_test, y_pred[0])
    
    print("\nFor LR: "+str(lr)+", Iterations= "+str(itrs))
    print("======================================")
    print("R2 Score: ", r2)
    print("Mean absolute error: ", mae)
    print("Root Mean squared error: ", rmse)
    print("Explained Variance Score: ", evs)
    
    file = open("Manual_SGD_log.txt","a")
    file.write("LR = " + str(lr) + ", max_iterations = " + str(itrs) + 
               ", R^2 = " + str(r2) + ", MAE = " + str(mae) + ", RMSE = " + 
               str(rmse) + ", Explained-Variance = " + str(evs) + " \n")
    file.close()
    print("Wrote to file sucessfully.")

    r2_lst.append(np.around(r2,7))
    itrs+=2500

plt.plot(r2_lst)

"""## Conclusion:
## From the above plot, it can observed that increasing n_iterations above 15000 does not improve r2_score
#The increase is of the order of 10^-7, which is very insignificant for so many iterations

## Now we can try altering learning_rate
"""

#try combination of lr by keeping n_iterations constant i.e 15000
lr = 0.003
r2_lst = []

while lr >= 0.0001:
    model = ManualSGD(learning_rate=lr,max_iterations=15000)

    #fit the training data on the model
    model.fit(X_train_sc,np.array(y_train))

    #predict
    y_pred=model.predict(X_test_sc)

    loss=list(model.losses)

    #visualize loss
    plt.plot(loss)
    plt.xlabel("Max_iterations")
    plt.ylabel("Loss")
    plt.show()
    
    r2 = model.Rsquared(X_train_sc,np.array(y_train))
    mae = mean_absolute_error(y_test, y_pred[0])
    rmse = mean_squared_error(y_test, y_pred[0], squared=False)
    evs = explained_variance_score(y_test, y_pred[0])
    
    print("\nFor LR: "+str(lr)+", Iterations= "+str(itrs))
    print("======================================")
    print("R2 Score: ", r2)
    print("Mean absolute error: ", mae)
    print("Root Mean squared error: ", rmse)
    print("Explained Variance Score: ", evs)
    
    file = open("Manual_SGD_log.txt","a")
    file.write("LR = " + str(lr) + ", max_iterations = " + str(itrs) + 
               ", R^2 = " + str(r2) + ", MAE = " + str(mae) + ", RMSE = " + 
               str(rmse) + ", Explained-Variance = " + str(evs) + " \n")
    file.close()
    print("Wrote to file sucessfully.")

    r2_lst.append(np.around(r2,2))
    lr/=2

plt.plot(r2_lst)

"""## The accuracy falls when learning rate is altered while keeping the n_iterations same"""

lr = 0.003
r2_lst = []

while lr >= 0.0001:
    model = ManualSGD(learning_rate=lr,max_iterations=30000)

    #fit the training data on the model
    model.fit(X_train_sc,np.array(y_train))

    #predict
    y_pred=model.predict(X_test_sc)

    loss=list(model.losses)

    #visualize loss
    plt.plot(loss)
    plt.xlabel("Max_iterations")
    plt.ylabel("Loss")
    plt.show()
    
    r2 = model.Rsquared(X_train_sc,np.array(y_train))
    mae = mean_absolute_error(y_test, y_pred[0])
    rmse = mean_squared_error(y_test, y_pred[0], squared=False)
    evs = explained_variance_score(y_test, y_pred[0])
    
    print("\nFor LR: "+str(lr)+", Iterations= "+str(itrs))
    print("======================================")
    print("R2 Score: ", r2)
    print("Mean absolute error: ", mae)
    print("Root Mean squared error: ", rmse)
    print("Explained Variance Score: ", evs)
    
    file = open("Manual_SGD_log.txt","a")
    file.write("LR = " + str(lr) + ", max_iterations = " + str(itrs) + 
               ", R^2 = " + str(r2) + ", MAE = " + str(mae) + ", RMSE = " + 
               str(rmse) + ", Explained-Variance = " + str(evs) + " \n")
    file.close()
    print("Wrote to file sucessfully.")

    r2_lst.append(r2)
    lr/=2

plt.plot(r2_lst)

"""## From the above plot we can observe that increasing iterations also doesn't help much.

# PART 2 - Impelementing SGD regressor using Scikit-learn library
"""

#use GridSearchCV to loop through predefined hyperparameters and 
#    fit your estimator (model) on your training set to find 
#    the best parameters from the listed hyperparameters

p={'learning_rate': ['constant'], 'eta0': [0.001, 0.01, 0.02, 0.05, 0.08, 0.1],
   'max_iter':[500, 1000, 2000, 5000, 7000, 10000, 15000, 20000, 25000, 30000, 
               35000, 40000, 45000, 50000]}

sgd=SGDRegressor()

model=GridSearchCV(sgd,param_grid=p)

#fit the data on the model created
model.fit(X_train_sc,y_train)

#print best estimators found by the model
model.best_estimator_

#print best parameters found by the model
print(model.best_params_)

#print best score found by the model
print(model.best_score_)

#predict using the model
y_pred=model.predict(X_test_sc)

#calculate metrics
r2 = model.score(X_train_sc,y_train)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
evs = explained_variance_score(y_test, y_pred)

print("R2 Score: ", r2)
print("Mean absolute error: ", mae)
print("Root Mean squared error: ", rmse)
print("Explained Variance Score: ", evs)

"""## Conclusion: We obtained a r2 score of 95.16% using scikit library which is less than that of our custom SGD regressor's score using GridSearchCV

## Comparing model performance with same set of parameters as that of our custom model
"""

#Function to display loss curve during each iteration
class DisplayLossCurve(object):
  def __init__(self, print_loss=False):
    self.print_loss = print_loss

  """Make sure the model verbose is set to 1"""
  def __enter__(self):
    self.old_stdout = sys.stdout
    sys.stdout = self.mystdout = io.StringIO()
  
  def __exit__(self, *args, **kwargs):
    sys.stdout = self.old_stdout
    loss_history = self.mystdout.getvalue()
    loss_list = []
    for line in loss_history.split('\n'):
      if(len(line.split("loss: ")) == 1):
        continue
      loss_list.append(float(line.split("loss: ")[-1]))
    plt.figure()
    plt.plot(np.arange(len(loss_list)), loss_list)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")

    if self.print_loss:
      print("=============== Loss Array ===============")
      print(np.array(loss_list))
      
    return True

lr, itrs = 0.003, 15000
model=SGDRegressor(learning_rate='constant', eta0=lr, max_iter=itrs, verbose=1)

with DisplayLossCurve(print_loss=True):
    model.fit(X_train_sc,y_train)
        
y_pred=model.predict(X_test_sc)

r2 = model.score(X_train_sc,y_train)
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
evs = explained_variance_score(y_test, y_pred)

r2_lst.append(r2)

print()
print("LR: "+str(lr)+" Iterations= "+str(15000))
print("R2 Score: ", r2)
print("Mean absolute error: ", mae)
print("Root Mean squared error: ", rmse)
print("Explained Variance Score: ", evs)

file = open("Scikit_SGD_log.txt","a")
file.write("LR = " + str(lr) + ",max_iterations = " + str(itrs) + " R^2 = " + 
           str(r2) + ", MAE = " + str(mae) + ", RMSE = " + str(rmse) + 
           ",  Explained-Variance = " + str(evs) + " \n")
file.close()

plt.figure(figsize = (8,8))
plt.scatter(y_test, y_pred)
plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],'k--',lw=2)
plt.xlabel('Actual')
plt.ylabel('Predicted')
plt.title('Actual vs. Predicted')
plt.show()

file = open("Scikit_SGD_log.txt","a")
file.write("LR = " + str(lr) + ", max_iterations = " + str(itrs) + ", R^2 = " + 
           str(r2) + ", MAE = " + str(mae) + ", RMSE = " + str(r2) + 
           ", Explained-Variance = " + str(evs) + " \n")
file.close()
print("Wrote to file sucessfully.")

#weights obtained
model.coef_

"""## We obtained a r2 score of 95.16% using scikit library which is less than that of our custom SGD regressor's score

## Now we can try altering iterations to observe how it affects r2 score like we did in part 1
"""

itrs = 17500
lr =0.003
r2_lst = []

while itrs <= 50000:
    model=SGDRegressor(learning_rate='constant', eta0=lr, max_iter=itrs, verbose=1)

    with DisplayLossCurve(print_loss=True):
        model.fit(X_train_sc,y_train)

    y_pred=model.predict(X_test_sc)

    r2 = model.score(X_train_sc,y_train)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    evs = explained_variance_score(y_test, y_pred)

    r2_lst.append(r2)

    print()
    print("For LR: "+str(lr)+", Iterations= "+str(itrs))
    print("======================================")
    print("R2 Score: ", r2)
    print("Mean absolute error: ", mae)
    print("Root Mean squared error: ", rmse)
    print("Explained Variance Score: ", evs)

    file = open("Scikit_SGD_log.txt","a")
    file.write("LR = " + str(lr) + ",max_iterations = " + str(itrs) + " R^2 = " 
               + str(r2) + ", MAE = " + str(mae) + ", RMSE = " + str(rmse) + 
               ",  Explained-Variance = " + str(evs) + " \n")
    file.close()

    plt.figure(figsize = (8,8))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],'k--',lw=2)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs. Predicted')
    plt.show()
    
    itrs+=2500

plt.plot(r2_lst)

"""## R2 score fluctuates as seen from the above plot

## Now we try altering learning rate while keeping iterations same
"""

lr = 0.003
itrs=15000
r2_lst = []

while lr >= 0.0001:
    model=SGDRegressor(learning_rate='constant', eta0=lr, max_iter=itrs, verbose=1)

    with DisplayLossCurve(print_loss=True):
        model.fit(X_train_sc,y_train)

    y_pred=model.predict(X_test_sc)

    r2 = model.score(X_train_sc,y_train)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    evs = explained_variance_score(y_test, y_pred)

    r2_lst.append(r2)

    print()
    print("For LR: "+str(lr)+", Iterations= "+str(itrs))
    print("======================================")
    print("R2 Score: ", r2)
    print("Mean absolute error: ", mae)
    print("Root Mean squared error: ", rmse)
    print("Explained Variance Score: ", evs)

    file = open("Scikit_SGD_log.txt","a")
    file.write("LR = " + str(lr) + ",max_iterations = " + str(itrs) + " R^2 = "
    + str(r2) + ", MAE = " + str(mae) + ", RMSE = " + str(rmse) + 
    ",  Explained-Variance = " + str(evs) + " \n")
    file.close()

    plt.figure(figsize = (8,8))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],'k--',lw=2)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs. Predicted')
    plt.show()
    
    r2_lst.append(np.around(r2,2))
    lr/=2

plt.plot(r2_lst)

"""## This does not improves much

## We can try to improve the above plot by increasing iterations say 150000
"""

lr = 0.003
itrs = 150000
r2_lst = []

while lr >= 0.0001:
    model=SGDRegressor(learning_rate='constant', eta0=lr, max_iter=itrs, verbose=1)

    with DisplayLossCurve(print_loss=True):
        model.fit(X_train_sc,y_train)

    y_pred=model.predict(X_test_sc)

    r2 = model.score(X_train_sc,y_train)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    evs = explained_variance_score(y_test, y_pred)

    r2_lst.append(r2)

    print()
    print("For LR: "+str(lr)+", Iterations= "+str(itrs))
    print("======================================")
    print("R2 Score: ", r2)
    print("Mean absolute error: ", mae)
    print("Root Mean squared error: ", rmse)
    print("Explained Variance Score: ", evs)

    file = open("Scikit_SGD_log.txt","a")
    file.write("LR = " + str(lr) + ",max_iterations = " + str(itrs) + 
               " R^2 = " + str(r2) + ", MAE = " + str(mae) + ", RMSE = " 
               + str(rmse) + ",  Explained-Variance = " + str(evs) + " \n")
    file.close()

    plt.figure(figsize = (8,8))
    plt.scatter(y_test, y_pred)
    plt.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],'k--',lw=2)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('Actual vs. Predicted')
    plt.show()
    
    r2_lst.append(r2)
    lr/=2

plt.plot(r2_lst)

"""## We can observe this also doesn't help much

# Final Conclusion:
## Hence we conclude that our custom SGD regressor works better than Scikit's SGD regressor
"""