import pandas as pd
import joblib
#joblib.load
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import r2_score, accuracy_score,classification_report
df=pd.read_csv("flood_predicts/weather_flood_synthetic_10000.csv")
print(df.shape)
print(df.info)
# Now split into x and y
x=df.iloc[:,1:10]
y=df["flood"]
print(x.info)
print(y.info)
# train text split
x_train,x_text,y_train,y_test=train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
# Use scaller 
scale=StandardScaler()
x_train=scale.fit_transform(x_train)
print(x_train)
#y_train answer of x_train
x_text=scale.transform(x_text)
# Now use model
#num_0=sum(y_train ==0)
#num_1=sum(y_train == 1)
#scale=num_0/num_1
model_output=XGBClassifier(
    # This is hyperparametertunning
    scale_pos_weight=4.56,
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    random_state=42,   
    min_child_weight=5,
    subsample=0.8,
    colsample_bytree=0.8
)
print(len(x_train))
print(len(y_train))
model_output.fit(x_train,y_train)
#model_work=model_output.predict(x_text)
# using this instend of upper 
model_probality=model_output.predict_proba(x_text)[:,1]
for threashold in [ 0.6,0.55, 0.50, 0.45,0.40,0.35,0.30]:
    model_work=(model_probality >=threashold).astype(int)
# accuracy
    print("Accuracy:",accuracy_score(y_test,model_work))
    print("classification info:",classification_report(y_test,model_work))
    print("confusion_matric:",confusion_matrix(y_test,model_work))
    print("Model type:", type(model_output))
    print("Prediction type:", type(model_output))
# save the model
joblib.dump(model_output,"flood_nodel.pkl")
joblib.dump(scale,"flood_scaler.pkl")

print("model fllood successfully")
