import numpy as np

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from tensorflow.keras.losses import MeanSquaredError
import matplotlib.pyplot as plt

def replace_nan_with_zeros(df):
    return df.fillna(0)

def replace_categorical(df):
    sections =[i for i in df.columns if df[i].dtype==object]
    for i in sections:
        fe = df.groupby(i).size()
        fe_ = fe/len(df)
        df["data_fe_"+i] = df[i].map(fe_).round(2)
        df.drop(i,axis=1,inplace=True)
    return df
    
def custom_model_training(df,st):
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df=replace_nan_with_zeros(df)
    df=replace_categorical(df)
    x=df[[i for i in df.columns if i!="Admitted"]]
    y=df[['Admitted']]
    st.write("Scaling the data...")
    scaler = MinMaxScaler()
    normalised = scaler.fit_transform(x)
    st.write("Model Training is started.....")
    st.write("-------------------------------------------------------------------------------------------------------\n")
    mse = MeanSquaredError()
    x_scale=normalised
    kfold = StratifiedKFold(n_splits=5)
    cvscores=[]
    cvloss=[]
    iteration_counter=0
    input_neuron_numbers=len(x.columns)
    hidden_neuron_numbers=int((2/3)*input_neuron_numbers+1)
    
    
    
    model_1 = Sequential([
        Dense(input_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(1, activation='sigmoid'),
        ])


    for train, test in kfold.split(x_scale, y):
        model_1.compile(optimizer='sgd',
                  loss=mse,
                  metrics=['accuracy'])
        x_val, x_test, y_val, y_test = train_test_split(x_scale[test], y.iloc[test].values, test_size=0.5)
        
        hist=model_1.fit(
            x_scale[train], y.iloc[train].values, 
            epochs=100, 
            batch_size=32,
            validation_data=(x_val, y_val),
            verbose=0
        )
        
        scores = model_1.evaluate(
            x_scale[test], 
            y.iloc[test].values,
            verbose=0
        )
        
        

        iteration_counter+=1
        st.write(f"Metrics at iteration {iteration_counter}")
             
        
        plt.plot(hist.history['loss'])
        plt.plot(hist.history['val_loss'])
        plt.title(f'Model loss at {iteration_counter} iteration')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper right')
        st.pyplot(plt.show())

        plt.plot(hist.history['accuracy'])
        plt.plot(hist.history['val_accuracy'])
        plt.title(f'Model accuracy at {iteration_counter} iteration')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='lower right')
        st.pyplot(plt.show())
                
        for i in range(len(model_1.metrics_names)):
            st.write(" %s: %.2f%%" % (model_1.metrics_names[i], scores[i]*100))
        cvscores.append(scores[1] * 100)
        cvloss.append(scores[0]*100)
        
       
        
        
        st.write("-------------------------------------------------------------------------------------------------------\n")
        
        
    st.write("Model 1 overall Accuracy-:%.2f%% (+/- %.2f%%)"%(np.mean(cvscores), np.std(cvscores)))
    st.write("Model 1 overall loss-:%.2f%% (+/- %.2f%%)"%(np.mean(cvloss), np.std(cvloss)))
    model_1.save("model_sgd.h5")






#Default model training
def default_model_training(df,st):
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df=replace_nan_with_zeros(df)
    df=replace_categorical(df)
    x=df[[i for i in df.columns if i!="Admitted"]]
    y=df[['Admitted']]
    st.write("Scaling the data...")
    scaler = MinMaxScaler()
    normalised = scaler.fit_transform(x)
    st.write("Model Training is started.....")
    st.write("-------------------------------------------------------------------------------------------------------\n")
    mse = MeanSquaredError()
    x_scale=normalised
    kfold = StratifiedKFold(n_splits=5)
    cvscores=[]
    cvloss=[]
    iteration_counter=0
    model_1 = Sequential([
        Dense(13, activation='relu'),
        Dense(10, activation='relu'),
        Dense(10, activation='relu'),
        Dense(10, activation='relu'),
        Dense(10, activation='relu'),
        Dense(1, activation='sigmoid'),
        ])


    for train, test in kfold.split(x_scale, y):
        model_1.compile(optimizer='sgd',
                  loss=mse,
                  metrics=['accuracy'])
        x_val, x_test, y_val, y_test = train_test_split(x_scale[test], y.iloc[test].values, test_size=0.5)
        
        hist=model_1.fit(
            x_scale[train], y.iloc[train].values, 
            epochs=100, 
            batch_size=32,
            validation_data=(x_val, y_val),
            verbose=0
        )
        
        scores = model_1.evaluate(
            x_scale[test], 
            y.iloc[test].values,
            verbose=0
        )
        
        

        iteration_counter+=1
        st.write(f"Metrics at iteration {iteration_counter}")
             
        plt.plot(hist.history['loss'])
        plt.plot(hist.history['val_loss'])
        plt.title(f'Model loss at {iteration_counter} iteration')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='upper right')
        st.pyplot(plt.show())

        plt.plot(hist.history['accuracy'])
        plt.plot(hist.history['val_accuracy'])
        plt.title(f'Model accuracy at {iteration_counter} iteration')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Val'], loc='lower right')
        st.pyplot(plt.show())
                
        for i in range(len(model_1.metrics_names)):
            st.write(" %s: %.2f%%" % (model_1.metrics_names[i], scores[i]*100))
        cvscores.append(scores[1] * 100)
        cvloss.append(scores[0]*100)
        
       
        
        
        st.write("-------------------------------------------------------------------------------------------------------\n")
        
        
    st.write("Model 1 overall Accuracy-:%.2f%% (+/- %.2f%%)"%(np.mean(cvscores), np.std(cvscores)))
    st.write("Model 1 overall loss-:%.2f%% (+/- %.2f%%)"%(np.mean(cvloss), np.std(cvloss)))
    model_1.save("model_sgd.h5")
