import streamlit as st


from SQLTOTEXT import Bot

tab1, tab2 = st.tabs(["🗃 DaTaBoT","📈 files" ])
#modevar
#model=Bot(mode=2)
mode1 = 0
def change_mode(selected_mode):
    global mode1
    if selected_mode == "Interactive Mode":
        mode1 = 0
    elif selected_mode == "Super Mode":
        mode1 = 2
    elif selected_mode == "Analytic Mode":
        st.write('I am still in developement(BETA_MODE)')
selected_mode = st.sidebar.selectbox("Select Mode", ["Interactive Mode", "Super Mode", "Analytic Mode"])
change_mode(selected_mode)
model = Bot(mode=mode1)
modes=['normal_mode','analytics_mode','english_qprompt']
model.db="hr.db"
file_output=False
## Add background image

tab1.title("DaTaBoT")
#st.sidebar.info("Welcome")
#st.sidebar.button("Interactive Mode")
#st.sidebar.button("Super Mode")
#st.sidebar.button("Analytic Mode")




container_output = tab1.container(border=True,height=240)
# Define markdown with colored characters for each half

    
  
  


    
question=tab1.text_area("Enter the query",height=10,max_chars=200)

submit=tab1.button("Submit")

    
    # if submit is clicked
if submit:
    display_text=model.eng_response(question)
    container_output.write(display_text)
if model.cache_data is not None and model.mode==2:
    file_output=True
if file_output:
    tab2.write("Here is the file associated with data")
    tab2.write(model.cache_data)
else:
    tab2.write("No files requested")    