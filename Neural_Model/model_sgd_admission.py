
import os
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from tensorflow.keras.losses import MeanSquaredError
from utils.database import add_admission_features_to_database, fetch_user_id, add_training_mode_admission
from streamlit_lottie import st_lottie_spinner, st_lottie
from featurewiz import featurewiz
import joblib
from extra_streamlit_components import CookieManager
from sklearn.naive_bayes import GaussianNB

#-------------------------------Objects initializations-----------------#
cookies = CookieManager(key="mode1")
#-----------------------------------------------------------------------#


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def replace_nan_with_zeros(df):
    return df.fillna(0)


def replace_categorical(df):
    sections = [i for i in df.columns if df[i].dtype == object]
    for i in sections:
        fe = df.groupby(i).size()
        fe_ = fe/len(df)
        df["data_fe_"+i] = df[i].map(fe_).round(2)
        df.drop(i, axis=1, inplace=True)
    return df


def custom_model_training(features, target, dataframe, st, cookie_manager):
    #-------------Streamlit containers-------------------------#
    messagesContainers = st.container()
    #----------------------------------------------------------#
    st.set_option('deprecation.showPyplotGlobalUse', False)
    dataframe = replace_nan_with_zeros(dataframe)
    dataframe = replace_categorical(dataframe)

    for i in features:
        if features[i].dtype == object:
            features.rename(columns={i: f'data_fe_{i}'}, inplace=True)

    x = dataframe[features.columns]
    EPOCHS=3*len(features.columns)
    y = dataframe[target.name]

    scaler = MinMaxScaler()
    normalised = scaler.fit_transform(x)
    mse = MeanSquaredError()
    x_scale = normalised
    kfold = StratifiedKFold(n_splits=5)
    input_neuron_numbers = len(x.columns)
    hidden_neuron_numbers = int((2/3)*input_neuron_numbers+1)
    model_1 = Sequential([
        Dense(input_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(hidden_neuron_numbers, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    messagesContainers.info("Task is executing, Please wait...")
    with st_lottie_spinner(load_lottiefile("assests\\lottianimations\\lottie-chat-bot.json"), key='Training is underway', height=350, width='100%', speed=1.4):
        bar = st.progress(0)
        i = 0
        y_true = []
        y_pred = []
        for train, test in kfold.split(x_scale, y):
            i += 20
            model_1.compile(optimizer='sgd',
                            loss=mse,
                            metrics=['accuracy'])
            x_val, x_test, y_val, y_test = train_test_split(
                x_scale[test], y.iloc[test].values, test_size=0.3)

            model_1.fit(
                x_scale[train], y.iloc[train].values,
                epochs=EPOCHS,
                batch_size=256,
                validation_data=(x_val, y_val),
                verbose=0
            )

            model_1.evaluate(
                x_scale[test],
                y.iloc[test].values,
                verbose=0
            )

            predictions = model_1.predict(x_scale[test], verbose=0)
            # st.write(np.argmax(predictions,axis=0))
            y_pred.extend(predictions.round().flatten().tolist())
            y_true.extend(y.iloc[test].tolist())
            bar.progress(i)

    # calculate accuracy
    accuracy = accuracy_score(y_true, y_pred)
    # Calculate precision
    precision = precision_score(y_true, y_pred)
    # Calculate recall
    recall = recall_score(y_true, y_pred)
    # Calculate F1-score
    f1score = f1_score(y_true, y_pred)

    # colors = ['blue', 'orange', 'red', 'green']
    # data = [go.Bar(x=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
    #                y=[accuracy, precision, recall, f1score],
    #                marker=dict(
    #     color=colors,
    #     line=dict(
    #         color='blue',
    #         width=0.2,
    #     )
    # ),
    #     opacity=0.8,
    #     width=0.5,
    # ),
    # ]

    # layout = go.Layout(
    #     title='Performance Metrics',
    #     xaxis=dict(title='Metrics'),
    #     yaxis=dict(title='Score', range=[0, 1]),
    #     height=500,
    #     width=800,
    # )

    # fig = go.Figure(data=data, layout=layout)

    # st.plotly_chart(fig, use_container_width=True)
    # #-----------------Save model to database---------------#
    id = fetch_user_id(cookie_manager.get(cookie='email'))
    os.makedirs(f"Main_Models\\{id}\\admission_model", exist_ok=True)
    add_training_mode_admission("custom", cookie_manager.get(cookie='email'))
    model_1.save(f"Main_Models\\{id}\\admission_model\\model")
    #------------Show lottie success----------------------#

    st_lottie(load_lottiefile("assests\\lottianimations\\model-trained.json"),
              key="model success", height=150, width="100%", speed=0.9)
    st.success("Model is trained and saved to dataset")
    #------------------------------------------------------#

#---------------------------------neural network for default training--------------------------#


def default_model(st, dataframe, target, cookie_manager, features=None):
    #-------------Streamlit containers-------------------------#
    messagesContainers = st.container()
    #----------------------------------------------------------#
    if features is None:
        x = dataframe
        y = target
    else:
        x = dataframe[features]
        y = dataframe[target.name]

    #------------------Renaming features so that we can use it in the model training-----------------#
    '''If we do not rename this we will get error for object dtype columns that they do not exist'''

    scaler = MinMaxScaler()
    normalised = scaler.fit_transform(x)
    x_scale = normalised
    kfold = StratifiedKFold(n_splits=5)
    model_1 = GaussianNB()

    messagesContainers.info("Task is executing, Please wait...")
    y_true = []
    y_pred = []
    for train, test in kfold.split(x_scale, y):
        model_1.fit(x_scale[train], y.iloc[train].values)
        predictions = model_1.predict(x_scale[test])
        # st.write(np.argmax(predictions,axis=0))
        y_pred.extend(predictions.round().flatten().tolist())
        y_true.extend(y.iloc[test].tolist())

        # calculate accuracy
        accuracy = accuracy_score(y_true, y_pred)
        # Calculate precision
        precision = precision_score(y_true, y_pred)
        # Calculate recall
        recall = recall_score(y_true, y_pred)
        # Calculate F1-score
        f1score = f1_score(y_true, y_pred)

    return accuracy, precision, recall, f1score, model_1


# Default model training
def default_model_training(dataframe, target, data, st, cookie_manager):
    #----------------------------------------------------------#
    st.set_option('deprecation.showPyplotGlobalUse', False)
    dataframe = replace_nan_with_zeros(dataframe)
    dataframe = replace_categorical(dataframe)

    scaler = MinMaxScaler()
    normalised = scaler.fit_transform(dataframe)

    x_scale = pd.DataFrame(normalised, columns=dataframe.columns)
    features, train_df = featurewiz(x_scale, target=target.name, corr_limit=0.70,
                                    verbose=0, skip_sulov=True)

    #------------------------------------If no features has been retrived from featurewiz then performing with whole --------------#
    if len(features) == 0:
        add_admission_features_to_database(
            cookie_manager.get(cookie="email"), dataframe.columns)
        accuracy, precision, recall, f1score, model_1 = default_model(
            st, x_scale, target, cookie_manager, features=None)
    #-----------------------------------------If length is not zero----------------------------------------#
    else:
        add_admission_features_to_database(
            cookie_manager.get(cookie="email"), features)

    accuracy, precision, recall, f1score, model_1 = default_model(
        st, train_df, target, cookie_manager, features=features)
    add_training_mode_admission('default', cookie_manager.get(cookie='email'))
    # colors = ['blue', 'orange', 'red', 'green']
    # data = [go.Bar(x=['Accuracy', 'Precision', 'Recall', 'F1-Score'],
    #                y=[accuracy, precision, recall, f1score],
    #                marker=dict(
    #     color=colors,
    #     line=dict(
    #         color='blue',
    #         width=0.2,
    #     )
    # ),
    #     opacity=0.8,
    #     width=0.5,
    # ),
    # ]

    # layout = go.Layout(
    #     title='Performance Metrics',
    #     xaxis=dict(title='Metrics'),
    #     yaxis=dict(title='Score', range=[0, 1]),
    #     height=500,
    #     width=800,
    # )

    # fig = go.Figure(data=data, layout=layout)

    # st.plotly_chart(fig, use_container_width=True)
    ##-----------------Save model to database---------------#
    id = fetch_user_id(cookie_manager.get(cookie='email'))
    os.makedirs(f"Main_Models\\{id}\\admission_model", exist_ok=True)
    joblib.dump(
        model_1, f"Main_Models\\{id}\\admission_model\\model.joblib")
    #------------Show lottie success----------------------#
    st.success("Model is trained and saved to dataset")
    st_lottie(load_lottiefile("assests\\lottianimations\\model-trained.json"),
              key="model success", height=150, width="100%", speed=0.9)
    #------------------------------------------------------#
