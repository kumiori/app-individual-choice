import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.express as px
from matplotlib.patches import Polygon
from lib.survey import CustomStreamlitSurvey
from lib.io import create_button, create_dichotomy, create_qualitative, create_yesno, create_yesno_row, create_next, create_globe, create_textinput, create_checkbox, create_equaliser, fetch_and_display_data, conn

from streamlit_extras.stateful_button import button as stateful_button 
from streamlit_extras.stylable_container import stylable_container
from streamlit_modal import Modal
from streamlit import rerun as rerun  # type: ignore
import streamlit.components.v1 as components


class _Modal(Modal):
    def open(self, **kwargs):
        print(kwargs)
        if 'src' in kwargs:
            self.src = kwargs['src']
            print(self.src)
        st.session_state[f'{self.key}-opened'] = True
        st.session_state[f'{self.key}-src'] = kwargs['src']
        rerun()


def generate_random_matrix(N, a=0, b=1):
    """
    Generate a random matrix of size NxN with values between a and b.

    Parameters:
        N (int): Size of the matrix (number of rows and columns).
        a (float): Lower bound of the random values.
        b (float): Upper bound of the random values.

    Returns:
        numpy.ndarray: Random matrix of size NxN.
    """
    return np.random.uniform(a, b, (N, N))

def plot_random_matrix(matrix):
    fig, ax = plt.subplots()
    ax.scatter(*np.meshgrid(range(matrix.shape[0]), range(matrix.shape[1])),
               c=matrix, cmap='gray', edgecolors='none', s=100)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Random Matrix")
    st.pyplot(fig)

def plot_random_matrix(matrix, placeholder):
    with placeholder:
        fig = px.imshow(matrix, color_continuous_scale='gray')
        # fig.update_layout(coloraxis_showscale=False)
        fig.update_layout(coloraxis_showscale=False, 
                          xaxis_showticklabels=False, 
                          yaxis_showticklabels=False)
        fig.update_layout(coloraxis_showscale=False, xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False))
        fig.update_traces(hovertemplate='Trust: %{z:.2f}')

        st.plotly_chart(fig)
   
def plot_random_matrix_matplotlib(matrix):
    plt.rcParams.update({
        "figure.facecolor":  (1.0, 0.0, 0.0, 0.9),  # red   with alpha = 30%
        "axes.facecolor":    (1.0, 0.0, 0.0, 0.4),  # green with alpha = 50%
        # "savefig.facecolor": (0.0, 0.0, 1.0, 0.0),  # blue  with alpha = 20%
    })
    fig, ax = plt.subplots()
    ax.scatter(*np.meshgrid(range(matrix.shape[0]), range(matrix.shape[1])),
               c=matrix, cmap='gray', edgecolors='none', s=500)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    # ax.patch.set_facecolor('red')

    # ax.set_title("Random Matrix")
    return fig

def plot_random_matrix_matplotlib2(matrix):
    fig, ax = plt.subplots()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color = plt.cm.gray(matrix[i, j])  # Convert matrix value to grayscale color
            polygon = Polygon([[i, j], [i+1, j], [i+1, j+1], [i, j+1]], closed=True, facecolor=color, edgecolor='none')
            ax.add_patch(polygon)
    ax.set_xlim(0, matrix.shape[0])
    ax.set_ylim(0, matrix.shape[1])
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    # ax.set_title("Random Matrix")
    return fig

def plot_random_matrix_matplotlib_binary(matrix):
    fig, ax = plt.subplots()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > 0.5:
                color = 'red'
            elif matrix[i, j] < 0.5:
                color = 'black'
            else:
                color = 'green'
            polygon = Polygon([[i, j], [i+1, j], [i+1, j+1], [i, j+1]], closed=True, facecolor=color, edgecolor='none')
            ax.add_patch(polygon)
    ax.set_xlim(0, matrix.shape[0])
    ax.set_ylim(0, matrix.shape[1])
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    return fig

def generate_sparse_matrix(N, M):
    # Create an empty matrix filled with zeros
    matrix = np.zeros((N, N))
    
    # Generate random row and column indices for non-zero values
    row_indices = np.random.choice(range(N), M, replace=True)
    col_indices = np.random.choice(range(N), M, replace=True)
    # Assign random non-zero values to the specified indices
    for i in range(M):
        matrix[row_indices[i], col_indices[i]] = np.random.rand()
    
    return matrix

