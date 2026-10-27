import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score

st.set_page_config(page_title="ML Dashboard", layout="wide")
st.title("Machine Learning Project Dashboard")
st.write("Upload clean data, explore features, train models, and analyze performance.")

uploaded_file = st.file_uploader("Upload Clean CSV Dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.header("1. Dataset Exploration")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Data Preview")
        st.dataframe(df.head(10))
        
    with col2:
        st.subheader("Dataset Summary")
        st.write(f"Total Rows: **{df.shape[0]}**")
        st.write(f"Total Columns: **{df.shape[1]}**")
        st.write("Data Types:")
        st.write(df.dtypes.astype(str))

    st.header("2. Quick Data Visualization")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Select X-Axis Feature", numeric_cols, index=0)
        y_axis = st.selectbox("Select Y-Axis Feature", numeric_cols, index=min(1, len(numeric_cols)-1))
        
        chart_type = st.radio("Select Chart Type", ["Scatter Plot", "Line Chart", "Bar Chart"])
        
        if chart_type == "Scatter Plot":
            st.scatter_chart(df[[x_axis, y_axis]], x=x_axis, y=y_axis)
        elif chart_type == "Line Chart":
            st.line_chart(df[[x_axis, y_axis]].set_index(x_axis))
        elif chart_type == "Bar Chart":
            st.bar_chart(df[[x_axis, y_axis]].set_index(x_axis))
    else:
        st.warning("Need at least 2 numerical columns for visualization charts.")

    st.header("3. Model Training Engine")
    all_cols = df.columns.tolist()
    
    target_var = st.selectbox("Select Target Variable (Y) to Predict", all_cols)
    feature_vars = st.multiselect("Select Feature Variables (X) to Train On", [c for c in all_cols if c != target_var])
    
    if feature_vars:
        task_type = st.radio("Select Machine Learning Task", ["Classification (Categorical Target)", "Regression (Continuous Numbers)"])
        test_size = st.slider("Test Dataset Split Ratio (%)", 10, 50, 20) / 100.0
        
        if st.button("Train Model Now", type="primary"):
            X = df[feature_vars]
            y = df[target_var]
            
            X = pd.get_dummies(X, drop_first=True)
            if y.dtype == 'object' and task_type == "Regression (Continuous Numbers)":
                st.error("Cannot run regression on text/categorical target variables.")
            else:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                
                if task_type == "Classification (Categorical Target)":
                    model = RandomForestClassifier(random_state=42)
                    model.fit(X_train, y_train)
                    preds = model.predict(X_test)
                    acc = accuracy_score(y_test, preds)
                    st.metric(label="Model Accuracy Score", value=f"{acc:.2%}")
                    
                else:
                    model = RandomForestRegressor(random_state=42)
                    model.fit(X_train, y_train)
                    preds = model.predict(X_test)
                    r2 = r2_score(y_test, preds)
                    mse = mean_squared_error(y_test, preds)
                    
                    m_col1, m_col2 = st.columns(2)
                    m_col1.metric(label="R² Score (Variance Explained)", value=f"{r2:.4f}")
                    m_col2.metric(label="Mean Squared Error (MSE)", value=f"{mse:.4f}")
                    
                st.success("Model trained successfully on your computer.")
