
import streamlit as st

st.header("What is a 2D affine IFS?")

st.markdown(r"""
A 2D affine iterated function system (IFS) is any finite collection of functions
""")

st.latex("\\mathcal{F} = \\{f_1, f_2, \\dots, f_m\\} \\, ,")

st.markdown(r"""
that has the following two properties:

1. Each $f_i$ is a *2D affine function*, meaning that it has the form
""")

st.markdown("<div style='padding-left: 2em;'>", unsafe_allow_html=True)

st.latex("f_i(\\vec{x}) = A_i \\vec{x} + \\vec{b_i} \\quad \\text{for all } \\vec{x} \\in \\mathbb{R}^2,")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
&emsp;&emsp;where $A_i$ is a $2 \\times 2$ matrix and $\\vec{b_i}$ is a vector in $\\mathbb{R}^2$.

2. Each $f_i$ is *contractive*, meaning that it satisfies
""", unsafe_allow_html=True)

st.markdown("<div style='padding-left: 2em;'>", unsafe_allow_html=True)

st.latex("\\|f_i(\\vec{x}) - f_i(\\vec{y})\\| \\leq c_i \\|\\vec{x} - \\vec{y}\\|  \\quad \\text{for all } \\vec{x} \\in \\mathbb{R}^2,")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
&emsp;&emsp;for some constant $c_i$ with $0 \\leq c_i < 1$. Here $\\|\\cdot\\|$ denotes the standard Euclidean norm on $\\mathbb{R}^2$.""")
