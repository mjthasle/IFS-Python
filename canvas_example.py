import io
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import streamlit as st
from threading import RLock

plot_lock = RLock()

st.set_page_config(layout="wide")
st.header("Drawing Canvas with Background and Polygon Plot")

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

# Only used as an initial fallback; real canvas size comes from the background 
# PNG.
canvas_dimension = 400

# Basic drawing canvas settings
drawing_mode = "polygon"
stroke_width = 3

# Coordinate limits for both the background grid and the right-hand plot
# Let's call this coordinate system the "world coordinates"
x_min, x_max = -1, 1
y_min, y_max = -1, 1

# ---------------------------------------------------------------------
# SESSION STATE 
# ---------------------------------------------------------------------
# polygon_coords      : list of (x, y) points from st_canvas (in image/canvas pixels)
# canvas_key          : used to force st_canvas to reset when "Clear" is pressed
# origin_canvas_coords: pixel coordinates of world-origin (0,0) in the background PNG
# canvas_size         : (width, height) of the PNG (and thus the drawable canvas)
# axes_bounds_img     : pixel bounds of the Matplotlib axes region inside the PNG
#                       (left, right, top, bottom) in image/canvas coordinates
st.session_state.setdefault("polygon_coords", None)
st.session_state.setdefault("canvas_key", 0)
st.session_state.setdefault("origin_canvas_coords", None)
st.session_state.setdefault("canvas_size", (canvas_dimension, canvas_dimension))
st.session_state.setdefault("axes_bounds_img", None)

# ---------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------

def extract_polygon_coords(path):
    """
    Extract (x, y) points from a canvas polygon 'path' as returned by st_canvas.

    The 'path' is a list of commands like:
        ["M", x0, y0], ["L", x1, y1], ...
    We keep only the M/L vertices.
    """
    coords = []
    if not isinstance(path, list):
        return coords
    for segment in path:
        if not segment:
            continue
        cmd = segment[0]
        if cmd in ("M", "L") and len(segment) >= 3:
            coords.append((segment[1], segment[2]))
    return coords


def canvas_to_world(x_c, y_c, axes_bounds, dx, dy):
    """
    Map canvas/image pixel coordinates (origin top-left) to world coordinates
    (x_min..x_max, y_min..y_max), using the true axes rectangle inside the PNG.

    axes_bounds = (axes_left_img, axes_right_img, axes_top_img, axes_bottom_img),
    all expressed in image/canvas pixel coordinates.
    """
    if axes_bounds is None:
        return None, None

    axes_left_img, axes_right_img, axes_top_img, axes_bottom_img = axes_bounds

    # Horizontal mapping: left -> right
    # x_c == axes_left_img  -> x_w == x_min
    # x_c == axes_right_img -> x_w == x_max
    t_x = (x_c - axes_left_img) / (axes_right_img - axes_left_img)
    x_w = x_min + t_x * dx

    # Vertical mapping: top -> bottom in image vs bottom -> top in world
    # y_c == axes_top_img    -> y_w == y_max
    # y_c == axes_bottom_img -> y_w == y_min
    t_y = (y_c - axes_top_img) / (axes_bottom_img - axes_top_img)
    y_w = y_max - t_y * dy

    return x_w, y_w


# ---------------------------------------------------------------------
# LAYOUT
# ---------------------------------------------------------------------

col1, col2 = st.columns(2, gap="medium")

