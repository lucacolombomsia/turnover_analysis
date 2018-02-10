def preprocess(a_orig):
    """
    Preprocesses the data -inputted by the user - that was read from the form in the flask app.
    The model was fit using scikit learn, so categorical variables need to be transformed into dummies
    for the user input to be used for prediction.
    The output of this function contains all necessary dummies, so it can be used for prediction.

    Args:
        a_orig (list): A list with the user input read from the form.

    Returns:
        list: A list with the processed data.
    """
    #define dictionaries that will be used to create dummies
    bin_dict = {"Yes" : 1, "No" : 0}
    dept_dict = {"HR" : 7,
                 "IT" : 8,
                 "Management" : 9,
                 "Marketing" : 10,
                 "Product management" : 11,
                 "R&D" : 12,
                 "Sales" : 13,
                 "Support" : 14,
                 "Technical" : 15}
    salary_dict = {"Low" : 16,
                   "Medium" : 17}
    
    #keep only the first 7 elements (5 numerical variables + 2 binary variables)
    a = a_orig[0:7]
    #use bin_dict to code the binary variables as 0 or 1
    a[5] = bin_dict[a[5]]
    a[6] = bin_dict[a[6]]
    #there are 10 possible categories (9 dummies) for the "department" variable
    #there are 3 possibile categories (2 dummies) for the "salary" variable
    #in total, 11 dummies ==> add 11 zeros, then will use dictionary to change the relevant dummy to 1
    a = a + [0]*11
    #Accounting is the reference category, so no dummy for it (to avoid perfect multicollinearity)
    if (a_orig[7]!="Accounting"):
        a[dept_dict[a_orig[7]]] = 1
    #High is the reference category, so no dummy for it (to avoid perfect multicollinearity)
    if (a_orig[8]!="High"):
        a[salary_dict[a_orig[8]]] = 1
    return a
