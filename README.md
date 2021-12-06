# Grover algorithm application

Creation of a Nbit Grover iterator for Master degrees quantum mechanics project

## Lib

Require jupyter to run the examples notebook

Qiskit is the quantum circuit simulator

And matplotlib is used for Quiskit plot


## Usage

Generic function are in utils.py file

Important functions are "build_diffuser", "num_oracle" and "build_cnot"

### Examples

The examples are:
- simple2bits: a simple exemple from Qiskit tutorials
- Diffiser: show the creation and a test of a basic Grover diffuser
- Oracle: show the creation and a test of a Number gessing Oracle
- Nsize_Cnot: A generic Cnot gate of Nbits
- Qgessing_number: The construction of a Nbits oracle tha gess a given w number
  
### Setup

We recommend to install the dependencies in a python virtual environment

```
# Inside the project folder
python -m venv venv
```

Windows:

`source ./venv/Scripts/activate`

Linux:

`source ./venv/bin/activate`

then
```
pip install -r requirements.txt
python -m ipykernel install --user --name=myenv
jupyter lab
```

### Issue 

Any issues ? Open one in github :)