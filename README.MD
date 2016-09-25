Setup:
1.  install Anaconda (this is a package containing Python, Jupyter, and many popular packages)
    1.1 https://www.continuum.io/downloads#windows
    1.2 click on the Python 3.5 (or latest) version using 64 bit 
    1.3 Anaconda downloads (~353mb)
    1.4 click on the downloaded installer to run it
    1.5 Next -> I Agree -> Just Me -> (leave default path) Next -> (leave both checkboxes checked) install
    1.6 Anaconda is now installing
    1.7 After installing -> Next -> Finish    
2.  start Jupyter
    2.1 open windows command prompt (type CMD into Cortana)
    2.2 in the command prompt type: jupyter notebook 
        to open jupyter at a specific directory append --notebook-dir=<folder name>
        eg:  jupyter notebook --notebook-dir=c:\notebooks
    2.3 jupyter should now start and should automatically open a browser windows
3.  opening a notebook
    3.1 within the jupyter browser window, navigate to the jupyter notebook file you want to open (*.ipynb)
    3.2 another browser window will open showing your notebook
4.  need to install additional package to run sql commands within the notebook
    4.1 within the command prompt running jupyter, type Ctrl-C twice to stop jupyter
    4.2 run:  pip install ipython-sql
        this will install the ipython-sql package, you can install any package using:  pip install <packagename>
    4.3 once installed you can start jupyter again
    
