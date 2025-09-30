from ifs import *
import streamlit as st
import numpy as np

st.set_page_config(layout="wide")
st.header("Build-Your-Own IFS")

# Initialize an array to store the IFS transforms
IFS_transforms = []

# Initialize the session state
# IFS_latex: list of LaTeX strings for function display
# done: whether or not the user is finished editing the IFS
# function_form: whether or not the "Add function" form is currently open
# count: number of functions defined so far
# matrix_input: the current text string in the "Matrix" field
#               - used to preserve invalid input for editing after errors
# shift_input: stores the current text string in the "Shift" field
#               - same purpose as matrix_input
# form_error: stores the most recent error message when parsing inputs fails
# form_version: unique version counter for the form widgets
#               - incremented only on new form/reset to force fresh widget keys
#               - keeps widgets editable without Streamlit key conflicts
if "IFS_latex" not in st.session_state:
    st.session_state.IFS_latex = []
if "done" not in st.session_state:
    st.session_state.done = False
if "function_form" not in st.session_state:
    st.session_state.function_form = False
if "count" not in st.session_state:
    st.session_state.count = 0
if "matrix_input" not in st.session_state:
    st.session_state.matrix_input = "[[1,0],[0,1]]"
if "shift_input" not in st.session_state:
    st.session_state.shift_input = "[[0],[0]]"
if "form_error" not in st.session_state:
    st.session_state.form_error = ""
if "form_version" not in st.session_state:
    st.session_state.form_version = 0

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
                delete_index = i
else:
    st.write("*No functions defined.*")

# Perform function deletion
if delete_index is not None:
    st.session_state.IFS_latex.pop(delete_index)

    # Renumber remaining functions (update latex labels)
    for j, tex in enumerate(st.session_state.IFS_latex, start=1):
        st.session_state.IFS_latex[j - 1] = re.sub(r"^f_\d", f"f_{j}", tex)

    # Update count
    st.session_state.count = len(st.session_state.IFS_latex)
    st.rerun()

# Button to add a function
if not st.session_state.function_form and st.session_state.done is False:
    if st.button("+ Add function"):
        st.session_state.function_form = True
        st.session_state.form_version += 1
        st.rerun()

# Form to add a new function
if st.session_state.function_form:
    fv = st.session_state.form_version
    matrix_key = f"matrix_widget_{fv}"
    shift_key = f"shift_widget_{fv}"

    with st.form(key=f"ifs_form_{fv}"):
        matrix_str = st.text_input("Matrix (format: [[a,b],[c,d]]):", value=st.session_state.matrix_input, key=matrix_key)
        shift_str = st.text_input("Shift (format: [[a],[b]]):", value=st.session_state.shift_input, key=shift_key)

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Clear previous error (we set it again if something goes wrong)
            st.session_state.form_error = ""
            try:
                # Verify bracket structure
                if not matrix_bracket_ok(matrix_str):
                    raise ValueError("Matrix must include outer square brackets in the form [[a,b],[c,d]]. Example: [[1,0],[0,1]]")
                if not shift_bracket_ok(shift_str):
                    raise ValueError("Shift must include outer square brackets in the form [[a],[b]]. Example: [[0],[0]]")

                # Parse strings into numpy arrays
                matrix = str_to_numpy_array(matrix_str)
                shift = str_to_numpy_array(shift_str)

                # Validate matrix shape (expecting 2x2)
                if matrix.shape != (2, 2):
                    raise ValueError(f"Matrix must be shape (2,2) but got shape {matrix.shape}. Example: [[1,0],[0,1]]")

                # Validate shift shape (expecting 2x1)
                if shift.shape != (2, 1):
                    raise ValueError(f"Shift must be a column vector of shape (2,1) but got shape {shift.shape}. Example: [[0],[0]]")

                # Build the homogeneous transform
                transform = np.block([[matrix, shift], [np.zeros((1, 2)), np.ones((1, 1))]])
                tex_string = (
                    f"f_{st.session_state.count + 1}(x)="
                    f"{array_to_latex(matrix)}x + {array_to_latex(shift)}"
                )

                # Everything valid: record it
                IFS_transforms.append(transform)
                st.session_state.IFS_latex.append(tex_string)
                st.session_state.count += 1
                st.session_state.function_form = False

                # Reset stored defaults and bump form_version so next time we get fresh widget keys
                st.session_state.matrix_input = "[[1,0],[0,1]]"
                st.session_state.shift_input = "[[0],[0]]"
                st.session_state.form_error = ""
                st.session_state.form_version += 1

                st.rerun()

            except (ValueError, TypeError, IndexError) as e:
                # Preserve the user's last-typed strings so they remain visible and editable
                st.session_state.matrix_input = matrix_str
                st.session_state.shift_input = shift_str

                # Save and show a helpful error message
                st.session_state.form_error = str(e)
                st.error(
                    f"Error parsing form inputs: {st.session_state.form_error}\n\n"
                    "Expected formats: matrix `[[a,b],[c,d]]` (shape 2x2) and shift `[[a],[b]]` (shape 2x1)."
                )
                # keep the form open so the user can edit the previous text
                st.session_state.function_form = True

# If the form submission results in an error, show the Try again button
if st.session_state.function_form and st.session_state.form_error:
    if st.button("Try again"):
        st.session_state.form_error = ""
        st.rerun()

# Button to confirm the ifs
if st.session_state.count > 0 and not st.session_state.done:
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
        st.session_state.matrix_input = "[[1,0],[0,1]]"
        st.session_state.shift_input = "[[0],[0]]"
        st.session_state.form_error = ""
        st.session_state.form_version += 1
        st.rerun()

# Runs after the ifs is confirmed
if st.session_state.done:
    if st.session_state.count > 0:
        st.write("IFS done.  Start plotting.")
    else:
        st.write("*No functions.  Hit reset to try again.*")