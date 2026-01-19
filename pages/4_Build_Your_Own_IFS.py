from ifs import *
import pandas as pd
from matplotlib.transforms import Affine2D
from streamlit_drawable_canvas import st_canvas
from threading import RLock
import time

st.set_page_config(layout="wide")

st.header("Build-Your-Own IFS")

# === Session State Preamble ===================================================
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
if "set_lim_toggle" not in st.session_state:
    st.session_state.set_lim_toggle = st.session_state.set_lim
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
if "plot_image" not in st.session_state:
    st.session_state.plot_image = None
if "generate_plots" not in st.session_state:
    st.session_state.generate_plots = False  
if "show_plots" not in st.session_state:
    st.session_state.show_plots = False  
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None
if "n" not in st.session_state:
    st.session_state.n = 0
if "auto_lim" not in st.session_state:
    st.session_state.auto_lim = None
if "draw_polygon" not in st.session_state:
    st.session_state.draw_polygon = False
if "draw_polygon_form" not in st.session_state:
    st.session_state.draw_polygon_form = False
if "canvas_result" not in st.session_state:
    st.session_state.canvas_result = None
if "gridlines" not in st.session_state:
    st.session_state.gridlines = True

# === Add/delete IFS functions =================================================

# Display IFS LaTeX
st.write("### Define your IFS:")


