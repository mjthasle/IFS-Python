from ifs import *
import operator
import time
from typing import Callable
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.colored_header import ST_COLOR_PALETTE


BLANK_COLUMNS_CONFIG = {i: {"title": ""} for i in range(4)}


def color_mask(x: pd.DataFrame, mask: pd.DataFrame, background_color: str) -> pd.DataFrame:
    hue, intensity = background_color.split("-")
    color = f"background-color: {ST_COLOR_PALETTE[hue][intensity]}; color:white;"
    style_df = pd.DataFrame("", index=x.index, columns=x.columns)
    style_df[mask] = color
    return style_df

def operation_interface(
    operation_label: str,
    operation_method: Callable,
    background_color: str,
    key_prefix: str,
) -> None:
    a, operation, b, equals, c = st.columns((10, 1, 10, 1, 10))

    with a:
        st.caption("A")
        A = st.data_editor(
            np.array([[0, 0, 2], [1, 3, 4], [3, 4, 4]]),
            use_container_width=True, hide_index=False,
            key=f"{key_prefix}_A",
        )

    with operation:
        add_vertical_space(6)
        st.write(f"###  {operation_label} ")

    with b:
        st.caption("B")
        B = st.data_editor(
            np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
            use_container_width=True, hide_index=False,
            key=f"{key_prefix}_B",
        )

    with equals:
        add_vertical_space(6)
        st.write("###  = ")

    with c:
        st.caption("C")
        C = pd.DataFrame(operation_method(A, B))

        key_C = f"{key_prefix}_C"
        avoid_coloring = False
        if key_C not in st.session_state:
            st.session_state[key_C] = C
            avoid_coloring = True

        result_df_container = st.empty()
        mask = (C - st.session_state[key_C]) != 0
        result_df_container.dataframe(
            C.style.apply(
                lambda x: color_mask(
                    x,
                    mask=mask,
                    background_color=background_color,
                ),
                axis=None,
            ),
            use_container_width=True,
        )

        if mask.sum().sum() > 0 and not avoid_coloring:
            time.sleep(0.5)
            result_df_container.dataframe(C, use_container_width=True)

        st.session_state[key_C] = C

    add_vertical_space(2)




operation_interface(
    "\+",
    operation_method=operator.__add__,
    background_color="green-80",
    key_prefix="sum"
)


st.header("Build-Your-Own IFS")

"""Add some description here..."""

k=1

def do_on_click(k):
	st.latex(f"f_{k}(x) = ")
	k=k+1

if st.button(r"\+ Add Function"):
	do_on_click(k)
