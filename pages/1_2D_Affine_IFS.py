
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

st.latex("f_i(x) = A_i x + b_i \\quad \\text{for all } x \\in \\mathbb{R}^2,")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
&emsp;&emsp;where $A_i$ is a $2 \\times 2$ matrix and $b_i$ is a vector in $\\mathbb{R}^2$.

2. Each $f_i$ is *contractive*, meaning that it satisfies
""", unsafe_allow_html=True)

st.markdown("<div style='padding-left: 2em;'>", unsafe_allow_html=True)

st.latex("\\|f_i(x) - f_i(y)\\| \\leq c_i \\|x - y\\|  \\quad \\text{for all } x \\in \\mathbb{R}^2,")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
&emsp;&emsp;for some constant $c_i$ with $0 \\leq c_i < 1$.""")
