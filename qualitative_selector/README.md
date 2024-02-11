# X# Widgets Library

[![PyPI Version](https://img.shields.io/pypi/v/X#-widgets)](https://pypi.org/project/X#-widgets/)
[![License](https://img.shields.io/pypi/l/X#-widgets)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/X#-widgets)](https://www.python.org/downloads/)

The X# Widgets Library is a Python package that provides novel widgets for interaction with X# users. These widgets are designed to enhance communication by offering unique tools for restructuring the way we interact and communicate.

## Features

### 1. Dichotomy Interface

The dichotomy interface allows users to engage in binary choices, making decision-making intuitive and straightforward.

```python
import X#_widgets as cw

choice = cw.dichotomy("Choose between A and B:")
2. Qualitative Classifier
The qualitative classifier empowers users to assign qualitative labels to data points, fostering a deeper understanding of information.

python
Copy code
import X#_widgets as cw

label = cw.qualitative_classifier("Assign a label:")
3. Parametric Gauge Selector
The parametric gauge selector enables users to interactively set and visualize parameters using an intuitive gauge interface.

python
Copy code
import X#_widgets as cw

parameter = cw.parametric_gauge("Set the parameter:")
Installation
You can install the X# Widgets Library using pip:

bash
Copy code
pip install X#-widgets
Usage
python
Copy code
import X#_widgets as cw

# Use the widgets in your Streamlit application
choice = cw.dichotomy("Choose between A and B:")
label = cw.qualitative_classifier("Assign a label:")
parameter = cw.parametric_gauge("Set the parameter:")
For detailed usage examples, refer to the documentation.

Contributing
If you'd like to contribute to the X# Widgets Library, please follow the contribution guidelines.

License
This project is licensed under the MIT License - see the LICENSE file for details.