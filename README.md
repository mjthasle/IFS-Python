# IFS-Python

A streamlit app for generating fractal images using  2D affine iterated function systems.

**App URL**:
[https://ifs-python.streamlit.app/](https://ifs-python.streamlit.app/)


**What is an affine IFS?**

Generally speaking, an [iterated function system (IFS)](https://en.wikipedia.org/wiki/Iterated_function_system) is a collection of *contractive* functions.  In two dimensions, an **affine IFS** is a collection of functions of the form $f(x) = Ax + b$, where $A$ is a 2-by-2 matrix, and $b$ is a constant vector.  In this case, *contractive* means that the length of the vector $f(x)$ is always less than the length of $x$.


**App Details:**

For each built-in IFS, the system is iteratively applied to an initial polygon.  For the included examples, this process generates a fractal images.  By default, the first several iterations are shown.  You can also get a more detailed view of any given step in the iteration process by turning off the "Multiplot" toggle.  Currently, the following built-in IFS are available:

- Cantor Ternary Set
- Fudgeflake
- Sierpinski Gasket
- Twindragon.

**Coming soon:**

- Select your own polygon colour
- Generate a random IFS
- Build your own IFS
