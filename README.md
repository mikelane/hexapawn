# Hexapawn Solver

### Installation

To install and run this, please unzip the files into a fresh directory. Then 
run the install script by running this command from within that directory:

    python3 setup.py install


### Execution

This will install any necessary requirements. You can access the CLI help by
running:

    python3 hexapawn_solver.py --help

Or you can run the solver by either passing a filename:

    python3 hexapawn_solver.py --filename ~/tests/mytests.in
    
or by redirecting stdin:

    python3 hexapawn_solver.py < ~/tests/mytests.in