"""dictionary serialization"""
import pickle

this_dict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964,
  "colour": "Purple"
}
# Open the pickle file in
# binary writing mode
with open("dict_serialized.pkl", "wb") as handle:
    # Serialize the dictionary
    pickle.dump(this_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
