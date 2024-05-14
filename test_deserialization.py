"""dictionary deserialization test"""
import pickle
# deserialize file received from client using load() function
with open('received_file_dict_serialized.pkl', 'rb') as handle:
    dict_deserialized = pickle.load(handle)
    # print dictionary
    print(dict_deserialized)



