<p align="center">
  <img src="img/logo.png" alt= “” class=“center” width="50%" height="50%">
</p>

# Welcome to PYDAQ documentation

## Introduction

This site presents the full documentation of PYDAQ - Data Acquisition and Experimental Analysis with Python.
Here the user can find examples of how to use it for data acquisition and generating
signals using NIDAQ and Arduino boards.

Also, step-response experiments can be easily performed, as showed up
in [Step response (NIDAQ)](pydaq/step_response_nidaq) and [Step response (Arduino)](pydaq/step_response_arduino).

Furthermore, this tool can be used to apply any generic output in an experimental
tool, such as PRBS (Pseudo Random Binary Signal) or other persistently exciting signal, in order to generate
data for black box system identification.

The user is able to get/send data either using a command line method
of a GUI (Graphical User Interface), speeding up prototypes and quick
experiments, keeping the user confidence in the acquired/sent data.
Besides, the command line interface allows one to keep developing new features
while data are acquired.

## Installation and Requirements

The fastest way to install PYDAQ is using pip:

```console
pip install pydaq
```

PYDAQ requires:

- Installed driver of the board used (Arduino or National Instruments NIDAQ);
- nidaqmx (>=0.6.5) for data acquisition from National Instruments Boards;
- matplotlib (>=3.5.3) as a visualization tool;
- numpy (>=1.22.3) to process data;
- PySide6 (>=6.7.1), PySide6_Addons, PySide6_Essentials and shiboken6 as a Graphical User Interface framework;
- pyserial (>=3.5) to manage data to/from Arduino.

## Documentation Map

### Data Acquisition

Here the user will find examples of how to use GUI (Graphical User Interface) and
also commando line to acquire data using [NIDAQ](https://samirmartins.github.io/pydaq/get_data_nidaq/)
or [Arduino](https://samirmartins.github.io/pydaq/get_data_arduino/) boards.

### Sending data

In this Section is presented how the user can send data
from [NIDAQ](https://samirmartins.github.io/pydaq/send_data_nidaq/)
or [Arduino](https://samirmartins.github.io/pydaq/send_data_arduino/),
by mean of command line or a GUI (Graphical User Interface).

### Step response

Here the user will find examples of how to define parameters to perform
a step response experiments with available
boards ([NIDAQ](https://samirmartins.github.io/pydaq/step_response_nidaq/)/[Arduino](https://samirmartins.github.io/pydaq/step_response_arduino/)).

### Examples

In this section it will be provided Jupyter Notebook examples
presenting code
functionalities ([NIDAQ](https://samirmartins.github.io/pydaq/jupyter_notebooks/)/[Arduino](https://samirmartins.github.io/pydaq/jupyter_notebooks/)).

<p align="center">
  <img src="img/pydaq.gif" alt= “” class=“center” width="75%" height="75%">
</p>