def generate_random_plots():
    col1, spacer, col2 = st.columns([2, .5, 2])
    
    with col1:
        placeholder = col1.empty()
    with spacer:
        st.markdown("# <center>`vs`</center>", unsafe_allow_html=True)
    placeholder2 = col2.empty()

    with st.expander("Settings", expanded=False):
        # User input for refresh interval
        refresh_interval = st.slider("Select refresh interval (seconds):", min_value=1, max_value=10, step=1)

            # User input for matrix size
        N = st.slider("Select number of players (or its root):", value=10, min_value=2, max_value=100, step=3)
            # User input for matrix size
        M = st.slider("Select number of nonzero in the sparse:", min_value=1, max_value=N, step=1)

    st.write("Players: ", N**2)
    
    while True:
        # Generate random matrix
        random_matrix = generate_random_matrix(N, a=.3)
        sparse_matrix = generate_sparse_matrix(N, M)
        
        if N == 2:
            random_matrix[1, 1] = 1.
        
        # Plot random matrix
        # plot_random_matrix(random_matrix, placeholder)
        # fig = plot_random_matrix_matplotlib(random_matrix)
        fig = plot_random_matrix_matplotlib2(random_matrix)
        fig2 = plot_random_matrix_matplotlib_binary(sparse_matrix)

        placeholder.pyplot(fig)
        placeholder2.pyplot(fig2)
            
        # Refresh and reshuffle matrix every given interval
        time.sleep(refresh_interval)

        placeholder.empty()
        for _fig in [fig, fig2]:
            plt.close(_fig)  # Close the figure to release memory

    