# Fragment containing buttons for adding IFS:
@st.fragment
def ifs_function_area():

    # Index of function to be duplicated/delted
    duplicate_index = None
    delete_index = None

    if st.session_state.count > 0:
        for i, tex in enumerate(st.session_state.IFS_latex):
            col1, col2, col3, col4 = st.columns([8, 1, 1.5, 1])
            with col1:
                st.latex(tex)
            if not st.session_state.done:
                with col2:
                    if st.button("Edit", key=f"edit_{i}"):
                        st.session_state.edit_index = i
                with col3:
                    if st.button("Duplicate", key=f"duplicate_{i}"):
                        duplicate_index = i
                with col4:
                    if st.button("Delete", key=f"delete_{i}"):
                        delete_index = i
    else:
        st.write("*No functions defined.*")

    # Open form to edit function
    if st.session_state.edit_index is not None:
        form_strings = affine_to_strings(
            st.session_state.IFS_transforms[st.session_state.edit_index])
        st.session_state.matrix_input = form_strings[0]
        st.session_state.shift_input = form_strings[1]
        st.session_state.function_form = True

    # Perform function duplication
    if duplicate_index is not None:
        st.session_state.IFS_latex.insert(duplicate_index+1,
            st.session_state.IFS_latex[duplicate_index])
        st.session_state.IFS_transforms.insert(duplicate_index+1,
            st.session_state.IFS_transforms[duplicate_index])
        for j, tex in enumerate(st.session_state.IFS_latex[duplicate_index+1: ], 
            start=duplicate_index+1):
            (duplicate_index)
            st.session_state.IFS_latex[j] = re.sub(r"^f_\d", f"f_{j+1}", tex)
        st.session_state.count = len(st.session_state.IFS_latex)
        st.rerun() # Needed to refresh the IFS list

    # Perform function deletion
    if delete_index is not None:
        st.session_state.IFS_latex.pop(delete_index)
        st.session_state.IFS_transforms.pop(delete_index)
        # Renumber remaining functions
        for j, tex in enumerate(st.session_state.IFS_latex, start=1):
            st.session_state.IFS_latex[j - 1] = re.sub(r"^f_\d", f"f_{j}", tex)
        st.session_state.count = len(st.session_state.IFS_latex)
        st.rerun() # Needed to refresh the IFS list

    # Add function button
    if not st.session_state.function_form and not st.session_state.done:
        if st.button("+ Add function"):
            st.session_state.function_form = True
            st.session_state.form_version += 1

    # Function form
    if st.session_state.function_form:
        st.session_state.generate_plots = False
        fv = st.session_state.form_version
        matrix_key = f"matrix_widget_{fv}"
        shift_key = f"shift_widget_{fv}"
        with st.form(key=f"ifs_form_{fv}"):
            matrix_str = st.text_input("Matrix (format: [[a,b],[c,d]]):",
                                       value=st.session_state.matrix_input,
                                       key=matrix_key)
            shift_str = st.text_input("Shift (format: [[a],[b]]):",
                                      value=st.session_state.shift_input,
                                      key=shift_key)
            if st.form_submit_button("Submit"):
                st.session_state.form_error = ""
                try:
                    if not matrix_bracket_ok(matrix_str):
                        raise ValueError("Matrix must include outer square \
                            brackets.")
                    if not shift_bracket_ok(shift_str):
                        raise ValueError("Shift must include outer square \
                            brackets.")
                    matrix = str_to_numpy_array(matrix_str)
                    shift = str_to_numpy_array(shift_str)
                    if matrix.shape != (2,2):
                        raise ValueError("Matrix must be 2x2.")
                    if shift.shape != (2,1):
                        raise ValueError("Shift must be 2x1.")
                    transform = np.block([[matrix, shift], 
                        [np.zeros((1,2)), np.ones((1,1))]])
                    if st.session_state.edit_index is None:
                        tex_string = f"f_{st.session_state.count+1}(x)= \
                            {array_to_latex(matrix)}x + {array_to_latex(shift)}"
                        st.session_state.IFS_transforms.append(Affine2D(transform))
                        st.session_state.IFS_latex.append(tex_string)
                        st.session_state.count += 1
                    else:
                        tex_string = f"f_{st.session_state.edit_index+1}(x)= \
                            {array_to_latex(matrix)}x + {array_to_latex(shift)}"
                        st.session_state.IFS_transforms[st.session_state.edit_index]\
                            = Affine2D(transform)
                        st.session_state.IFS_latex[st.session_state.edit_index] = \
                        tex_string
                        st.session_state.edit_index = None
                    st.session_state.function_form = False
                    st.session_state.matrix_input = "[[1,0],[0,1]]"
                    st.session_state.shift_input = "[[0],[0]]"
                    st.session_state.form_version += 1
                    st.rerun() # Needed to have the function form close on submit
                except (ValueError, TypeError, IndexError) as e:
                    st.session_state.matrix_input = matrix_str
                    st.session_state.shift_input = shift_str
                    st.session_state.form_error = str(e)
                    st.error(f"Error parsing form inputs: \
                        {st.session_state.form_error}")
                    st.session_state.function_form = True
        # Button to close the x and y limit form
        if st.button("Close form"):
            st.session_state.function_form = False
            st.session_state.edit_index = None
            st.rerun() # Needed to make form close when clicked

    # Try again button in case of error
    if st.session_state.function_form and st.session_state.form_error:
        if st.button("Try again"):
            st.session_state.form_error = ""
            st.rerun()  # Needed to make the try again button disappear when clicked

    # Edit button
    if st.session_state.done:
        if st.button("Edit functions"):
            st.session_state.done = False
            st.session_state.show_plots = False
            st.session_state.generate_plots = False 
            st.rerun() # Needed to re-enter edit mode 

    # Reset button
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
            st.session_state.generate_plots = False
            st.session_state.show_plots = False
            st.session_state.xlim = config['xlim_default']
            st.session_state.ylim = config['ylim_default']
            st.session_state.set_lim = False
            st.session_state.set_lim_form = False
            st.session_state.set_lim_toggle = False
            st.session_state.draw_polygon = False
            st.session_state.draw_polygon_form = False 
            st.session_state.drawing_canvas_toggle = False
            st.session_state.canvas_result = None
            st.rerun() # Needed to make the reset button disappear when clicked


    # Done button
    if st.session_state.count > 0 and not st.session_state.done:
        if st.button("Done"):
            st.session_state.done = True
            st.session_state.function_form = False
            st.session_state.show_plots = False
            st.session_state.generate_plots = False
            st.rerun() # Required to make the done botton disappear when clicked

    # IFS confirmed message
    if st.session_state.done:        
        if st.session_state.count > 0:
            st.write("IFS confirmed.")
        else:
            st.write("*No functions. Hit reset to try again.*")

