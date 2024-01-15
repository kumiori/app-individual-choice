import streamlit as st
import time
from streamlit_extras.streaming_write import write as streamwrite 
import random
import string
import streamlit_survey as ss

from pages.test_geocage import get_coordinates
# Function to initialize or get the session state


def corrupt_string(input_str, damage_parameter):
    # Define the list of symbols
    symbols = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~"

    # Calculate the number of characters to replace based on the damage parameter
    num_chars_to_replace = int(len(input_str) * damage_parameter)
    st.write(num_chars_to_replace)
    # Select random indices to replace
    indices_to_replace = random.sample(range(len(input_str)), num_chars_to_replace)

    # Corrupt the string
    corrupted_list = list(input_str)
    for index in indices_to_replace:
        corrupted_list[index] = random.choice(symbols)

    return ''.join(corrupted_list), num_chars_to_replace


summary0 = """## 
The System, solved.

## Everything cracks, eventually. Right? > 

## Everything is flawed, already. Right? >

## This is the beginning of a thriller. 
# Killer
"""

summary1 = """## 

What is the use of a mathematical tool?
## Did we ever land on the moon?

## What is understanding? What is to understand?

## Where all this is going? Where all this comes from?

"""

summary2 = """## 
Think of a theorem, as a product to be sold.
Who buys, if it is for all?

## In how many ways it can be used 

## other than those those for which is sold?

## How triangles behaves belongs to all (of them).
"""
summary3 = """##
## For them, this is a scientific experiment. 
## If you were to be asked...

## For us, this is the way we understand.
## For now, only few participate.

"""

part_0 = """## 

## Do you like it sexy? We deploy a scientific platform to predict large-scale crack-like events.

Where are you located? 

"""

part_1 = """## part_1
We implement a numerical platform, a general framework to model and understand evolutionary problems that are challenging enough to require squeezing the mind until it melts.

## The system is irreversible and shows smooth continuous incremental transitions as well as rare, brutal, discontinuous events.

We like them both.

Unless understood, cracks seem always dangerous. 

Your location helps us updating our sensors. 

## Thank you for supporting our research.  
"""

part_2 = """"part_2
The overarching goal is to continuously integrate data for reliable predictions of strongly nonlinear phenomena,
to address mathematical problems that are general enough to apply, in principle, to a large variety of applications

Crunchy problems may arise in diverse fields of science including mechanics, economy, ecology, quantum physics, and social sciences.

Our technology, is three nonlinear variational solvers to be seen as modular components that are trained to address singular irreversible systems.
"""

solve = """## The problem *P(0), solved.

 We serve a problem of the following type:
 
> P(0): compute the evolution of a “complex system” 
over a given time horizon (T) as AN OBSERVABLE 
and measurable irreversible map 
THAT IS globally energy-optimal.

What is a "complex system", you ask?

Many definitions may fail, but we like this one:

think of a beast with many heads,

with teeth sharp and extensible limbs,

fluid in motion and heavy in rest, 

eyes that see across all frequencies,

a beast that bites and screams,

as touched, spits fire and eats itself,

it only befriends its own kind,

A complex problem is elusive,
 
a rock into a drop: in math enshrined.


\* We solve P(0) in the case of fracture
finding a new path, in an infinitely 
dimensional space...
"""

