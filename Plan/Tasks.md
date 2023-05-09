## TODO



### IFS Engine

- [x] Develop a list-based algorithm for handing the codespace

- [x] Develop a function to apply the IFS functions to a specified point, given an element of the code space (MH)

- [x] Use list comprehension to create another function that does this for every code, and every polygon vertex (EK)

- [x] Develop a function for plotting the attractor (what plotting options?)

  - [x] Choose a preliminary function for plotting
  
  - [x] Convert vertex coordinates to the appropriate format
  
  - [x] Investigate which module/function is best for plotting polygons
  
    - [x] Look into:
      - [x] mathplotlib.transforms
      - [x] mathplotlib.patches 
      - [x] mathplotlib.paths (we will primarily use .patches and .transforms)
  
  - [x] Investigate which module/function is best for plotting polygons (matplotlib)
  
    For example, for the Sierpinski Gasket: 
    
    - path (patch?) p = triangle with given vertices
    - array of paths P = array of results of applying the IFS transforms to p
    - iteratively apply the IFS transforms to the array of paths P
  
- [x] Create a full example (e.g. Sierpinski Gasket) using mathplotlib.patches, mathplotlib.transforms, and mathplotlib.artists.Artists.set_transform function to apply the transforms to the polygon

- [ ] Create an IFS object (EK)

- [ ] Create python script of functions to load into main (EK)

- [ ] Find a good way to store the IFS data for gallery of examples 

- [ ] Collect examples: https://larryriddle.agnesscott.org/ifs/ifs.htm

- [ ] What is the best way to organize the subplots?

### User Interface

- [ ] Create main notebook for user (for now)

- [ ] Look into streamlit: https://streamlit.io/ (EK, MH)

- [ ] Set up a method for the user to specify the matrix transformations and shifts of the affine IFS

  

