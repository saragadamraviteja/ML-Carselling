from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type=request.form['Fuel_Type_Petrol']
        if(Fuel_Type=='Petrol'):
                Petrol=1
                Diesel=0
                CNG = 0
        elif(Fuel_Type=='Diesel'):
            Petrol=0
            Diesel=1
            CNG = 0
        else:
            Petrol = 0
            Diesel = 0
            CNG = 1
        Year=2020-Year
        Seller_Type=request.form['Seller_Type_Individual']
        if(Seller_Type=='Individual'):
            Individual = 1
            Dealer = 0
        else:
            Individual = 0
            Dealer = 1 	
        Transmission=request.form['Transmission_Mannual']
        if(Transmission=='Mannual'):
            Manual=1
            Automatic = 0
        else:
            Manual=0
            Automatic = 1    										
        prediction=model.predict([[Present_Price,Kms_Driven2,Owner,Year,Dealer,Individual,CNG,Diesel,Petrol,Automatic,Manual]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)