def main():
    st.title("Welcome to Game Trust")
    st.write("Game Trust is an experimental game designed to explore trust dynamics between investors and financial institutions.")
    """
We explore questions of trust, trustworthiness, and cooperation in social interactions. It's particularly interesting because it involves sequential decision-making, where one player's decision influences the other's subsequent decision. 

Trusting behavior often depends on many factors and it is difficult to estimate. The perceived trustworthiness of the partner plays a role, likewise perceived risks and rewards as well as social norms regarding cooperation and reciprocity. Transparency, clarity, how many other factors? This game allows us, researchers and players, to study how these factors influence decision-making and how trust and cooperation can emerge or break down in different situations.
And, more importantly, to foresee what are the outcomes.    
    """

    # technology outsmarting the humans
    # take a lot of people? how many people are there?
    
    st.divider()
    st.header("Disclaimer:")
    st.write("""
             `This game involves real-time decision-making and may involve real-world consequences. 
             ................................... Please play consciously ....................................
             This game involves money, and the outcomes are real. Please play responsibly.
             What money really is, is a question that has been asked for centuries.
             This time, we ask you to play with it. Using it as a tool, to understand trust,
             to send encoded signals.
             `
    """)
    st.write('`.|.|..........|.....................................|............*..............|.....||.`')
    st.write('`A matter of trust, coded fast.`')
    st.write('`In an infinite-dimensional energy space there are two players: player I and player B...`')
    st.header("Instructions:")
    st.write("In this game, you will act as an investor deciding how much trust to invest in the bank (the Trustee).")
    st.write("Your task is to choose a level of trust, represented by a value between 0 and 1.")
    st.write("You will also have an initial capital to allocate to the bank, for you to gauge.")
    st.write("The bank has received a challenge: to repay the investor's trust allocating a small part of its financial assets to the investor, to allow the investor play a role facing the shared issues facing climate concerns.")
    st.write("Will the Trustee accept the challenge and move, or will it betray the investor's trust?")
    st.write("Based on your the investor's perceptions and the bank's response, both players will receive certain payoffs.")
    st.write("Remember, your level of trust can change and this is of utmost importance.")
    
    st.header("Gameplay:")
    st.write("0. Are you happy to pay? Save your preferences.")
    st.write("1. Choose a level of trust (α) between 0 and 1 using the slider.")
    # st.write("2. Allocate an initial capital (C) to the bank.")
    st.write("2. The bank, or someone on their behalf, will decide whether to 'move' or 'betray'.")
    st.write("3. Based on the bank's decision(s) and your trust level, things will unfold.")
    st.write("4. Rember: you can adjust your trust level at any time, increase is free - decrease leaves a trace.")
    
    
    st.divider()
    survey = CustomStreamlitSurvey()
    create_dichotomy(key = 'trust', kwargs={'survey': survey, 
                                            'name': 'investor', 
                                           'label': 'Trust Level', 
                                           'question': 'How much do you trust the Trustee?', 
                                           'rotationAngle': 0, 
                                           'gradientWidth': 60,
                                           "inverse_choice": lambda x: 'full 🫧' if x == 1 else 'none 🕳️' if x == 0 else 'midway ✨' if x == 0.5 else 'partial 💩' if x < 0.5 else 'partial 🥀',  
                                           'messages': ["⛈️🔔🎐", "Sounds great!", "Going up or down?"],
                                           'height': 220, 
                                           'title': 'I trust',
                                           'invert': False, 
                                           'shift': 30})
    

    st.header("Trust Level:")
    trust_level = st.slider("Select your trust level:", min_value=0.0, max_value=1.0, step=0.01)
    st.write("Your current trust level: ", trust_level)
    
    st.divider()
    st.header("Preferences:")
    capital = st.number_input("Enter, roughly, the capital you host on the Trustee's network:", min_value=1, step=1000)
    capital_oom = int(np.log10(capital))
    st.write("Your order of magnitude: ", capital_oom, 'zeros')
    
    if st.button("Start Game"):
        st.toast("Preferences saved!", icon="🚀")
        
    
    st.divider()

    st.title('Welcome to this experiment')

    st.divider()


    src_101 = "https://pay.sumup.com/b2c/QDJLWO13"
    src_100K = 'https://pay.sumup.com/b2c/Q8F8EX3C'
    src_free = "https://pay.sumup.com/b2c/Q2RYJEC8"
    src_bet = 'https://pay.sumup.com/b2c/QDEYTAA2'

    modal = _Modal(
        "There is no _______ without consent.", 
        key="pay-mode",
        padding=20,    # default value
        max_width=744  # default value
    )
    
    betray = Modal(
        "There is no _______ without consent.", 
        key="betray",
    )
    
    """### Steps:
1. **Players**: The game involves two players: the investor and the bank (HSBC). The investor is a collective player, each of its elements decides how much trust to invest in the Trustee, while the bank determines its response on their cost-opportunity.

2. **Trust Variable**: The investor's decision is represented by a trust variable (α), ranging from zero (no trust) to one (full trust), reflecting the level of trust invested in HSBC.

3. **Impact of Investment**: The investor's trust investment (α) is multiplied by their capital (C), determining the resources allocated to HSBC.

4. **Trustee's Decision**: the Trustee (or an entity on their behalf) chooses to "move" or "betray." Moving implies positive action towards allocating funds to transparently address challenges such as climate change, while betraying maintains the status quo, the bank gains - business as usual - at the investor's expense.

5. **Reciprocation**: If the Trustee moves, it allocates a portion of resources (β, a percentage of the Trustee's assets) to the investor. If it betrays, the resources are kept by the bank, business as usual.

6. **Outcome**: The payoffs for both players depend on the Trustee's decision and the investor's level of trust. Positive action by the Trustee and increased trust lead to mutual gains, betrayal results in systematic losses for the investor, and progressive erosion of the trust variable may shed new light on the bank's trustworthiness.

    """    
    
    col1, col2, col3 = st.columns([1, 1, 1])
    placeholder = st.empty()                
    with col2:
        if stateful_button("3", key="button1", type="primary", use_container_width = True):
            if stateful_button("2", key="button2", use_container_width = True):
                if stateful_button("1", key="button3", use_container_width = True):
                    st.markdown("<center>Let's go...</center>", unsafe_allow_html=True)
                    st.toast('Consent granted/Preferences saved!', icon="🚀")
                    
                    open_play = st.button("I play", use_container_width=True, key="play")

                    if open_play:
                        modal.open(src=src_101)


    def foo():
        st.toast("Button clicked!")

    with stylable_container(key="payment_button",css_styles="""
    {
        [data-testid="baseButton-primary"] {
            box-shadow: 0px 10px 14px -7px #3e7327;
            background-image:url("data/qrcode_1.png") fixed center;
            border-radius:4px;
            border:1px solid #4b8f29;
            display:inline-block;
            cursor:pointer;
            color:#ffffff;
            font-family:Arial;
            font-size:13px;
            font-weight:bold;
            padding:14px 31px;
            height: 100px;
            text-decoration:none;
            text-shadow:0px 1px 0px #5b8a3c;
        }
        [data-testid="baseButton-primary"]:hover {
            # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
            background-color:#72b352;
            background-color: red;
            cursor: arrow;
        }
        [data-testid="baseButton-primary"]:active {
            position:relative;
            background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
            top:1px;
        }
    }
    """,):
        st.button("button", type='primary', on_click=foo, use_container_width=True, key="payment")

    st.divider()
    
    open_play = st.button("I play", use_container_width=True)

    if open_play:
        modal.open(src=src_101)

    st.header("Bank's Decision:")
    # Implement bank's decision logic and display here
    
    open_betray = st.button("I betray I", use_container_width=True)
    open_move = st.button("I move I", use_container_width=True)

    if open_move:
        modal.open(src=src_100K)

    if modal.is_open():
        with modal.container():
            components.iframe(st.session_state[f'{modal.key}-src'], height=1500)
            # st.snow()

    if open_betray:
        betray.open()
    
    if betray.is_open():
        with betray.container():
            st.title('Betrayal')
         
    st.header("Heads or tails? You can bet")
    open_bet = st.button("I bet against (.......1) or in favour (......0)", use_container_width=True)

    if open_bet:
        modal.open(src=src_bet)


    st.divider()
    
    col1, _, col2 = st.columns([1, .5, 1])
        
    with col1:
        st.title('Investor')

        with stylable_container(key="play_button", css_styles="""
        {
            [data-testid="baseButton-primary"] {
                box-shadow: 0px 10px 14px -7px #3e7327;
                background-image:url("data/qrcode_1.png") fixed center;
                border-radius:4px;
                border:1px solid #4b8f29;
                display:inline-block;
                cursor:pointer;
                color:#ffffff;
                font-family:Arial;
                font-size:13px;
                font-weight:bold;
                padding:14px 31px;
                height: 150px;
                text-decoration:none;
                text-shadow:0px 1px 0px #5b8a3c;
            }
            [data-testid="baseButton-primary"]:hover {
                # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                background-color:#72b352;
                background-color: red;
                cursor: arrow;
            }
            [data-testid="baseButton-primary"]:active {
                position:relative;
                background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                top:1px;
            }
        }
        """,):
            # st.button("button", type='primary', on_click=foo, use_container_width=True, key="_payment")
            open_play = st.button("I play", type='primary', use_container_width=True, key="play2")
        with stylable_container(key="bet_button", css_styles="""
        {
            [data-testid="baseButton-primary"] {
                box-shadow: 0px 10px 14px -7px #3e7327;
                background-image:url("data/qrcode_1.png") fixed center;
                background-color: gray;
                border-radius:4px;
                border:1px solid #4b8f29;
                display:inline-block;
                cursor:pointer;
                color:#ffffff;
                font-family:Arial;
                font-size:13px;
                font-weight:bold;
                padding:14px 31px;
                height: 50px;
                text-decoration:none;
                text-shadow:0px 1px 0px #5b8a3c;
            }
            [data-testid="baseButton-primary"]:hover {
                # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                background-color:#72b352;
                background-color: red;
                cursor: arrow;
            }
            [data-testid="baseButton-primary"]:active {
                position:relative;
                background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                top:1px;
            }
        }
        """,):
            open_bet = st.button("I bet (how does it end? 1 or 0)", type='primary', use_container_width=True, key="bet")

        if open_bet:
            modal.open(src=src_bet)

        if open_play:
                modal.open(src=src_101)
        
    with col2:
        st.title('Trustee')
        with stylable_container(key="betray_button", css_styles="""
        {
            [data-testid="baseButton-primary"] {
                box-shadow: 0px 10px 14px -7px #3e7327;
                border-radius:4px;
                border:1px solid #4b8f29;
                background-color: black;
                display:inline-block;
                cursor:pointer;
                color:#ffffff;
                font-family:Arial;
                font-size:13px;
                font-weight:bold;
                padding:14px 31px;
                height: 100px;
                text-decoration:none;
                text-shadow:0px 1px 0px #5b8a3c;
            }
            [data-testid="baseButton-primary"]:hover {
                # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                background-color:#72b352;
                background-color: black;
                cursor: arrow;
            }
            [data-testid="baseButton-primary"]:active {
                position:relative;
                background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                top:1px;
            }
        }
        """,):
            open_betray = st.button("Trustee betrays", type='primary', use_container_width=True, key="betray")
        with stylable_container(key="move_button", css_styles="""
        {
            [data-testid="baseButton-primary"] {
                box-shadow: 0px 10px 14px -7px #3e7327;
                border-radius:4px;
                border:1px solid #4b8f29;
                background-color: green;
                display:inline-block;
                cursor:pointer;
                color:#ffffff;
                font-family:Arial;
                font-size:13px;
                font-weight:bold;
                padding:14px 31px;
                height: 100px;
                text-decoration:none;
                text-shadow:0px 1px 0px #5b8a3c;
            }
            [data-testid="baseButton-primary"]:hover {
                # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                background-color:#72b352;
                background-color: green;
                cursor: arrow;
            }
            [data-testid="baseButton-primary"]:active {
                position:relative;
                background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                top:1px;
            }
        }
        """,):
            open_move = st.button("Trustee moves", type='primary', use_container_width=True, key="move")

        if open_betray:
            betray.open()
            
        if open_move:
            modal.open(src=src_100K)
    
    st.divider()
            
    st.header("Outcome:")
    # Display payoffs for both players based on the bank's decision and trust level
    
    st.divider()
    st.header("Visualisation:")
    st.markdown("`Red flags denote bets against the investor.`")
    st.write("If you wish to send us a donation, just bet against us.")
    
    col1, _, col2 = st.columns([1, .3, 1])
    
        
    with col1:

        with stylable_container(key="bet2_button", css_styles="""
        {
            [data-testid="baseButton-primary"] {
                box-shadow: 0px 10px 14px -7px #3e7327;
                background-image:url("data/qrcode_1.png") fixed center;
                border-radius:4px;
                border:1px solid #4b8f29;
                display:inline-block;
                cursor:pointer;
                color:#ffffff;
                font-family:Arial;
                font-size:13px;
                font-weight:bold;
                padding:14px 31px;
                height: 300px;
                text-decoration:none;
                text-shadow:0px 1px 0px #5b8a3c;
            }
            [data-testid="baseButton-primary"]:hover {
                # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                background-color:#72b352;
                background-color: yellow;
                cursor: arrow;
            }
            [data-testid="baseButton-primary"]:active {
                position:relative;
                background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                top:1px;
            }
        }
        """,):
            # st.button("button", type='primary', on_click=foo, use_container_width=True, key="_payment")
            open_play = st.button("I bet against", type='primary', use_container_width=True, key="bet2")
    
    with col2:
        with stylable_container(key="bet-_button", css_styles="""
        {
            [data-testid="baseButton-primary"] {
                box-shadow: 0px 10px 14px -7px #3e7327;
                border-radius:4px;
                border:1px solid #4b8f29;
                background-color: black;
                display:inline-block;
                cursor:pointer;
                color:#ffffff;
                font-family:Arial;
                font-size:13px;
                font-weight:bold;
                padding:14px 31px;
                height: 300px;
                text-decoration:none;
                text-shadow:0px 1px 0px #5b8a3c;
            }
            [data-testid="baseButton-primary"]:hover {
                # background:linear-gradient(to bottom, #72b352 5%, #77b55a 100%);
                background-color:#72b352;
                background-color: black;
                cursor: arrow;
            }
            [data-testid="baseButton-primary"]:active {
                position:relative;
                background:linear-gradient(to bottom, #77b55a 5%, #72b352 100%);
                top:1px;
            }
        }
        """,):
            open_betray = st.button("I bet pro", type='primary', use_container_width=True, key="bet-")
    generate_random_plots()
    st.divider()
    # matrix_placeholder = st.empty()

    # while True:
    #     # Generate and display random matrix
    #     random_matrix = generate_random_matrix(N)
    #     matrix_placeholder.dataframe(random_matrix)

    #     # Refresh and reshuffle matrix every given interval
    #     time.sleep(refresh_interval)

    # while True:
    #     # Generate random matrix
    #     random_matrix = generate_random_matrix(N)

    #     # Plot random matrix
    #     plot_random_matrix(random_matrix)

    #     # Refresh and reshuffle matrix every given interval
    #     st.text("Refreshing matrix in {} seconds...".format(refresh_interval))
    #     matrix_placeholder.empty()
        

if __name__ == "__main__":
    main()
