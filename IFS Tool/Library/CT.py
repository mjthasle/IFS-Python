# --------------------------------
# Cantor Ternary Set IFS
#
# Created by: Emily Rose Korfanty
# Last updated: 2022-02-20
#---------------------------------

# define the IFS
def F(i,x):
    '''
    Insert docstring here
    '''
    if i==1:
        y = (1/3)*x          
    elif i==2:
        y = (1/3)*x + 2/3   
        
    return y

