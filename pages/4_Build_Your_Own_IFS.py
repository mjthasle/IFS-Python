from ifs import *

st.set_page_config(layout = "wide")

st.header("Build-Your-Own IFS")

import streamlit as st

# Initialize an array to store the IFS transforms
IFS_transforms = []

# Initialize the session state 
if "IFS_latex" not in st.session_state:
    st.session_state.IFS_latex = []
if "done" not in st.session_state:
    st.session_state.done = False
if "function_form" not in st.session_state:
    st.session_state.function_form = False
if "count" not in st.session_state:
    st.session_state.count = 0 

        
# Display the IFS latex 
st.write("### Your IFS:")

if st.session_state.IFS_latex:
    for i, tex_string in enumerate(st.session_state.IFS_latex, start=1):
        cols = st.columns([4, 1])
        with cols[0]:
            st.latex(tex_string)
        with cols[1]:
            if st.session_state.done == False:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.IFS_latex.pop(i-1)
                    st.rerun()
else:
    st.write("*No functions defined.*")

# Button to add a function
if not st.session_state.function_form and st.session_state.done == False:
    if st.button("\+ Add function"):
        st.session_state.function_form = True
        st.rerun()

# Form to add a new function
if st.session_state.function_form:
    with st.form(key="ifs_form"):
        matrix_str = st.text_input("Matrix:", "[[1,0],[0,1]]")
        shift_str = st.text_input("Shift", "[[0],[0]]")
        matrix = str_to_numpy_array(matrix_str)
        shift = str_to_numpy_array(shift_str)
        transform = np.block([[matrix,shift],[np.zeros((1,2)),np.ones((1,1))]])
        tex_string = f"f_{st.session_state.count+1}(x)=" + \
                     f"{array_to_latex(matrix)}x + {array_to_latex(shift)}"
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            if tex_string:
                IFS_transforms.append(transform)
                st.session_state.IFS_latex.append(tex_string)
                st.session_state.count += 1
                st.session_state.function_form = False
                st.rerun()

# Button to confirm the ifs
if st.session_state.count > 0 and not st.session_state.done :
    if st.button("Done"):
        st.session_state.done = True
        st.session_state.function_form = False
        st.rerun()

# Button to edit functions
if st.session_state.done:
    if st.button("Edit functions"):
        st.session_state.done = False
        st.rerun() 

# Button to reset
if st.session_state.count > 0:
    if st.button("Reset"):
        st.session_state.IFS_latex = []
        st.session_state.done = False
        st.session_state.function_form = False
        st.session_state.count = 0
        st.rerun()

# Runs after the ifs is confirmed
if st.session_state.done:
    if st.session_state.IFS_latex:
        st.write("IFS done.  Start plotting.")
    else:
        st.write("*No functions.  Hit reset to try again.*")
