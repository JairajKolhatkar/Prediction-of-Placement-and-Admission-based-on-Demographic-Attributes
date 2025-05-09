import plotly.graph_objs as go
import streamlit as st
import pandas as pd
import joblib 
from os import path
import plotly.io as pio
from Neural_Model.model_sgd_admission import replace_categorical, replace_nan_with_zeros
from sklearn.preprocessing import MinMaxScaler
from utils.database import fetch_placement_features_from_database, fetch_user_id,retrive_training_mode_placement
from keras.models import load_model
from extra_streamlit_components import CookieManager 

#-------------------------Object initializatiobs--------------------------#
cookies = CookieManager()
#-------------------------------------------------------------------------#


def get_graph(graph_df,i,colors):
    bar = go.Figure(go.Bar(x=graph_df[i], y=graph_df['Placed'], marker=dict(color=colors)))
    bar.update_yaxes(title="percentage")
    bar.update_layout(
        yaxis=dict(
        title="Percentage",
        range=[0, graph_df['Placed'].max()]
        ),
        xaxis=dict(
        title=f"{i}"
        )
    )
    bar.update_traces(text=graph_df['Placed'].apply(
        lambda x: round((x/graph_df["Placed"].sum())*100, 2)), textposition='auto')
    #-----------Draw doughnt chart-------------------------------#
    pie = go.Figure(go.Pie(labels=graph_df[i], values=graph_df['Placed'], hole=.5, marker=dict(
        colors=colors), textposition='inside'))
    pie.update_layout(width=800, height=500)

    return bar,pie
    



