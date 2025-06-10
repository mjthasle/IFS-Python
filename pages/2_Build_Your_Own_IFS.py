from ifs import *

col1, col2 = st.columns(2, gap = "large", vertical_alignment = "bottom")

# build-your-own settings in the left column
with col1:

	st.header("Build-Your-Own IFS")

	common_transforms = st.toggle("Common Transforms", value = False)

	if common_transforms:
		st.write("Coming soon!")

	if col1.button("Random IFS"):
		st.write("Coming soon!")

# plot the attractor in the right column
with col2:
	if common_transforms:
		st.write("Coming soon!")
