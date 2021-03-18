# The Role of Transitivity and Implicit Bias in Decision-Making with AI

Last updated: 03/18/2021

## Screenshots

TODO

## Setup

This is an Angular application (`/app`) with Python backend (`/server`).

These are the versions the system has been tested on as of **03/18/2021**

### /App

- Node.js (v14.16.0) [Link](https://nodejs.org/en/) - Environment
- npm (v6.14.11) [Link](https://www.npmjs.com/get-npm) - Package installer for Node.js
- Angular CLI (v11.2.5) [Link](https://cli.angular.io/) - For working with Angular projects

1. Make sure Node.js and npm are install on your system (see prior section for working versions)
2. Install Angular CLI by running `npm install -g @angular/cli`
3. Navigate to `/app` and run `npm install` to install packages
4. finally run `ng serve` and open a browser page at <localhost:4200>

### /Server

- Python (v.3.9.x) [Link](https://www.python.org/) - Environment
- pip [Link](https://pypi.org/project/pip/) - Package installer for Python
- venv [Link](https://docs.python.org/3/library/venv.html) - Serves files in virtual environment

#### Windows

1. `py -3.9 -m venv venv` - create a python3 virtual environment called _venv_ in the current directory
2. `venv\Scripts\activate.bat` - enters the virtual environment
   - **FROM THIS POINT ON: only use `python` command to invoke interpeter, avoid using global command `py`!!**
3. `python -m pip install -r requirements.txt` - installs required libraries local to this project environment

#### MacOS/Linux

1. `python3.9 -m venv venv` / `virtualenv --python=python3.7 venv` - create a python3 virtual environment called venv
2. `source venv/bin/activate` - enters the virtual environment
   - **FROM THIS POINT ON: only use `python` command to invoke interpeter, avoid using global command `python3.7`!!**
3. `python -m pip install -r requirements.txt` - installs required libraries local to this project environment

## Investigators

- Sarah Mathew ( smathew64 \[at\] gatech.edu )
- Adam Coscia ( acoscia6 \[at\] gatech.edu )
- Marina Vemmou ( mvemmou \[at\] gatech.edu )
