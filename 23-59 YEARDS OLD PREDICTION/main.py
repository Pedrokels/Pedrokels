import pickle
import numpy as np
from flask import Flask, request, jsonify

underweight_model = pickle.load(open("underweight_rf.pkl", "rb"))
overweight_model = pickle.load(open("overweight_rf.pkl","rb"))
wasting_model = pickle.load(open("wasting_rf_random_state=0.pkl", "rb")) 
stunting_model = pickle.load(open("stunting_rf.pkl", "rb"))

underweight_model59 = pickle.load(open("underweight_59mos_rf.pkl","rb"))
overweight_model59 = pickle.load(open("overweight_59mos_rf.pkl","rb"))
wasting_model59 = pickle.load(open("wasting_rf_random_state59.pkl","rb")) 
stunting_model59 = pickle.load(open("stunting_59mos_rf.pkl","rb"))

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def home():
    return 'Department of Science and Technology - Food and Nutrition Research Institute'

@app.route('/prediction', methods = ['POST'])
def predict():
    
    bw_grams = request.form.get('bw_grams')
    wdrinking = request.form.get('wdrinking')
    psoc_hh = request.form.get('psoc_hh')
    age_child = request.form.get('age_child')
    age_hh = request.form.get('age_hh') 
    educ_mom = request.form.get('educ_mom')
    parity = request.form.get('parity')
    feeding = request.form.get('feeding')
    educ1_hh = request.form.get('educ1_hh')

    input_query_underweight = np.array([[bw_grams,wdrinking,psoc_hh,age_child,age_hh,educ_mom]])
    input_query_wasting = np.array([[bw_grams,wdrinking,parity,age_child,psoc_hh,educ_mom]])  
    input_query_stunting = np.array([[bw_grams,wdrinking,parity,age_child,psoc_hh,educ_mom]])
    input_query_overweight = np.array([[bw_grams,age_hh,psoc_hh,feeding,educ1_hh]])
    prediction_underweight = underweight_model.predict(input_query_underweight)[0]
    prediction_wasting = wasting_model.predict(input_query_wasting)[0]
    prediction_stunting = stunting_model.predict(input_query_stunting)[0]
    prediction_overweight = overweight_model.predict(input_query_overweight)[0]
        
    if prediction_underweight == 0: 
        prediction_underweight = ('Normal')
    else:
        prediction_underweight =('Underweight')
    if prediction_wasting == 0 and prediction_overweight == 1: 
        prediction_wasting = ('Overweight')
    elif prediction_wasting == 1 and prediction_overweight == 0:
        prediction_wasting = ('Wasting')
    elif prediction_wasting == 0 and prediction_overweight == 0:
        prediction_wasting = ('Normal')
    else:
        prediction_wasting =  ('Invalid')
        
    if prediction_stunting == 0: 
        prediction_stunting = ('Normal')
    else:
        prediction_stunting = ('Stunted')

    return jsonify({"Underweight": prediction_underweight,
                    "WastingOverweight":  prediction_wasting,
                    "Stunting": prediction_stunting})
    
@app.route('/predictions', methods = ['POST'])
def predicts():
    
    bw_grams = request.form.get('bw_grams')
    psoc_hh = request.form.get('psoc_hh')
    age_hh = request.form.get('age_hh')
    hhsize = request.form.get('hhsize')
    psccat_mom = request.form.get('psccat_mom')
    drinkingwater = request.form.get('drinkingwater')
    educ_mom = request.form.get('educ_mom')
    wcooking = request.form.get('wcooking')
    educ_hh = request.form.get('educ_hh')
    agemos = request.form.get('agemos')
    whands = request.form.get('whands')
    occup_mom = request.form.get('occup_mom')
    
    input_query_underweight59 = np.array([[bw_grams,psoc_hh,age_hh,hhsize,psccat_mom,drinkingwater,educ_mom]])
    input_query_wasting59 = np.array([[bw_grams,psoc_hh,wcooking,psccat_mom,educ_hh,agemos,drinkingwater]])  
    input_query_stunting59 = np.array([[bw_grams,psoc_hh,age_hh,whands,psccat_mom,drinkingwater,educ_mom]])
    input_query_overweight59 = np.array([[bw_grams,psoc_hh,wcooking,age_hh,psccat_mom,occup_mom,drinkingwater]])

    prediction_underweight59 = underweight_model59.predict(input_query_underweight59)[0]
    prediction_wasting59 = wasting_model59.predict(input_query_wasting59)[0]
    prediction_stunting59 = stunting_model59.predict(input_query_stunting59)[0]
    prediction_overweight59 = overweight_model59.predict(input_query_overweight59)[0]
    
    if prediction_wasting59 ==0 and prediction_overweight59 == 1: 
        prediction_wasting59 = ('Overweight')
    elif prediction_wasting59 == 1 and prediction_overweight59 == 0:
        prediction_wasting59 = ('Wasting')
    elif prediction_wasting59 == 0 and prediction_overweight59 == 0:
        prediction_wasting59 = ('Normal')
    else:
        prediction_wasting59 =  ('Invalid')
    if prediction_underweight59 == 0: 
        prediction_underweight59 = ('Normal')
    else:
        prediction_underweight59 = ('Underweight')
    if prediction_stunting59 == 0: 
        prediction_stunting59 = ('Normal')
    else:
        prediction_stunting59 = ('Stunted')
 
    return jsonify({"Underweight": prediction_underweight59,
                    "WastingOverweight": prediction_wasting59,
                    "Stunting": prediction_stunting59})
     
if __name__ == '__main__':
    app.run(debug=True)