def use_placement(user):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    id = fetch_user_id(user)
    if not path.exists(f"Main_Models\\{id}\\placement_model"):
        st.error("No model has been trained")
        return 
    st.header("Choose CSV file")
    uploaded_file = st.file_uploader("", key="use_placement")
    if uploaded_file is not None: 
        #----------------To acess the fetched columns into list we have used this eval function--------------#
        features = fetch_placement_features_from_database(user)
        # Create a list of columns of csv files and return rhe list and its dataframe
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file)
            dataframe.columns = dataframe.columns.str.replace(" ", "")
            try:                    
                try:
                    df = dataframe[features]
                except KeyError as err:
                    raise ValueError(
                        "The uploaded dataset may be have differnt features than the dataset on which model has been trained and the important error is as: "+str(err))
                st.write("Scaling the data...")

                df = replace_nan_with_zeros(df)
                df = replace_categorical(df)
                scaler = MinMaxScaler()
                normalised = scaler.fit_transform(df)
                
                if retrive_training_mode_placement(user) == "custom": 
                    loaded_model = load_model(f"Main_Models\\{id}\\placement_model\\model")
                elif retrive_training_mode_placement(user) == "default":
                    loaded_model=joblib.load(f"Main_Models\\{id}\\placement_model\\model.joblib")
                else:
                    st.error("No model has been trained")
                    return
                c = (loaded_model.predict(normalised))
                c_df = [i for i in c if i>=0.6]
                st.header("Expand the categories to visualize the predictions")
                sections = [i for i in dataframe.columns if dataframe[i].dtype == object]
                for i in sections:
                    with st.expander(f"{i}"):
                        st.markdown(
                            f"<h1 style='text-align: center;'>Reports of {i}</h1>", unsafe_allow_html=True)
                        temp_df = dataframe[i]
                        temp_df = temp_df.to_frame()
                        temp_df['Placed'] = pd.DataFrame(c_df)
                        temp_df = temp_df.dropna()
                        final_df = temp_df.groupby([i], as_index=False).sum()
                        final_df["Placed"] = final_df['Placed'].apply(
                            lambda x: round((x/final_df["Placed"].sum())*100, 2))
                    
                        #---------------------------------If we have more than 5 columns then only show top 5 columns------------------------------------#
                        if len(final_df) > 5:
                            counts = final_df.sort_values(by="Placed",ascending=False)
                            graph_df=counts.drop_duplicates(subset=['Placed'])[:5]
                            #------------------MAke to show two graphs in two columns-------------------#
                            num_categories = len(graph_df[i])
                            colors = ['hsl(' + str(h) + ',50%' + ',50%)' for h in [round(h *
                                                                                        360 / num_categories) for h in range(num_categories)]]
                            #-----------------Draw bar graph----------------------------#
                            bar = go.Figure(
                                go.Bar(x=graph_df[i], y=graph_df['Placed'], marker=dict(color=colors)))
                            bar.update_yaxes(title="percentage")
                            bar.update_layout(
                                yaxis=dict(
                                title="Percentage",
                                range=[0, graph_df['Placed'].max()]
                                ),
                                xaxis=dict(
                                title=f"{i}"
                                )
                            )
                            bar.update_traces(text=graph_df['Placed'].apply(
                                lambda x: round((x/graph_df["Placed"].sum())*100, 2)), textposition='auto')
                            #-----------Draw doughnt chart-------------------------------#
                            pie = go.Figure(go.Pie(labels=graph_df[i], values=graph_df['Placed'], hole=.5, marker=dict(
                                colors=colors), textposition='inside'))
                            pie.update_layout(width=800, height=500)
                            # display the chart
                            st.warning(f"These are the prediction of top five {i}. To get full insights please download charts")
                            st.plotly_chart(bar,use_container_width=True)
                            st.plotly_chart(pie,use_container_width=True)
                            #------------------------------Call the function get graph to get complete graph while downloading---------------------------#
                            bar,pie=get_graph(final_df,i,colors)
                            image_bytes_download_bargt5 = pio.to_image(bar, format="png")
                            st.download_button(label="Download Bar Graph as PNG", data=image_bytes_download_bargt5, file_name=f"{i}_bar_graph.png", mime="image/png")
                            image_bytes_download_donutgt5 = pio.to_image(pie, format="png")
                            st.download_button(label="Download Donut Graph as PNG", data=image_bytes_download_donutgt5, file_name=f"{i}_donut_graph.png", mime="image/png")
                            
 
                            

                        #--------------------------------------If we less than five columns---------------------------#
                        else:   
                            #------------------MAke to show two graphs in two columns-------------------#
                            num_categories = len(final_df[i])
                            colors = ['hsl(' + str(h) + ',50%' + ',50%)' for h in [round(h *
                                                                                        360 / num_categories) for h in range(num_categories)]]
                            #-----------------Draw bar graph----------------------------#
                            bar = go.Figure(
                                go.Bar(x=final_df[i], y=final_df['Placed'], marker=dict(color=colors)))
                            bar.update_yaxes(title="percentage")
                            bar.update_layout(
                                yaxis=dict(
                                title="Percentage",
                                range=[0, final_df['Placed'].max()]
                                ),
                                xaxis=dict(
                                    title=f"{i}"
                                )
                            )
                            bar.update_traces(text=final_df['Placed'].apply(
                                lambda x: round((x/final_df["Placed"].sum())*100, 2)), textposition='auto')
                            #-----------Draw doughnt chart-------------------------------#
                            pie = go.Figure(go.Pie(labels=final_df[i], values=final_df['Placed'], hole=.5, marker=dict(
                                colors=colors), textposition='inside'))
                            pie.update_layout(width=800, height=500)
                            # display the chart
                            
                            st.plotly_chart(bar,use_container_width=True)
                            st.plotly_chart(pie,use_container_width=True)

                            #----------------------Download graph-------------------------#
                            image_bytes_download_barlt5 = pio.to_image(bar, format="png")
                            st.download_button(label="Download Bar Graph as PNG", data=image_bytes_download_barlt5, file_name=f"{i}_bar_graph.png", mime="image/png")
                            image_bytes_download_donutlt5 = pio.to_image(pie, format="png")
                            st.download_button(label="Download Donut Graph as PNG", data=image_bytes_download_donutlt5, file_name=f"{i}_donut_graph.png", mime="image/png")
                
                    
            except ValueError as err:
                print(err) 
        else:
            st.header("Select the CSV file")
            