ifs_function_area()

# === Left column plot settings ================================================

# Built-in initial sets
initial_set_options = config['initial_sets']

# Settings for the drawing canvas
drawing_mode = "polygon"
stroke_width = 3

# Create columns
col1, col2 = st.columns(2, gap = "medium")

# Define the attractor
a = attractor(IFS=st.session_state.IFS_transforms,
              grid=st.session_state.grid,
              xlim=st.session_state.xlim,
              ylim=st.session_state.ylim)
max_iterations = a.max_iterations

# Left column: controls 
with col1:
    st.write("### Plot Settings:")

    # Function to trigger plot generation 
    def trigger_plots():
        st.session_state.generate_plots = True
        #st.session_state.show_plots = True

    # Toggles
    multiplot = st.toggle("Multiplot", value=True, on_change=trigger_plots)
    st.toggle("Show grid", value=True, key="gridlines", on_change=trigger_plots)
    st.toggle("Draw initial polygon", key="draw_polygon", on_change=trigger_plots)
    set_lim_toggle = st.toggle("Manual x and y limits", key="set_lim_toggle")

    # Set manual x/y lim defaults to most recent auto x/y lim
    if st.session_state.auto_lim is not None:
        st.session_state.xlim = st.session_state.auto_lim
        st.session_state.ylim = st.session_state.auto_lim

    # Sync derived x and y lim state variables 
    if st.session_state.set_lim != st.session_state.set_lim_toggle:
        st.session_state.set_lim = st.session_state.set_lim_toggle

        # If user turns off manual limits, trigger automatic rescaling
        if not st.session_state.set_lim_toggle:
            st.session_state.generate_plots = True  
            st.session_state.show_plots = True    

    # Adjust font sizes
    if multiplot:
        plt.rcParams.update({'font.size': config['multiplot_font']})
        plt.rcParams['figure.figsize'] = config['multiplot_size']
    else:
        plt.rcParams.update({'font.size': config['singleplot_font']})
    stroke_color = st.color_picker("Select a colour for the attractor: ", 
                            colour_default)

    # Use a select box if not using the drawing canvas
    if not st.session_state.draw_polygon:
        initial_set_selected = st.selectbox("Select an initial set",
                                      initial_set_options.keys(),
                                      on_change=reset_n,
                                      index=get_default_index())

    # Use an input box for number of iterations when not multiplot
    if not multiplot:
        def update_n():
            st.session_state.generate_plots = True

        n = st.number_input(
            "Number of iterations:",
            min_value=0,
            max_value=max_iterations,
            step=1,
            key="n",
            on_change=update_n
        )

    # Draw polygon button
    if st.session_state.draw_polygon:
        if not st.session_state.draw_polygon_form:
            if st.button("Open inital polygon drawing canvas"):
                st.session_state.draw_polygon_form = True
    else:
        st.session_state.draw_polygon_form = False

    # Draw polygon form
    if st.session_state.draw_polygon and st.session_state.draw_polygon_form: 
        with st.form("drawing_canvas"):
            st.write("Draw the initial polygon here (only the first polygon\
                drawn on the canvas will be used:")
            form_canvas_result = st_canvas(
                fill_color=stroke_color,
                stroke_width=stroke_width,
                stroke_color=stroke_color,
                background_color="#eee",
                background_image=None,
                update_streamlit=True,
                height=canvas_dimension,
                width=canvas_dimension,
                drawing_mode=drawing_mode,
                point_display_radius=0,
                display_toolbar=True,
                key="full_app"
            )

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.canvas_result = form_canvas_result
                st.session_state.draw_polygon_form = False
                st.session_state.generate_plots = True
                st.rerun() # Needed to make canvas form disappear when submitted

        # Button to close the form
        if st.button("Close form"):
            st.session_state.draw_polygon_form = False
            st.rerun() # Needed to make canvas form disappear 

    # Prevent plotting when no canvas result exists
    if st.session_state.draw_polygon:
        if st.session_state.canvas_result is None:
            st.session_state.show_plots = False 


    # Use selected stroke colour
    colour_selected = stroke_color

    # Extract drawing canvas polygon coordinates
    if st.session_state.draw_polygon and st.session_state.canvas_result is not None:
        initial_polygon = st.session_state.canvas_result
        if initial_polygon.json_data is not None:
            objects = pd.json_normalize(initial_polygon.json_data["objects"])
            if len(objects) > 0:
                coordinates = objects["path"][0]
        
    # Set x and y limits button
    if st.session_state.set_lim_toggle:
        if not st.session_state.set_lim_form:
            if st.button("Set x and y limits"):
                st.session_state.set_lim_form = True
    else:
        st.session_state.set_lim_form = False

    # Manual x and y limits form
    if st.session_state.set_lim_toggle and st.session_state.set_lim_form: 
        with st.form("xylim"):
            st.write("Input the x limits [x1, x2]:")
            x1 = st.number_input("x1 = ", value=st.session_state.xlim[0])
            x2 = st.number_input("x2 = ", value=st.session_state.xlim[1])
            st.write("Input the y limits [y1, y2]:")
            y1 = st.number_input("y1 = ", value=st.session_state.ylim[0])
            y2 = st.number_input("y2 = ", value=st.session_state.ylim[1])

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                st.session_state.xlim = [x1, x2]
                st.session_state.ylim = [y1, y2]
                st.session_state.set_lim_form = False
                st.session_state.generate_plots = True
                st.rerun() # Needed to make limits form close when submitted

        # Button to close the x and y limit form
        if st.button("Close form"):
            st.session_state.set_lim_form = False
            st.rerun() # Needed to make form close when clicked

