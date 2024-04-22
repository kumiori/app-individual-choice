import streamlit.components.v1 as components
import streamlit as st

st.text("Hello")

_qualitative_selector = components.declare_component(
    "qualitative",
    url='http://localhost:3001'
)


def dichotomy(name, question, rotationAngle = 0, gradientWidth = 40, invert = False, shift = 0, key=None):
    return _qualitative_selector(component = "dichotomy",
    name = name,
    key=key,
    question = question,
    rotationAngle = rotationAngle,
    gradientWidth = gradientWidth,
    invert = invert,
    shift = shift
    )


def qualitative(name, question, data_values, key=None):
    return _qualitative_selector(component = "qualitative",
    name = name,
    key=key,
    data_values = data_values,
    question = question)

def qualitative_parametric(name, question, areas, key=None):
    return _qualitative_selector(component = "parametric",
    name = name,
    key=key,
    areas = areas,
    data_values  = [1, 3, 10],
    question = question)

def main():

    return_value = dichotomy(name = "Spirit", question = "Dychotomies, including time...", key = "boundaries")
    st.write('You picked', return_value)

    # return_value = dichotomy(name = "Spirit", question = "Dychotomies, including time...", key = "thickness",
    #                          gradientWidth=10)
    # st.write('You picked', return_value)

    return_value = dichotomy(name = "Spirit", question = "Dychotomies, including time...", key = "perspective",
                            rotationAngle=10,
                            gradientWidth=30)

    st.write('You picked', return_value)

    return_value = dichotomy(name = "Spirit", question = "Dychotomies, including time...", key = "invert",
                            rotationAngle=10,
                            gradientWidth=50,
                            invert=True,
                            #  invert=False,
                            )
    st.write('You picked', return_value)


    return_value = dichotomy(name = "Spirit", question = "Dychotomies, including time...", key = "nuances",
                            gradientWidth=100,
                            shift = 0)
    st.write('You picked', return_value)


    return_value = qualitative_parametric(name = "Spirit",
        question = "Boundaries matter, see below...",
        areas = 3,
        key = "parametric")
    st.write('You picked', return_value)



    return_value = qualitative(name = "Spirit", question = "How tricky is Quantity?", data_values = [1, 10, 100, 0.1], key = "qualitative")
    st.write('You picked', return_value)


# Run the cosmic app
if __name__ == "__main__":
    main()
