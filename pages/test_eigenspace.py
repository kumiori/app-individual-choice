import streamlit as st
import sympy as sp
import numpy as np
import plotly.express as px

if st.secrets["runtime"]["STATUS"] == "Production":
    st.set_page_config(
        page_title="Celestial Verse Portal",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

st.write(st.secrets["runtime"]["STATUS"])

if 'parameters' not in st.session_state:
    st.session_state.parameters = {}

def solve_eigenspace_vector(parameters, idx = 0):
    x = sp.symbols('x', real=True)
    v = sp.Function('v', real=True)(x)
    β = sp.Function('β', real=True)(x)
    C, A = sp.symbols('C A')
    
    a = parameters["a"]
    b = parameters["b"]
    c = parameters["c"]    
    
    if b * c**2 < sp.pi**2 * a:
        st.write('case 1')
        _subs = {A: 0}
        A = 0
    elif b * c**2 > sp.pi**2 * a:
        st.write('case 2')
        _subs = {C: 0}
        C = 0
    
    β = C + A*sp.cos(sp.pi * x)
    v = c * A / sp.pi * sp.sin(sp.pi * x)

    depends_on_A = np.any([sp.symbols('A') in expression.free_symbols for expression in [v, β]])
    depends_on_C = np.any([sp.symbols('C') in expression.free_symbols for expression in [v, β]])
    
    _norm = sp.sqrt(np.sum([sp.integrate(eigenfunction**2, (x, 0, 1)) for eigenfunction in (v, β)]))

    print([expression.free_symbols for expression in [v, β]])
    print(_norm, depends_on_A, depends_on_C)
    
    if depends_on_A:
        print('depends_on_A')
        _normalise = [{sp.symbols('A'): ay} for ay in sp.solve(_norm - 1, A)]
    elif depends_on_C:
        print('depends_on_C')
        _normalise = [{sp.symbols('C'): cy} for cy in sp.solve(_norm - 1, C)]
    # print(_normalise)
    
    # return (v.subs(_normalise[idx]), β.subs(_normalise[idx])), _normalise
    st.write({"v": v.subs(_normalise[idx]), "β": β.subs(_normalise[idx]), "D": 0})
    return {"v": v.subs(_normalise[idx]), "β": β.subs(_normalise[idx]), "D": 0}

def solve_eigenspace_cone(parameters, idx = 0):
    x = sp.symbols('x', real=True)
    v = sp.Function('v', real=True)(x)
    β = sp.Function('β', real=True)(x)
    C, A = sp.symbols('C A')
    
    a = parameters["a"]
    b = parameters["b"]
    c = parameters["c"]    
    D = 0
    
    if b * c**2 < sp.pi**2 * a:
        print('case 1')
        β = C
        
    elif b * c**2 > sp.pi**2 * a:
        print('case 2')
        # D = sp.symbols('D')
        D = (sp.pi**2 * a / (b * c**2))**(1/3)
        β = sp.Piecewise(
            (C *(1 + sp.cos(sp.pi * x / D)), (0 <= x) & (x <= D)),
            (0, True)
            )
        
        _min = (np.pi**2 * a)**(1/3) * (b * c**2)**(2/3)
        
    elif b * c**2 == sp.pi**2 * a:
        print('case eq')
        _min = b * c**2
        _subs = {C: 0}
        C = 0
        β = C + A*sp.cos(sp.pi * x)
        # abs(A) < C
    
    depends_on_A = sp.symbols('A') in β.free_symbols
    depends_on_C = sp.symbols('C') in β.free_symbols
    depends_on_D = sp.symbols('D') in β.free_symbols
    
    _norm = sp.sqrt(sp.integrate(β**2, (x, 0, 1)))

    # print([expression.free_symbols for expression in [v, β]])
    print(_norm)
    
    if depends_on_A:
        print('depends_on_A')
        _normalise = [{sp.symbols('A'): ay} for ay in sp.solve(_norm - 1, A)]
    elif depends_on_C:
        print('depends_on_C')
        _normalise = [{sp.symbols('C'): cy} for cy in sp.solve(_norm - 1, C) if cy > 0]
    elif depends_on_D:
        print('depends_on_D')
    
    return {"v": 0, "β": β.subs(_normalise[idx]), "D": D}

def book_of_the_numbers():
    """This function, formerly called `fuck_dgsi`, invokes the book of the numbers
    to get three real quantities, according to the scriptures.
    
    @article{pham:2011-the-issues,
        author = {Pham, Kim and Marigo, Jean-Jacques and Maurini, Corrado},
        date-added = {2015-08-24 14:23:19 +0000},
        date-modified = {2022-08-10 11:03:49 +0200},
        journal = {Journal of the Mechanics and Physics of Solids},
        number = {6},
        pages = {1163--1190},
        publisher = {Elsevier},
        title = {The issues of the uniqueness and the stability of the homogeneous response in uniaxial tests with gradient damage models},
        volume = {59},
        year = {2011},
        }
        
    Fuck Elsevier.
    
    """
    while True:
        a = np.random.rand()
        b = np.random.rand()*3
        c = (np.random.choice([-1, 1], 1) * np.random.rand(1))[0]*3  # Generate three random numbers between 0 and 1

        # Check conditions
        if a > 0 and b > 0 and c != 0:
            break

    return {"a": a, "b": b, "c": c}

def main():
    st.title("Eigenspace Explorer")
    st.markdown("Consider this: We solve a difficult problem and we do it for ________. (Fill the blank)")
    # Parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        a = st.slider("a", 0.0, 10.0, 1.0)
    with col2:
        b = st.slider("b", 0.0, 10.0, 1.0)
    with col3:
        c = st.slider("c", -10.0, 10.0, 1.0)
    parameters = {"a": a, "b": b, "c": c}

    # Button to generate random numbers
    if st.button("Generate Random Numbers"):
        parameters = book_of_the_numbers()
        st.session_state.parameters = parameters
        st.write(f"Generated Parameters: {parameters}")
        st.write('`Remark: Parameters are generated from the book of the numbers. You should have received a copy...`')
    else:
        st.write(f"Custom Parameters: {parameters}")
        st.session_state.parameters = parameters
    
    st.write(f'This is the competition:')

    if 'a' in st.session_state.parameters:
        a, b, c = st.session_state.parameters["a"], st.session_state.parameters["b"], st.session_state.parameters["c"]
    st.markdown(f'# <center>$bc^2$ `{np.around(b*c**2, 1)}` vs. $\pi a^2$ `{np.around(np.pi**2 * a, 1)}`</center>', unsafe_allow_html=True)
    st.markdown(f'# <center>|supp| = $(\pi^2 a / (bc^2))^{{1 / 3}}$ `{np.around((np.pi**2 * a / (b * c**2))**(1/3), 1)}` or $0$</center>', unsafe_allow_html=True)
    st.write(st.session_state.parameters)

    
    space_choice = st.radio("Choose Space", ["Vector Space", "Convex Set"], horizontal=True)
    if st.button("Compute Eigenspace"):
        st.markdown(f"$bc^2$ = {np.around(b*c**2, 2)}, \
                    $\pi^2  a$ = {np.around(np.pi**2 * a, 2)}")
        
        if space_choice == "Vector Space":
            eigenspace = solve_eigenspace_vector(st.session_state.parameters)
            v, β = eigenspace["v"], eigenspace["β"]
            D = eigenspace["D"]
            
        elif space_choice == "Convex Set":
            eigenspace = solve_eigenspace_cone(st.session_state.parameters)
            v, β = eigenspace["v"], eigenspace["β"]
            D = eigenspace["D"]
            
        # st.write(f"v = {v}")
        # st.write(f"β = {β}")
        # Sample points for visualization
        x_values = np.linspace(0, 1, 100)
        v_function = sp.lambdify('x', v)
        β_function = sp.lambdify('x', β)

        v_values = [v_function(x) for x in x_values]
        β_values = [float(β_function(x)) for x in x_values]
        _β_values = [float(β_function(1-x)) for x in x_values]
        # Plotting
        _D = float(sp.N(D))
        fig = px.line(x=x_values, y=[v_values, β_values, _β_values],
                    labels={'value': 'Function Value', 'x': 'x'},
                    title=f'Eigenspace Functions in {space_choice} with D={np.around(_D, 2)}')

        _layout = dict(xaxis=dict(title='x',
                        tickvals=[0, 1, _D],
                        ticktext=['0', '1', 'D']), 
                    yaxis=dict(title='Function Value',
                        tickvals=[0, 1]))
        fig.update_layout(_layout)
        fig.update_traces(opacity=0.4, selector=dict(name='Identity'))

        # Show plot
        st.plotly_chart(fig)

if __name__ == '__main__':
    main()