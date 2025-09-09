from ifs import *
import re

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


# Track which function is deleted
delete_index = None
        
# Display the IFS latex 
st.write("### Your IFS:")
if st.session_state.count > 0:
    for i, tex in enumerate(st.session_state.IFS_latex):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.latex(tex)
        with col2:
            if st.button("Delete", key=f"delete_{i}"):
                # Mark the index to be deleted
                delete_index = i  
else:
    st.write("*No functions defined.*")

# Perform function deletion 
if delete_index is not None:
    st.session_state.IFS_latex.pop(delete_index)
    IFS_transforms.pop(delete_index)
 
    # Renumber remaining functions
    for j, tex in enumerate(st.session_state.IFS_latex, start = 1):
        st.session_state.IFS_latex[j-1] = re.sub("^f_\d", f"f_{j}", tex)
        print(st.session_state.IFS_latex)

    # Update count
    st.session_state.count = len(st.session_state.IFS_latex)

    st.rerun()  

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
    if st.session_state.count > 0:
        st.write("IFS done.  Start plotting.")
    else:
        st.write("*No functions.  Hit reset to try again.*")
