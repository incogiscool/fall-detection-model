from lib.clean import clean_dataset
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, RocCurveDisplay
from micromlgen import port

DATASET_PATH = "data/SisFall_dataset"
CLEANED_DATASET_PATH = "data/clean_data.csv"

# Uncomment the line below if you need to clean the dataset again
# clean_dataset(DATASET_PATH, CLEANED_DATASET_PATH)

# Read the cleaned dataset
dataframe = pd.read_csv(CLEANED_DATASET_PATH).sample(frac=1)

# Separate features and target variable
y = dataframe.pop("is_fall")
x = dataframe

# Split the dataset into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=16)

print("split dataset", x_train.shape, x_test.shape, y_train.shape, y_test.shape)

# Initialize the logistic regression model
logreg = LogisticRegression(random_state=16, max_iter=10000)

print("model initialized")

# Train the model
print("training model")
logreg.fit(x_train, y_train)

# Port model to C (for arduino)
if __name__ == '__main__':
    c_code = port(clf=logreg)
    print(c_code)

    # Save model to file (model.h)
    with open("model.h", "w") as f:
        f.write(c_code)

# Predict the test set
print("predicting")
y_pred = logreg.predict(x_test)

# Print the accuracy of the model
accuracy = logreg.score(x_test, y_test) * 100
print(f"accuracy: {accuracy:.2f}%")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.show()

# ROC curve
fpr, tpr, _ = roc_curve(y_test, logreg.decision_function(x_test))
roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()
plt.show()
