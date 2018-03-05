# Turnover Analysis

## Project Charter
A high turnover rate can seriously impact our company’s ability to be successful, as it causes high monetary costs and losses of human capital. The goal of this project is to enable HR professionals and team managers to work conjunctly to retain the best talent. Our model will predict the likelihood that current employees will leave the company and will help understand what are the most relevant reasons behind an employee’s decision to voluntary terminate his employment – for example: low satisfaction, excessive workload, lack of career progression.

**Vision**: increase employee retention and reduce the turnover rate, with a particular focus on reducing the number of high-performers that voluntarily leave.    

**Mission**: develop a model that evaluates the probability that each employee will quit and that helps inform the decision of team managers on whether or not to take action –and which action to take– to mitigate employee flight risk.    

**Success criteria**: a satisfactory level across multiple metrics that measure classification accuracy. The longer term goal is to observe a measurable increase in the ability to retain employees that are highly valued by their managers.

 
## Suggested steps to deploy app

1. Clone repository

2. Create virtual environment and activate it

    ```
    virtualenv -p python3 turnover
    source turnover/bin/activate
    ```
    

3. Install required packages 

    ```
    pip install -r requirements.txt
    ```

4. Set up turnover.env file with the following structure

    ```
    export DATABASE=XXX
    export USERNAME=XXX
    export PORT=XXX
    export PASSWORD=XXX
    export HOST=XXX
    ```

5. Set environment variables from file

    ```
    source turnover.env
    ```

6. Download the data. The data was originally available on Kaggle, but it has since been remove. It can be downloaded from my Dropbox

    ```
    wget -O develop/data/turnover.csv https://www.dropbox.com/s/qnu09f9xo30njvc/turnover.csv?dl=1
    ```

7. Run the Makefile 

    ```
    make all
    ```

8. Launch the app

    ```
    python webapp/turnover.py
    ```

You can then go to the IP address where the app is running and use the app.