# Set xlim and ylim 
if st.session_state.set_lim:
    a.xlim = st.session_state.xlim
    a.ylim = st.session_state.ylim

# === Plot iterations ============================================

# Right column: attractor plots
with col2:
    # Plot iterations button
    # Only show if IFS functions are done and user has not plotted yet
    st.write("### Iteration Plots:")
    if st.session_state.done:
        if not st.session_state.show_plots:
            if st.button("Plot iterations"):
                st.session_state.generate_plots = True
                st.session_state.show_plots = True
    else:
        st.write("*IFS definition required - click **Done** to confirm your IFS*")

    if st.session_state.count > 0 and st.session_state.done and st.session_state.show_plots:
        # Determine initial points
        if st.session_state.draw_polygon:
            try:
                clicks = get_coordinates(coordinates)
            except (TypeError, KeyError, NameError):
                clicks = [[0, 0]]
        else:
            clicks = initial_set_options[initial_set_selected]
        # Generate multiplot/plot
        if st.session_state.generate_plots:
            if multiplot:
                st.session_state.plot_image = a.multiplot(
                    facecolor=colour_selected,
                    showgridlines=st.session_state.gridlines,
                    set_lim=st.session_state.set_lim_toggle,
                    clicks=clicks
                )
                st.session_state.generate_plots = False
                st.session_state.show_plots = True
                st.rerun() # Needed to refresh the plots
            else:
                plot_data = a.plot(
                    n=st.session_state.n,
                    facecolor=colour_selected,
                    set_lim=st.session_state.set_lim_toggle,
                    clicks=clicks, get_lim=True, 
                    showgridlines=st.session_state.gridlines
                )
                st.session_state.plot_image = plot_data[0]
                st.session_state.auto_lim = plot_data[1]
                st.session_state.generate_plots = False
                st.session_state.show_plots = True

        # Keep final plot displayed plot 
        if st.session_state.show_plots and \
            st.session_state.plot_image is not None:
            st.pyplot(st.session_state.plot_image)