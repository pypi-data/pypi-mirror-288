import pickle
import sys
import types

# Dynamically create a module and class structure matching the original structure
# module_name = "naiveBayesClassifier"
# class_name = "trainedData"
#
# # Create a new module
# naiveBayesClassifier = types.ModuleType(module_name)
# sys.modules[module_name] = naiveBayesClassifier


# Define the original class within this module
class NotSeen(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Token '{self.value}' is never seen in the training set."


class trainedData:
    def __init__(self):
        self.docCountOfClasses = {}
        self.frequencies = {}

    def increaseClass(self, className, byAmount=1):
        self.docCountOfClasses[className] = self.docCountOfClasses.get(className, 0) + 1

    def increaseToken(self, token, className, byAmount=1):
        if token not in self.frequencies:
            self.frequencies[token] = {}

        self.frequencies[token][className] = (
            self.frequencies[token].get(className, 0) + 1
        )

    def decreaseToken(self, token, className, byAmount=1):
        pass

    def getDocCount(self):
        return sum(self.docCountOfClasses.values())

    def getClasses(self):
        return self.docCountOfClasses.keys()

    def getClassDocCount(self, className):
        return self.docCountOfClasses.get(className, None)

    def getFrequency(self, token, className):
        try:
            foundToken = self.frequencies[token]
        except KeyError:
            raise NotSeen(token)

        try:
            return foundToken[className]
        except KeyError:
            return None


# Assign the class to the module
# setattr(naiveBayesClassifier, class_name, trainedData)

# Load the pickle file
model_file_path = "model_en.txt"
with open(model_file_path, "rb") as f:
    data = pickle.load(f)

# Now reassign the data to the new class location
# Assuming new_module.TrainedData has the same structure as the old class
import genderizer3.trainedData  # Replace this with the actual module path
import json

with open("c:\\users\\advan\\desktop\\stupid.json", "a+") as f:
    f.write(json.dumps(data.__dict__))
# print(data.__dict__)
new_class_instance = genderizer3.trainedData.TrainedData()
new_class_instance.__dict__.update(data.__dict__)

# Save the updated data back to a new pickle file
new_model_file_path = "model_en_updated.txt"
with open(new_model_file_path, "wb") as f:
    pickle.dump(new_class_instance, f, pickle.HIGHEST_PROTOCOL)

print(f"Updated the class name in the pickle file and saved to {new_model_file_path}.")
