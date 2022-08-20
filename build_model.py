from transformer import Cost_Transformer
from model import ToyModel
import pickle

model = LogisticModel()
model.train()
with open('models/model.pkl', 'wb') as f:
	pickle.dump(model,f)