code = """live code
INFO:root:The root process spawning an evolution computation (rank 0)
INFO:root:DOLFINx version: 0.6.0 based on GIT commit: 24f86a9ce57df6978070dbee22b3eae8bb77235f of https://github.com/FEniCS/dolfinx/
===================-output/one-dimensional-bar/MPI-1/50/b0107f5c9f5d9d181c005d2fc943e030-=================
INFO:root:{'snes_type': 'vinewtonrsls', 'snes_linesearch_type': 'basic', 'snes_rtol': 1e-08, 'snes_atol': 1e-08, 'snes_max_it': 30, 'snes_monitor': '', 'linesearch_damping': 0.5}
INFO:root:(1e-08, 1e-08, 1e-08, 30)
CRITICAL:root:-- Solving for t = 0.00 --
  0 SNES Function norm 0.000000000000e+00 
  0 SNES Function norm 0.000000000000e+00 
CRITICAL:root:AM - Iteration:   0, res F Error: 0.0000e+00, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, H1 Error: 0.0000e+00, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, L2 Error: 0.0000e+00, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, Linfty Error: 0.0000e+00, alpha_max: 0.0000e+00
  0 SNES Function norm 0.000000000000e+00 
  0 SNES Function norm 0.000000000000e+00 
ALTMIN - Iterations:   1,            Error: 0.0000e+00, alpha_H1,            alpha_max: 0.0000e+00
CRITICAL:root:
### SNES iteration 0
CRITICAL:root:# sub  0 |x|=0.000e+00 |dx|=0.000e+00 |r|=0.000e+00 (Displacement)
CRITICAL:root:# sub  1 |x|=0.000e+00 |dx|=0.000e+00 |r|=1.407e-01 (Damage)
CRITICAL:root:# all    |x|=0.000e+00 |dx|=0.000e+00 |r|=1.407e-01
  0 SNES Function norm 0.000000000000e+00 
INFO:root:rank 0) Current state is damage-critical? False 🌪 
State is elastic: False
State's inertia: (0, 0, 51)
Evolution is unique: True
INFO:root:the current state is damage-subcritical (hence elastic), the state is thus stable
nan
CRITICAL:root:-- Solving for t = 0.50 --
  0 SNES Function norm 2.500499950010e+01 
  1 SNES Function norm 2.259119721580e+01 
  2 SNES Function norm 1.776359264721e+01 
  3 SNES Function norm 8.108383510023e+00 
  4 SNES Function norm 1.438424505441e-14 
  0 SNES Function norm 0.000000000000e+00 
CRITICAL:root:AM - Iteration:   0, res F Error: 1.4384e-14, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, H1 Error: 0.0000e+00, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, L2 Error: 0.0000e+00, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, Linfty Error: 0.0000e+00, alpha_max: 0.0000e+00
  0 SNES Function norm 1.438424505441e-14 
  0 SNES Function norm 0.000000000000e+00 
ALTMIN - Iterations:   1,            Error: 0.0000e+00, alpha_H1,            alpha_max: 0.0000e+00
CRITICAL:root:
### SNES iteration 0
CRITICAL:root:# sub  0 |x|=2.072e+00 |dx|=0.000e+00 |r|=1.438e-14 (Displacement)
CRITICAL:root:# sub  1 |x|=0.000e+00 |dx|=0.000e+00 |r|=1.055e-01 (Damage)
CRITICAL:root:# all    |x|=2.072e+00 |dx|=0.000e+00 |r|=1.055e-01
  0 SNES Function norm 1.438424505441e-14 
INFO:root:rank 0) Current state is damage-critical? False 🌪 
State is elastic: False
State's inertia: (0, 0, 51)
Evolution is unique: True
INFO:root:the current state is damage-subcritical (hence elastic), the state is thus stable
nan
CRITICAL:root:-- Solving for t = 0.99 --
  0 SNES Function norm 2.450489951010e+01 
  1 SNES Function norm 1.950389961008e+01 
  2 SNES Function norm 9.501899810038e+00 
  3 SNES Function norm 2.130818515879e-14 
  0 SNES Function norm 0.000000000000e+00 
CRITICAL:root:AM - Iteration:   0, res F Error: 2.1308e-14, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, H1 Error: 0.0000e+00, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, L2 Error: 0.0000e+00, alpha_max: 0.0000e+00
CRITICAL:root:AM - Iteration:   0, Linfty Error: 0.0000e+00, alpha_max: 0.0000e+00
  0 SNES Function norm 2.130818515879e-14 
  0 SNES Function norm 0.000000000000e+00 
ALTMIN - Iterations:   1,            Error: 0.0000e+00, alpha_H1,            alpha_max: 0.0000e+00
CRITICAL:root:
### SNES iteration 0
CRITICAL:root:# sub  0 |x|=4.102e+00 |dx|=0.000e+00 |r|=2.131e-14 (Displacement)
CRITICAL:root:# sub  1 |x|=0.000e+00 |dx|=0.000e+00 |r|=2.800e-03 (Damage)
CRITICAL:root:# all    |x|=4.102e+00 |dx|=0.000e+00 |r|=2.800e-03
  0 SNES Function norm 2.130818515879e-14 
INFO:root:rank 0) Current state is damage-critical? False 🌪 
State is elastic: False
State's inertia: (0, 0, 51)
Evolution is unique: True
INFO:root:the current state is damage-subcritical (hence elastic), the state is thus stable
nan
CRITICAL:root:-- Solving for t = 1.01 --
  0 SNES Function norm 1.000199980004e+00 
  1 SNES Function norm 1.639074257117e-14 
  0 SNES Function norm 2.828320703174e-03 
  1 SNES Function norm 1.740467256589e-16 
CRITICAL:root:AM - Iteration:   0, res F Error: 1.5997e-14, alpha_max: 1.9704e-02
CRITICAL:root:AM - Iteration:   0, H1 Error: 1.9704e-02, alpha_max: 1.9704e-02
CRITICAL:root:AM - Iteration:   0, L2 Error: 1.9704e-02, alpha_max: 1.9704e-02
CRITICAL:root:AM - Iteration:   0, Linfty Error: 1.9704e-02, alpha_max: 1.9704e-02
  0 SNES Function norm 1.599723126151e-14 
  0 SNES Function norm 1.740467256589e-16 
CRITICAL:root:AM - Iteration:   1, res F Error: 1.5997e-14, alpha_max: 1.9704e-02
CRITICAL:root:AM - Iteration:   1, H1 Error: 0.0000e+00, alpha_max: 1.9704e-02
CRITICAL:root:AM - Iteration:   1, L2 Error: 0.0000e+00, alpha_max: 1.9704e-02
CRITICAL:root:AM - Iteration:   1, Linfty Error: 0.0000e+00, alpha_max: 1.9704e-02
  0 SNES Function norm 1.599723126151e-14 
  0 SNES Function norm 1.740467256589e-16 
  0 SNES Function norm 1.599723126151e-14 
  0 SNES Function norm 1.740467256589e-16 
ALTMIN - Iterations:   2,            Error: 0.0000e+00, alpha_H1,            alpha_max: 1.9704e-02
CRITICAL:root:
### SNES iteration 0
CRITICAL:root:# sub  0 |x|=4.185e+00 |dx|=0.000e+00 |r|=1.600e-14 (Displacement)
CRITICAL:root:# sub  1 |x|=1.407e-01 |dx|=0.000e+00 |r|=1.740e-16 (Damage)
CRITICAL:root:# all    |x|=4.187e+00 |dx|=0.000e+00 |r|=1.600e-14
  0 SNES Function norm 1.599817803055e-14 
INFO:root:rank 0) Current state is damage-critical? False 🌪 
State is elastic: True
State's inertia: (1, 0, 101)
Evolution is unique: False
CRITICAL:root:     [i=0] error_x_L2 = 4.9287e+00, atol = 1e-06, res = 1.0
CRITICAL:root:     [i=10000] error_x_L2 = 6.6466e-06, atol = 1e-06, res = 0.030273525638537892
CRITICAL:root:     [i=20000] error_x_L2 = 1.8026e-06, atol = 1e-06, res = 0.02759191628132749
CRITICAL:root:     [i=30000] error_x_L2 = 1.0118e-06, atol = 1e-06, res = 0.027415762528682403
CRITICAL:root:     [i=30221] met criteria: [1], reason(s) ['converged atol']
INFO:root:Convergence of SPA algorithm within 30221 iterations
INFO:root:Restricted Eigen _xk is in cone 🍦 ? True
CRITICAL:root:Restricted Eigenvalue -1.1062e-02
INFO:root:Restricted Eigenvalue is positive False
INFO:root:Restricted Error 9.9999e-07
WARNING:matplotlib.legend:No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
WARNING:matplotlib.legend:No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
-0.011061629018396649
CRITICAL:root:-- Solving for t = 1.30 --
  0 SNES Function norm 1.393723241992e+01 
  1 SNES Function norm 4.229229148114e+00 
  2 SNES Function norm 3.060593114322e-14 
  0 SNES Function norm 9.240592640444e-02 
  1 SNES Function norm 3.210806372043e-15 
CRITICAL:root:AM - Iteration:   0, res F Error: 1.1414e-14, alpha_max: 4.0828e-01
CRITICAL:root:AM - Iteration:   0, H1 Error: 3.8858e-01, alpha_max: 4.0828e-01
CRITICAL:root:AM - Iteration:   0, L2 Error: 3.8858e-01, alpha_max: 4.0828e-01
CRITICAL:root:AM - Iteration:   0, Linfty Error: 3.8858e-01, alpha_max: 4.0828e-01
  0 SNES Function norm 1.141439399906e-14 
  0 SNES Function norm 3.210806372043e-15 
CRITICAL:root:AM - Iteration:   1, res F Error: 1.1414e-14, alpha_max: 4.0828e-01
CRITICAL:root:AM - Iteration:   1, H1 Error: 0.0000e+00, alpha_max: 4.0828e-01
CRITICAL:root:AM - Iteration:   1, L2 Error: 0.0000e+00, alpha_max: 4.0828e-01
CRITICAL:root:AM - Iteration:   1, Linfty Error: 0.0000e+00, alpha_max: 4.0828e-01
  0 SNES Function norm 1.141439399906e-14 
  0 SNES Function norm 3.210806372043e-15 
  0 SNES Function norm 1.141439399906e-14 
  0 SNES Function norm 3.210806372043e-15 
ALTMIN - Iterations:   2,            Error: 0.0000e+00, alpha_H1,            alpha_max: 4.0828e-01
CRITICAL:root:
### SNES iteration 0
CRITICAL:root:# sub  0 |x|=5.387e+00 |dx|=0.000e+00 |r|=1.141e-14 (Displacement)
CRITICAL:root:# sub  1 |x|=2.916e+00 |dx|=0.000e+00 |r|=3.211e-15 (Damage)
CRITICAL:root:# all    |x|=6.125e+00 |dx|=0.000e+00 |r|=1.186e-14
  0 SNES Function norm 1.185738874814e-14 
INFO:root:rank 0) Current state is damage-critical? False 🌪 
State is elastic: True
State's inertia: (2, 0, 100)
Evolution is unique: False
CRITICAL:root:     [i=0] error_x_L2 = 6.0169e+00, atol = 1e-06, res = 1.0
CRITICAL:root:     [i=10000] error_x_L2 = 1.2082e-05, atol = 1e-06, res = 0.039735448114524584
CRITICAL:root:     [i=20000] error_x_L2 = 6.1977e-06, atol = 1e-06, res = 0.03490267714457259
CRITICAL:root:     [i=30000] error_x_L2 = 3.7133e-06, atol = 1e-06, res = 0.033456582941216687
CRITICAL:root:     [i=40000] error_x_L2 = 2.2053e-06, atol = 1e-06, res = 0.03298461011637732
CRITICAL:root:     [i=50000] error_x_L2 = 1.2506e-06, atol = 1e-06, res = 0.0326297722657053
CRITICAL:root:     [i=53949] met criteria: [1], reason(s) ['converged atol']
INFO:root:Convergence of SPA algorithm within 53949 iterations
INFO:root:Restricted Eigen _xk is in cone 🍦 ? True
CRITICAL:root:Restricted Eigenvalue -1.8790e-02
INFO:root:Restricted Eigenvalue is positive False
INFO:root:Restricted Error 9.9995e-07
WARNING:matplotlib.legend:No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
WARNING:matplotlib.legend:No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.
-0.018790339767650537
   load  elastic_energy  fracture_energy  ...                                                u_t      inertia uniqueness
0  0.00        0.000000         0.000000  ...  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, ...   (0, 0, 51)       True
1  0.50        0.125000         0.000000  ...  [0.0, 0.010000000000000054, 0.0200000000000001...   (0, 0, 51)       True
2  0.99        0.490050         0.000000  ...  [0.0, 0.01980000000000006, 0.03960000000000012...   (0, 0, 51)       True
3  1.01        0.490148         0.019704  ...  [0.0, 0.02020000000000001, 0.04040000000000002...  (1, 0, 101)      False
4  1.30        0.295858         0.408284  ...  [0.0, 0.026000000000000047, 0.0520000000000000...  (2, 0, 100)      False

[5 rows x 14 columns]
[nan, nan, nan, -0.011061629018396649, -0.018790339767650537]
===================-b0107f5c9f5d9d181c005d2fc943e030-=================
===================-output/one-dimensional-bar/MPI-1/50/b0107f5c9f5d9d181c005d2fc943e030-=================
"""

