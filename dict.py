import pickle

dict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "colour": "Purple"
}

with open("dict_serialized.pkl", "wb") as handle:
  pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open("dict_serialized.pkl", "rb") as handle:
  dict_unserialized = pickle.load(handle)

print(dict == dict_unserialized)
