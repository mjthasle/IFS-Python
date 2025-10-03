from ifs import *
import pandas as pd
from matplotlib.transforms import Affine2D
from streamlit_drawable_canvas import st_canvas
from threading import RLock


st.set_page_config(layout="wide")

st.header("Build-Your-Own IFS")

st.write("Use the \"Add Function\" button to add functions to your IFS. \
    When you are finished addint functions to your IFS, click the \"Done\" \
    button.  After specifying the initial polygon, the result of iterating the \
    IFS will be displayed. No matter what polygon you start with, the results \
    approximate the IFS attractor as the number of iterations increases!")

st.write("Use the Multiplot toggle to change between views of individual \
    iterations and multiple iterations on the same canvas.")

# Initialize the session state
# IFS_latex: list of LaTeX strings for function display
# IFS_tansforms: list of Affine2D transforms specifying the IFS
# grid: number of rows/columns for multiplot
# xlim: x limits of plots
# ylim: y limits of plots
# set_lim: automatic xlim and ylim when false
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
if "IFS_transforms" not in st.session_state:
    st.session_state.IFS_transforms = []
if "grid" not in st.session_state:
    st.session_state.grid = config['grid_default']
if "xlim" not in st.session_state:
    st.session_state.xlim = config['xlim_default']
if "ylim" not in st.session_state:
    st.session_state.ylim = config['ylim_default']
if "set_lim" not in st.session_state:
    st.session_state.set_lim = False
if "set_lim_form" not in st.session_state:
    st.session_state.set_lim_form = False
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
if "start_plotting" not in st.session_state:
    st.session_state.start_plotting = False

# Get built-in initial set options
initial_set_options = config['initial_sets']

# Track which function is deleted
delete_index = None

# Display the IFS LaTeX
st.write("### Define your IFS:")
if st.session_state.count > 0:
    for i, tex in enumerate(st.session_state.IFS_latex):
        col1, col2 = st.columns([8, 1])
        with col1:
            st.latex(tex)
        with col2:
            if not st.session_state.done:
                if st.button("Delete", key=f"delete_{i}"):
                    delete_index = i
else:
    st.write("*No functions defined.*")


# Perform function deletion
if delete_index is not None:
    st.session_state.IFS_latex.pop(delete_index)
    st.session_state.IFS_transforms.pop(delete_index)

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
    st.session_state.start_plotting = False
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
                st.session_state.IFS_transforms.append(Affine2D(transform))
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
        st.session_state.start_plotting = False
        st.rerun()

# Button to edit functions
if st.session_state.done:
    if st.button("Edit functions"):
        st.session_state.done = False
        st.start_plotting = False
        st.rerun()

# Button to reset
if st.session_state.count > 0:
    if st.button("Reset"):
        st.session_state.IFS_latex = []
        st.session_state.IFS_transforms = []
        st.session_state.done = False
        st.session_state.function_form = False
        st.session_state.count = 0
        st.session_state.matrix_input = "[[1,0],[0,1]]"
        st.session_state.shift_input = "[[0],[0]]"
        st.session_state.form_error = ""
        st.session_state.form_version += 1
        st.session_state.start_plotting = False
        st.session_state.xlim = config['xlim_default']
        st.session_state.ylim = config['ylim_default']
        st.session_state.set_lim = False
        st.rerun()

# Runs after the ifs is confirmed
if st.session_state.done:
    if st.session_state.count > 0:
        st.write("IFS confirmed.")
    else:
        st.write("*No functions.  Hit reset to try again.*")

st.write("### Choose your plot settings:")

# Settings for the drawing canvas
drawing_mode = "polygon"
stroke_width = 3

# Display toggles
drawing_canvas = st.toggle("Draw initial polygon", value = False)
set_lim = st.toggle("Set x and y limits", value = False)
multiplot = st.toggle("Multiplot", value = True)
gridlines = st.toggle("Show grid", value = True)

# Adjust font sizes
if multiplot:
    plt.rcParams.update({'font.size': config['multiplot_font']})
    plt.rcParams['figure.figsize'] = config['multiplot_size']
