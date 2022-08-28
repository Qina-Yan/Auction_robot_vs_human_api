from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
import os
import json
import pandas as pd
  
app = Flask(__name__)
api = Api(app)

# load trained classifier
model_path = 'models/model_XGB_balanced.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')

def get_prediction(score):
    '''
    score float: model proba
    return str: negative or positive
    '''
    return 'Robots' if score >=0.85 else 'Human'

def predict(context):
        """
        context: dictionary format {'cost':'$300k'... etc}
        return np.array
        """
        num_predictions = 1 #len(context[features[0]])
        X = pd.DataFrame(context,index=range(num_predictions))
        y_prob_pred = model.predict_proba(X)
        #float(round(y_prob_pred[0][1], 3) )
        return round(float(y_prob_pred[0][1]),3)
    
class PredictUser(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']
        # json needs to replace single quote with double 
        #X = json.loads(user_query.replace("\'", "\""))
        proba = predict(json.loads(user_query.replace("\'", "\"")))
        
        results = {'results':[]}
        #results['results'].append({'label': proba, 'ModelScore':1})  
        results['results'].append({'label': get_prediction(proba), 'ModelScore':proba})      
        return results


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictUser, '/')


if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port= int(os.environ.get("PORT", 5000)))