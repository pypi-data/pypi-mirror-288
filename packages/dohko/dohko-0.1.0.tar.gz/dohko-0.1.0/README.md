# Dohko
zkGraph's experimental ZKP backend



## Introduction

This codebase serves as base point for the zkGraph's distributed and low memory footprint zero knowledge proofs using the Libra protocol. 
On this repo the following ideas are implemented:
* Linear time Sumcheck and GKR protocols and it's zk extensions
* Multilinear KZG and KZG10 protocols
* Plookup lookup arguments protocol


## Note
The plookup implementation comes from https://github.com/NOOMA-42/pylookup


## Install pybind11 and compile virgo bindings
* export CPLUS_INCLUDE_PATH=/usr/local/Cellar//python@3.12/3.12.4/Frameworks/Python.framework/Versions/3.12/include/python3.12/  
* cmake .. -DPython=1 -DPYTHON_EXECUTABLE=/Users/lorenzotomaz/Library/Caches/pypoetry/virtualenvs/dohko-Rkwus1zB-py3.11/bin/python -DPYTHON_INCLUDE_DIRS=/Users/lorenzotomaz/Library/Caches/pypoetry/virtualenvs/dohko-Rkwus1zB-py3.11/lib/python3.11/