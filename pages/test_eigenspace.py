import streamlit as st
import sympy as sp
import numpy as np
import plotly.express as px
import pages


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
    st.write({"v": v.subs(_normalise[idx]), "β": β.subs(_normalise[idx]), "D": 1})
    return {"v": v.subs(_normalise[idx]), "β": β.subs(_normalise[idx]), "D": 1}

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
    st.title("A Fundamental problem, which we solve(d)")
    
    st.markdown(f'# <center>$\min \mathcal R(v, \\beta)$ in $V$ and $K^+_0$</center>', unsafe_allow_html=True)
    # st.markdown(f'# <center>$\mathcal R(v, \\beta):=\int_0^1$</center>', unsafe_allow_html=True)
    st.markdown(f'# <center>where</center>', unsafe_allow_html=True)
    st.markdown(r"### <center>$\mathcal R(v, \beta):=\dfrac{\int_0^1 \textcolor{red}{a}\beta'^2 dx+\int_0^1 \textcolor{red}b(v' -\textcolor{red}c\beta)^2dx}{\int_0^1\beta^2dx}$</center>", unsafe_allow_html=True)
    st.markdown(f'### well defined for $v, \\beta$ in $H^1(0, 1)$ when extended to $+\infty$ if $\\beta=0,$', unsafe_allow_html=True)
    st.markdown(f'# <center>and</center>', unsafe_allow_html=True)
    st.markdown(r'### $V := H^1_0(0, 1) \times H^1(0, 1)$', unsafe_allow_html=True)
    st.markdown(r'### $K^+_0 := H^1_0(0, 1) \times \{ \beta \in H^1(0, 1): \beta\geq 0 \}$', unsafe_allow_html=True)
    st.markdown(f'### are the energy (minimisation) spaces: a vector space and a convex set,', unsafe_allow_html=True)
    st.markdown(f'# <center>and</center>', unsafe_allow_html=True)
    st.markdown(r'### $\beta, v:x \mapsto \mathbb R$ are real <em>fields</em>, whereas $\textcolor{red}a, \textcolor{red}b > 0$, and $\textcolor{red}c\neq 0$ are <em>real</em> quantities. Is this good business?', unsafe_allow_html=True)
    
    st.title("Rationale, to be understood")
    """
    The variational quotient defiend above, often referred to as the Rayleigh ratio, is a fundamental concept that plays a crucial role in the study of stability and instabilities, in the context of the analysis of (nonlinear) complex systems. Named after `Lord Rayleigh`, it is used to estimate the lowest eigenvalue of a functional operator, and it plays a crucial role to assess the uniqueness of evolution paths and the stability of states.
    
    In the context of stability analysis for constrained (irreversible) systems, particularly in the study of multiscale, nonconvex, nonlinear systems, we exploit the Rayleigh quotient to estimate the stability of (critical) equilibrium points along their manifold paths. For a nonlinear system represented by an energy $E$ (a real scalar associated to all of its configurations), the stability of the system is closely related to the sign of minimal eigenvalue of $E''$, roughly speaking, the curvature of the energy landscape.
    
    The Rayleigh quotient provides a quantitative measure that aids in understanding the stability of complex systems, making it an essential concept in theoretical investigations and scientific computations.
    """
    
    st.title("The solution strategy")
    """
    We solve the problem above in full generality in the one-dimensional case, leaving the specification of the energy (and hence the constants a, b, c) to the applications. In our view, the latter concern fundamental questions arising from solid mechanics, economy, biology, game theory, and quantum physics. We consider the two cases: the minimisation in the vector space $V$ and in the convex cone $K^+_0$.
    
    
    ### How we attack:
    
    1. First, establish existence of the minimum in $V$ and $K^+_0$
        - use the compactness of the embedding $H^1 \\hookrightarrow L^2$, coercivity, and lower semicontinuity
    1. The minimum is attained by an admissible pair $(v_*, \\beta_*)$
    1. Establish that the minimum is strictly positive, that is $\mathsf R := \mathcal R(v_*, \\beta_*) > 0$
    1. Next, eliminate $v$ solving $v_* = \\argmin {\\mathcal R}(\cdot, \\beta)$
    and obtain new functional $\\beta \mapsto \\hat{\\mathcal R}(\\beta):={\\mathcal R}(v_*, \\beta)$ to be minimised.
    1. Minimisation of $\\hat{\\mathcal R}$ over $H^1$ is done solving the associated Euler-Lagrange equation and standard arguments. Accordingly, there exist two possibilities:
        - Either ... or ...
    1. We thus determine the minimum of $\\mathcal R$ in $V$ and the eigenspace.
    1. Minimisation of $\\hat{\\mathcal R}$ over $K^+_0$ is done solving a variational _inequality_, which is a bit more involved. 
    """
    
    st.title("The solution of a (large) inequality, or, where the real competition is?")
    
    """
    ### We solve the minimisation problem in the convex cone $K^+_0$.
    1. Let $\\beta_*$ be a minimiser, it satisfies the variational inequality:
    ### $$ \hat {\mathcal R}'(\\beta_*)(\\beta)\geq 0, \\forall \\beta \in K^+_0 $$
    the equality holds if and only if $\\beta_*$ is a minimiser.
    
    2. Establish regularity of minimiser ($H^2(0, 1)$) or assume continuous differentiability.
    1. Obtain a (local) inequality in $(0, 1)$ and (natural) boundary conditions.
    1. Interpretation of the variational inequality as a differential equation.
    1. The minimiser is supported on a nontrivial open interval $I\\subseteq (0, 1)$, which can be internal or touch the boundary.
    1. Due to regularity and the fact that $\\beta_*$ is non-negative, $\\beta'_* = 0$ where $\\beta_*$ vanishes.
    1. Thus, $\\beta_*$ satisfies
    $$
    \\beta_*(x)> 0, a\\beta_*''(x) + \mathsf{R} \\beta_*(x) = b c^2 \\langle \\beta_*\\rangle, x \in I_i  
    $$
    where $I_i$ is any connected component of the support of $\\beta_*$.
    $$
    \\beta'_*(x)=0, \\text{ on } \\partial I_i  
    \\text{ and }
    \\beta_*(x)=0, \\text{ on } \\partial I_i \\text{ if } I_i \\subset (0, 1).
    $$
    1. At this point, there are several possibilities:
        - that the support, say $I$, is well included in $(0, 1), |I|=:D<1$
        - that the support touches one boundary, say the left, or $I = (0, D), D < 1$
        - that the support is full and $\\beta_*>0$ at the boundaries, or $I = (0, 1)$
        - all symmetric cases obtained by changing $x\\mapsto 1-x$

    """
    st.title("We propose...")
    
    st.markdown("### Proposition 1. (Minimisation over $V$)", unsafe_allow_html=True)
    st.write("🥁The minimum is ... and the minimisers are ... 💫")
    st.markdown("### Proposition 2. (Minimisation over $K^*_0$)", unsafe_allow_html=True)
    st.write("🥁The minimum is ... and the minimisers are ... 💫")
    
    
    st.title("Eigenspace Explorer")
    st.markdown("Consider this: we solve a difficult problems and we do it for fun.")
    # Parameters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("# <center>a</center>", unsafe_allow_html=True)
        a = st.slider("a", 0.0, 10.0, 1.0)
    with col2:
        st.markdown("# <center>b</center>", unsafe_allow_html=True)
        b = st.slider("b", 0.0, 10.0, 1.0)
    with col3:
        st.markdown("# <center>c</center>", unsafe_allow_html=True)
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
    
    st.write(f'## This is the real competition:')

    if 'a' in st.session_state.parameters:
        a, b, c = st.session_state.parameters["a"], st.session_state.parameters["b"], st.session_state.parameters["c"]
    st.markdown(f'# <center>$bc^2$ `{np.around(b*c**2, 1)}` vs. $\pi a^2$ `{np.around(np.pi**2 * a, 1)}`</center>', unsafe_allow_html=True)
    _supp_D = min(np.around((np.pi**2 * a / (b * c**2))**(1/3), 1), 1)
    st.markdown(f'# <center>|supp| = $(\pi^2 a / (bc^2))^{{1 / 3}}$ =`{_supp_D}`</center>', unsafe_allow_html=True)
    triviality_condition = b*c**2 < np.pi**2 * a
    
    st.write(f"## Triviality Condition is $bc^2 < \pi^2 a$ = `{triviality_condition}`")
    st.write('Check the parameters')
    st.json(st.session_state.parameters, expanded=False)
    
    space_choice = st.radio("Choose the minimisation space", ["Vector Space", "Convex Set"], horizontal=True)
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
                    labels={'v_values': 'v', 'β_values': 'β'},
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