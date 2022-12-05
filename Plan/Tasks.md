## TODO



### IFS Engine

- [x] Develop a list-based algorithm for handing the codespace

- [x] Develop a function to apply the IFS functions to a specified point, given an element of the code space (MH)

- [ ] Use list comprehension to create another function that does this for every code, and every polygon vertex (EK)

  **Next meeting: Dec. 4, 2022, 7:30PM MST, 9:30PM EST**

- [ ] Develop a function for plotting the attractor

  - [x] Choose a preliminary function for plotting
  
  - [x] Convert vertex coordinates to the appropriate format
  
  - [ ] Investigate which module/function is best for plotting polygons
  
    - [ ] Look into:
      - [ ] mathplotlib.transforms
      - [ ] mathplotlib.patches
      - [ ] mathplotlib.paths 
  
    For example, for the Sierpinski Gasket: 
  
    - path (patch?) p = triangle with given vertices
    - array of paths P = array of results of applying the IFS transforms to p
    - iteratively apply the IFS transforms to the array of paths P

### User Interface

- [ ] Create main notebook for user

- [ ] Set up a method for the user to specify the matrix transformations and shifts of the affine IFS

  