offer = """Offer support to the project, and get access to the code, the data, and the results.
"""

texts = [summary0, summary1, summary2, summary3, part_0, part_1, part_2, solve, code, offer]

def _stream_example(text, damage):
    # Define sleep lengths for different punctuation symbols
    sleep_lengths = {'.': 1., ',': 0.3, '!': 1.7, '?': 1.5, ';': 0.4, ':': 0.4}
    sleep_lengths = {key: value * (1. + damage) for key, value in sleep_lengths.items()}
    # st.json(sleep_lengths)

    # st.write(sleep_lengths.values() * (1+damage))
    
    for i, word in enumerate(text.split()):
        # Check if the last character is a punctuation symbol
        last_char = word[-1] if word[-1] in string.punctuation else None

        # Yield the word with appropriate sleep length
        if last_char == '.' or last_char == '?' or last_char == '^':
            yield word + " \n "
        else:
            yield word + " "
        
        if last_char and last_char in sleep_lengths:
            time.sleep(sleep_lengths[last_char])
        else:
            time.sleep(0.3)
            
# Main function
def main():
    # Page title
    st.title("The Code")
    # Session State also supports attribute based syntax
    survey = ss.StreamlitSurvey("Home")
    col1, col2, col3 = st.columns(3)

    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    
    if 'damage_parameter' not in st.session_state:
        st.session_state.damage_parameter = 0.0  # Initial damage parameter
    
    if 'location' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter
    
    if 'coordinates' not in st.session_state:
        st.session_state.location = None  # Initial damage parameter

    st.write(f'page_number {st.session_state.page_number}')

    last_page = len(texts) - 1
    prev, _ ,next = st.columns([1, 10, 1])

    st.write(f"Damage Parameter: {st.session_state.damage_parameter:.2f}")
    if st.session_state.damage_parameter > 0:
        st.info("There is no way back in this game. Go back and corrupt the strings.")
    if next.button("\>"):
        if st.session_state.page_number + 1 > last_page:
            st.session_state.page_number = 0
        else:
            st.session_state.page_number += 1

    if prev.button("<"):
        if st.session_state.page_number - 1 < 0:
            st.session_state.damage_parameter += 0.01  # You can adjust the increment
            st.session_state.page_number = last_page
        else:
            st.session_state.damage_parameter += 0.01  # You can adjust the increment
            st.session_state.page_number -= 1

    # streamwrite(_stream_example(texts[st.session_state.page_number]), unsafe_allow_html=True)
    corrupted_text, replaced_chars = corrupt_string(texts[st.session_state.page_number], st.session_state.damage_parameter)

    if st.session_state.page_number == 4:
        if st.session_state.location:
            st.write(f"Location: {st.session_state.location}")
            st.write(corrupted_text)
        else:
            streamwrite(_stream_example(corrupted_text, st.session_state.damage_parameter), unsafe_allow_html=True)
            
    else:
        streamwrite(_stream_example(corrupted_text, st.session_state.damage_parameter), unsafe_allow_html=True)



    if st.session_state.page_number == 0:
        current_local_time = survey.timeinput("What time is it, on your side? Sorry to ask..")
    
    # if st.session_state.page_number == 5:
    #     st.write("```python")
    #     st.code(code, language="python")
    #     st.write("```")
    #     # st.markdown(texts[st.session_state.page_number])

    if st.session_state.page_number == 4:
        location = survey.text_input("location", help="Our location.", value=st.session_state.location)
        coordinates = get_coordinates(st.secrets.opencage["OPENCAGE_KEY"], location)
        if coordinates:
            st.write(f"Coordinates for {location}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
            st.session_state.location = location
            st.session_state.coordinates = coordinates
            
        st.markdown("## Think of Antartica.")
        
        if st.button("This is what we run"):
            st.session_state.page_number += 1
            
    if st.session_state.page_number == 8:
        
        params = st.query_params
        st.write(params)
        # {"show_map": ["True"], "selected": ["asia", "america"]}

        # Question 1 in the first column

        # Question 2 in the second column
        with col2:
            st.write("We start by showing something we have never seen...Where are you located now?")

        # Question 3 and 4 in the third column
        with col3:
            # birthplace = survey.text_input("Where were you born?", help="Enter the name of your birthplace.")
            lucky_number = survey.number_input("What's your lucky number?", min_value=0, max_value=100000000)

        # Get user input for location

        st.json(survey.data)
        
# Run the app
if __name__ == "__main__":
    main()