# =====================================================================
# LEFT COLUMN: DRAWING CANVAS WITH BACKGROUND GRID
# =====================================================================
with col1:
    st.subheader("Draw initial polygon")

    stroke_color = st.color_picker("Select a colour for the polygon:", "#000000")

    # Clear button: reset polygon + origin + canvas widget key
    if st.button("Clear drawing"):
        st.session_state["polygon_coords"] = None
        st.session_state["origin_canvas_coords"] = None
        st.session_state["axes_bounds_img"] = None
        st.session_state["canvas_key"] += 1

    # -----------------------------------------------------------------
    # 1. Build background figure: world grid + red dot at (0,0)
    # -----------------------------------------------------------------
    fig, ax = plt.subplots()
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal")

    # Leave some room for ticks/labels, but keep axes fairly large
    fig.subplots_adjust(left=0, right=0.95, bottom=0.1, top=0.95)

    ax.grid(alpha=0.75)
    ax.plot(0, 0, marker="o", markersize=6, color="red")  # world origin marker

    # -----------------------------------------------------------------
    # 2. Compute origin + axes bounds in FIGURE pixel coordinates
    # -----------------------------------------------------------------
    fig.canvas.draw()

    # (0,0) in world coords -> (x_fig_px, y_fig_px) in figure pixels
    x_fig_px, y_fig_px = ax.transData.transform((0, 0))
    fig_w_px, fig_h_px = fig.canvas.get_width_height()

    # Axes rectangle (in figure-relative 0..1 coords) -> figure pixels
    pos = ax.get_position()   # Bbox in figure coordinates (0..1)
    axes_left_fig   = pos.x0 * fig_w_px
    axes_right_fig  = pos.x1 * fig_w_px
    axes_bottom_fig = pos.y0 * fig_h_px
    axes_top_fig    = pos.y1 * fig_h_px

    # -----------------------------------------------------------------
    # 3. Save figure to PNG and read its actual pixel size
    # -----------------------------------------------------------------
    img_buf = io.BytesIO()
    with plot_lock:
        fig.savefig(img_buf, format="png", dpi=80, pad_inches=0)
    img_buf.seek(0)
    pil_img = Image.open(img_buf)

    # This (width, height) is the coordinate system used by st_canvas.
    img_w_px, img_h_px = pil_img.size
    canvas_width, canvas_height = img_w_px, img_h_px
    st.session_state["canvas_size"] = (canvas_width, canvas_height)

    # -----------------------------------------------------------------
    # 4. Map FIGURE pixels -> IMAGE/CANVAS pixels
    # -----------------------------------------------------------------
    scale_x_img = img_w_px / fig_w_px
    scale_y_img = img_h_px / fig_h_px

    # World origin (0,0) in IMAGE/CANVAS pixel coords (origin top-left)
    x_canvas_origin = x_fig_px * scale_x_img
    y_canvas_origin = (fig_h_px - y_fig_px) * scale_y_img
    st.session_state["origin_canvas_coords"] = (x_canvas_origin, y_canvas_origin)

    # Axes bounds in IMAGE/CANVAS pixel coords
    axes_left_img   = axes_left_fig * scale_x_img
    axes_right_img  = axes_right_fig * scale_x_img
    axes_top_img    = (fig_h_px - axes_top_fig) * scale_y_img
    axes_bottom_img = (fig_h_px - axes_bottom_fig) * scale_y_img

    st.session_state["axes_bounds_img"] = (
        axes_left_img,
        axes_right_img,
        axes_top_img,
        axes_bottom_img,
    )

    # -----------------------------------------------------------------
    # 5. Create the Streamlit drawable canvas with the PNG as background
    # -----------------------------------------------------------------
    canvas_result = st_canvas(
        fill_color=stroke_color,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color="#eee",
        background_image=pil_img,
        update_streamlit=True,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        point_display_radius=0,
        display_toolbar=True,
        key=f"canvas_{st.session_state['canvas_key']}",
    )
    img_buf.close()

    # -----------------------------------------------------------------
    # 6. Extract the first polygon drawn on the canvas (if any)
    # -----------------------------------------------------------------
    if canvas_result is not None and canvas_result.json_data is not None:
        objects = pd.json_normalize(canvas_result.json_data["objects"])
        if len(objects) > 0:
            # Only use the first polygon; ignore additional ones
            path = objects.loc[0, "path"]
            coords = extract_polygon_coords(path)
            if coords:
                st.session_state["polygon_coords"] = coords


# =====================================================================
# RIGHT COLUMN: WORLD-COORDINATE PLOT OF THE DRAWN POLYGON
# =====================================================================
with col2:
    st.subheader("Matplotlib plot of the drawn polygon")

    fig2, ax2 = plt.subplots()
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(y_min, y_max)
    ax2.set_aspect("equal")
    ax2.grid(True, alpha=0.75)

    # World-range lengths
    dx = x_max - x_min
    dy = y_max - y_min

    # Pixel bounds of the axes region in the PNG (image/canvas coords)
    axes_bounds = st.session_state["axes_bounds_img"]

    # -----------------------------------------------------------------
    # 1. Plot the world origin (red dot) as inferred from the background
    # -----------------------------------------------------------------
    origin_canvas = st.session_state["origin_canvas_coords"]
    x_plot = y_plot = None
    if origin_canvas is not None and axes_bounds is not None:
        x_c, y_c = origin_canvas
        x_plot, y_plot = canvas_to_world(x_c, y_c, axes_bounds, dx, dy)

    if x_plot is not None and y_plot is not None:
        ax2.plot(
            x_plot,
            y_plot,
            marker="o",
            markersize=6,
            color="red",
            clip_on=False,
        )

    # -----------------------------------------------------------------
    # 2. Map the drawn polygon from canvas pixels -> world coordinates
    # -----------------------------------------------------------------
    coords = st.session_state["polygon_coords"]

    if coords and axes_bounds is not None:
        xs_canvas, ys_canvas = zip(*coords)

        xs_world = []
        ys_world = []

        for x_c, y_c in zip(xs_canvas, ys_canvas):
            x_w, y_w = canvas_to_world(x_c, y_c, axes_bounds, dx, dy)
            xs_world.append(x_w)
            ys_world.append(y_w)

        # Draw polygon in world coordinates, matching background placement
        ax2.plot(xs_world, ys_world, marker="o", color="blue")
        ax2.plot(
            [xs_world[-1], xs_world[0]],
            [ys_world[-1], ys_world[0]],
            color="blue",
        )

    # Render the right-hand plot
    with plot_lock:
        st.pyplot(fig2)