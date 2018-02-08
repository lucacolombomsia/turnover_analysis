def preprocess(a_orig):
    """
    Preprocesses the user input that was inputted in the form in the flask app.
    The output contains all the dummies that are needed for the data to be used for prediction.

    Args:
        a_orig (list): A list with the user input read from the form.

    Returns:
        list: A list with the processed data.
    """
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
    
    a = a_orig[0:7]
    a[5] = bin_dict[a[5]]
    a[6] = bin_dict[a[6]]
    a = a + [0]*11
    if (a_orig[7]!="Accounting"):
        a[dept_dict[a_orig[7]]] = 1
    if (a_orig[8]!="High"):
        a[salary_dict[a_orig[8]]] = 1
    return a
