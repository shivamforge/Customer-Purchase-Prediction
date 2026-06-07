import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib

st.markdown("""
<style>
# .stButton > button {
#     background-color: #00ff88;
#     color: black;
#     border: none;
#     border-radius: 10px;
#     font-weight: bold;
#     box-shadow: 0 0 5px #00ff88,
#                 0 0 10px #00ff88,
#                 0 0 15px #00ff88;
#     transition: 0.3s;
# }
    .stButton > button {
    background-color: #00ff88;
    color: black;
    border-radius: 10px;
    font-weight: bold;
    box-shadow: 0 0 4px #00ff88;
}

.stButton > button:hover {
    box-shadow: 0 0 10px #00ff88,
                0 0 15px #00ff88,
                0 0 20px #00ff88;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

scaler = joblib.load("scaler.pkl")

# Load Model
loaded_model = load_model("customer_purchase_model.keras")

# Initialize StandardScaler
#scaler = StandardScaler()

# Title
st.title("🛒 Customer Purchase Prediction System")

st.markdown("""
Predict whether an online customer is likely to make a purchase
based on browsing behavior and session characteristics.
""")


#sidebar
with st.sidebar:
    st.header("About Project")

    st.write("""
    This application uses a trained Neural Network model
    to predict purchase probability of online shoppers. \n 
    🤖  Trained ANN Model \n
    ⚙️ TensorFlow/Keras  \n
    📊 17 Input Features \n
    🎯 Purchase Probability Output \n
    🛒 Online Shopper Behaviour Dataset \n 
    """)
  

# Month Encoding
month_map = {
    "Aug": 0,
    "Dec": 1,
    "Feb": 2,
    "Jul": 3,
    "June": 4,
    "Mar": 5,
    "May": 6,
    "Nov": 7,
    "Oct": 8,
    "Sep": 9
}

# Visitor Encoding
visitor_map = {
    "New_Visitor": 0,
    "Other": 1,
    "Returning_Visitor": 2
}

# Inputs

administrative = st.number_input(
    "Administrative Pages Visited",
    min_value=0,
    value=0
)

administrative_duration = st.number_input(
    "Time on Administrative Pages",
    min_value=0.0,
    value=0.0
)

informational = st.number_input(
    "Informational Pages Viewed",
    min_value=0,
    value=0
)

informational_duration = st.number_input(
    "Time on Informational Pages",
    min_value=0.0,
    value=0.0
)

product_related = st.number_input(
    "Product Pages Viewed",
    min_value=0,
    value=1
    
)

product_related_duration = st.number_input(
    "Time on Product Pages",
    min_value=0.0,
    value=0.0
)

bounce_rates = st.number_input(
    "Bounce Rate",
    min_value=0.0,
    value=0.0
)

exit_rates = st.number_input(
    "Exit Rate",
    min_value=0.0,
    value=0.0
)

page_values = st.number_input(
    "Page Value Score",
    min_value=0.0,
    value=0.0
)

special_day = st.slider(
    "Special Day Score",
    0.0,
    1.0,
    0.0
)

month = st.selectbox(
    "Month",
    list(month_map.keys())
)

operating_system = st.number_input(
    "Operating System",
    min_value=1,
    value=1
)

browser = st.number_input(
    "Browser",
    min_value=1,
    value=1
)

region = st.number_input(
    "Region",
    min_value=1,
    value=1
)

traffic_type = st.number_input(
    "Traffic Type",
    min_value=1,
    value=1
)

visitor_type = st.selectbox(
    "Visitor Type",
    list(visitor_map.keys())
)

weekend = st.selectbox(
    "Weekend Visit?",
    ["No", "Yes"]
)



# Predict Button
if st.button("🚀Predict Purchase"):

    input_data = np.array([[
        administrative,
        administrative_duration,
        informational,
        informational_duration,
        product_related,
        product_related_duration,
        bounce_rates,
        exit_rates,
        page_values,
        special_day,
        month_map[month],
        operating_system,
        browser,
        region,
        traffic_type,
        visitor_map[visitor_type],
        1 if weekend == "Yes" else 0
    ]])

    # st.write("Input Data:")

    input_data = scaler.transform(input_data)

    prediction = loaded_model.predict(input_data)

    st.progress(float(prediction[0][0]))


    probability = float(prediction[0][0])
    
    # st.write(prediction)
    # st.write(probability)
    # st.progress(probability)

    st.subheader(f"Purchase Probability: {probability*100:.2f}%")

    if probability < 0.3:
        st.error("Low Purchase Intent")

    elif probability < 0.7:
        st.warning("Moderate Purchase Intent")

    else:
        st.success("High Purchase Intent")

    # if probability >= 0.5:
    #     st.success("✅ Likely To Purchase")
    # else:
    #     st.error("❌ Unlikely To Purchase")


st.markdown("---")
st.write("Model: Artificial Neural Network (ANN)")
st.write("Framework: TensorFlow/Keras")
st.write("Frontend: Streamlit")
