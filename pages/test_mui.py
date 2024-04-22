from streamlit_elements import elements
from streamlit_elements import mui, html
import streamlit as st


# Define the steps for the stepper
steps = ["Step 1", "Step 2", "Step 3"]

# Display the stepper
with elements("example_stepper"):
    with mui.Stepper(activeStep=2, alternativeLabel=True):
        for label in steps:
            with mui.Step:
                mui.StepLabel(label, completed = False)
                
# Display the stepper
with elements("example_stepper_2"):
    with mui.Stepper(activeStep=0, alternativeLabel=False):
        for label in steps:
            with mui.Step:
                mui.StepLabel(label, completed = False)
                
# Define the steps for the stepper
steps = [
    {
        "label": "Select campaign settings",
        "description": "For each ad campaign that you create, you can control how much "
                       "you're willing to spend on clicks and conversions, which networks "
                       "and geographical locations you want your ads to show on, and more."
    },
    {
        "label": "Create an ad group",
        "description": "An ad group contains one or more ads which target a shared set of keywords."
    },
    {
        "label": "Create an ad",
        "description": "Try out different ad text to see what brings in the most customers, "
                       "and learn how to enhance your ads using features like ad extensions. "
                       "If you run into any problems with your ads, find out how to tell if "
                       "they're running and how to resolve approval issues."
    }
]

# Define a function to handle the next step
def handle_next():
    st.session_state.active_step += 1

# Define a function to handle going back to the previous step
def handle_back():
    st.session_state.active_step -= 1

# Define a function to reset the stepper
def handle_reset():
    st.session_state.active_step = 0

# Initialize session state
if "active_step" not in st.session_state:
    st.session_state.active_step = 0

# Display the vertical stepper
with elements("vertical_stepper"):
    with mui.Box(sx={"maxWidth": 400}):
        with mui.Stepper(activeStep=st.session_state.active_step, orientation="vertical"):
            for index, step in enumerate(steps):
                with mui.Step:
                    mui.StepLabel(step["label"])
                    with mui.StepContent:
                        mui.Typography(step["description"])
                        # with mui.Box(sx={"mb": 2}):
                        #     with mui.Typography:
                        #         mui.Button(
                        #             variant="contained",
                        #             onclick=handle_next,
                        #             disabled=index == len(steps) - 1,
                        #             sx={"mt": 1, "mr": 1}
                        #         )
                        #         mui.Button(
                        #             "Back",
                        #             onclick=handle_back,
                        #             disabled=index == 0,
                        #             sx={"mt": 1, "mr": 1}
                        #         )

# Display completion message and reset button
if st.session_state.active_step == len(steps):
    with mui.Paper(square=True, elevation=0, sx={"p": 3}):
        st.markdown("All steps completed - you're finished")
        mui.Button("Reset", onclick=handle_reset, sx={"mt": 1, "mr": 1})
        
        

# Define the content for the card
def render_card():
    with mui.Card(sx={"width": 300}):
        with mui.CardContent:
            mui.Typography("Word of the Day", sx={"fontSize": 14}, color="text.secondary", gutterBottom=True)
            mui.Typography("be•nev•o•lent", variant="h5", component="div")
            mui.Typography("/ˈbɛnɪvələnt/")
            mui.Typography("adjective", sx={"mb": 1.5}, color="text.secondary")
            mui.Typography(
                "well meaning and kindly.")
            mui.Typography(
                '"A benevolent smile"',
                variant="body2",
                dangerously_set_inner_html=True
            )
        with mui.CardActions:
            mui.Button("Learn More", size="small")

# Display the card
with elements("basic_card"):
    render_card()


# Define the circular progress with label component
def CircularProgressWithLabel(props):
    return mui.Box(sx={"position": "relative", "display": "inline-flex"})(
        mui.CircularProgress(variant="determinate", **props),
        mui.Box(
            sx={
                "top": 0,
                "left": 0,
                "bottom": 0,
                "right": 0,
                "position": "absolute",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
            }
        )(
            mui.Typography(
                f"{round(props['value'])}%", variant="caption", component="div", color="text.secondary"
            )
        ),
    )

# Display the circular progress with label
with elements("circular_progress"):
    progress_value = st.slider("Progress Value", 0, 100, 0, 1)
    CircularProgressWithLabel(props={"value": progress_value})
    # for t in range(0, 101, 10):
    #     CircularProgressWithLabel(props={"value": t})



def SwipeableTextMobileStepper():
    # Define the images and other necessary variables
    images = [
        {
            "label": "San Francisco – Oakland Bay Bridge, United States",
            "imgPath": "https://imgur.com/TgDpuc7",
        },
        {
            "label": "Bird",
            "imgPath": "https://images.unsplash.com/photo-1538032746644-0212e812a9e7?auto=format&fit=crop&w=400&h=250&q=60",
        },
        {
            "label": "Bali, Indonesia",
            "imgPath": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=400&h=250",
        },
        {
            "label": "Goč, Serbia",
            "imgPath": "https://images.unsplash.com/photo-1512341689857-198e7e2f3ca8?auto=format&fit=crop&w=400&h=250&q=60",
        },
    ]
    session_state = st.session_state

    # Initialize activeStep variable in session state
    if 'activeStep' not in session_state:
        session_state.activeStep = 0

    maxSteps = len(images)

    # Initialize session state
    if "direction" not in st.session_state:
        st.session_state.direction = "ltr"  # Default direction is left-to-right

    # Define the function to handle next step
    def handleNext():
        session_state.activeStep = (session_state.activeStep + 1) % maxSteps

    # Define the function to handle previous step
    def handleBack():
        session_state.activeStep = (session_state.activeStep - 1) % maxSteps

    # Display the component
    with elements("stepper"):
        mui.Paper(
            square=True,
            elevation=0,
            sx={
                "display": "flex",
                "alignItems": "center",
                "height": 50,
                "pl": 2,
                "bgcolor": "background.default",
            },
        )(images[session_state.activeStep]["label"])

        mui.Box(sx={"maxWidth": 400, "flexGrow": 1})(
            mui.Box(
                component="img",
                sx={
                    # "height": 255,
                    "display": "block",
                    "minWidth": 700,
                    "overflow": "hidden",
                    "width": "100%",
                },
                src=images[session_state.activeStep]["imgPath"],
                alt=images[session_state.activeStep]["label"],
            ),
        )

        mui.MobileStepper(
            variant="progress",
            steps=maxSteps,
            position="static",
            activeStep=session_state.activeStep,
            nextButton=mui.Button(
                size="small",
                onClick=handleNext,
                disabled=session_state.activeStep == maxSteps - 1,
            )(
                "Next",
                mui.icon.KeyboardArrowLeft() if st.session_state.direction == "rtl" else mui.icon.KeyboardArrowRight(),
            ),
            backButton=mui.Button(
                size="small", onClick=handleBack, disabled=session_state.activeStep == 0
            )(
                mui.icon.KeyboardArrowRight() if st.session_state.direction == "rtl" else mui.icon.KeyboardArrowLeft(),
                "Back",
            ),
        )

# Display the SwipeableTextMobileStepper component
SwipeableTextMobileStepper()

def basic_tooltip():
    with elements("basic-tooltip"):
        mui.Tooltip("Delete")
        # mui.icon_button(icon="delete")

# st.write(mui)
# basic_tooltip()