else:
    plt.rcParams.update({'font.size': config['singleplot_font']})

# Create columns
col1, col2 = st.columns(2, gap = "medium")

# Define the attractor
a = attractor(IFS = st.session_state.IFS_transforms, 
            grid = st.session_state.grid, xlim = st.session_state.xlim, 
            ylim = st.session_state.ylim)
max_iterations = a.max_iterations

# IFS settings in the left column
with col1:
    stroke_color = st.color_picker("Select a colour for the attractor: ", colour_default)

    if not drawing_canvas:
        initial_set_selected = st.selectbox("Select an initial set",
                                      initial_set_options.keys(),
                                      on_change = reset_n,
                                      index = get_default_index())
    if not multiplot:
        n = st.number_input("Number of iterations: ", min_value = 0,
            max_value = max_iterations, step = 1, key = "n")
    if drawing_canvas:
        canvas_result = st_canvas(
            fill_color = stroke_color,
            stroke_width = stroke_width,
            stroke_color = stroke_color,
            background_color = "#eee",
            background_image = None,
            update_streamlit = True,
            height = canvas_dimension,
            width = canvas_dimension,
            drawing_mode = drawing_mode,
            point_display_radius = 0,
            display_toolbar = True,
            key = "full_app",
        )
    else:
        canvas_result = None
        colour_selected = stroke_color

    if canvas_result is not None:
        if canvas_result.json_data is not None:
            objects = pd.json_normalize(canvas_result.json_data["objects"])
            if len(objects) > 0:
                coordinates = objects["path"][0]

        colour_selected = stroke_color


    # Display xlim and ylim
    if set_lim:
        st.session_state.set_lim = True
        st.write(f"x limits: {st.session_state.xlim}")
        st.write(f"y limits: {st.session_state.ylim}")
    else:
        st.session_state.set_lim = False

    # Button to set xlim and ylim
    if not st.session_state.set_lim_form and set_lim:
        if st.button("Set x and y limits"):
            st.session_state.set_lim_form = True
            st.session_state.start_plotting = False
            st.rerun()

    # Form to add a new function
    if st.session_state.set_lim_form:
        with st.form("xylim"):
            st.write("Input the x limits [x1, x2]:")
            x1 = st.number_input("x1 = ", value=st.session_state.xlim[0])
            x2 = st.number_input("x2 = ", value=st.session_state.xlim[1])
            st.write("Input the y limits [y1, y2]:")
            y1 = st.number_input("y1 = ", value=st.session_state.ylim[0])
            y2 = st.number_input("y2 = ", value=st.session_state.ylim[1])

            submit_button = st.form_submit_button("Submit")

            if(submit_button):
                st.session_state.xlim[0] = x1
                st.session_state.xlim[1] = x2
                st.session_state.ylim[0] = y1
                st.session_state.ylim[1] = y2
                st.session_state.set_lim = True
                st.session_state.set_lim_form = False
                st.rerun()

    if(st.button("Plot iterations")):
        st.session_state.start_plotting = True
        st.rerun()

    if(st.session_state.start_plotting and not st.session_state.done):
        st.write("*No IFS defined - click **Done** to confirm your IFS*")


# set xlim and ylim 
if(st.session_state.set_lim == True):
    a.xlim = st.session_state.xlim
    a.ylim = st.session_state.ylim

# plot the attractor in the right column
with col2:
    # Runs after the ifs is confirmed and the start plotting button is clicked
    if st.session_state.done and st.session_state.start_plotting:
        if st.session_state.count > 0:
            if drawing_canvas:
                try:
                    clicks = get_coordinates(coordinates)
                except (TypeError, KeyError, NameError):
                    clicks = [[0, 0]]
            else:
                clicks = initial_set_options[initial_set_selected]
            _lock = RLock()
            with _lock:
                if multiplot:
                    a.multiplot(showgridlines = gridlines, 
                        set_lim = st.session_state.set_lim,
                        facecolor = colour_selected, clicks = clicks)
                else:
                    a.plot(n = n, showgridlines = gridlines, 
                        set_lim = st.session_state.set_lim, 
                        facecolor = colour_selected, clicks = clicks)


