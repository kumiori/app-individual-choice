import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Atelier sur l'Évolution de la Cryosphère",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize a DataFrame to store survey responses
survey_responses = pd.DataFrame(columns=['Nom', 'Email', 'Intérêt pour l\'Investissement', 'Feedback'])

# Landing Page
def landing_page():
    st.title('Atelier sur l\'Évolution de la Cryosphère')
    st.write(
        "Bienvenue sur le Atelier sur l'Évolution de la Cryosphère. "
        "Explorez les onglets ci-dessous pour en savoir plus et participer."
    )
    # Add any additional landing page content here

# About Us Section
def about_us():
    st.header('À Propos de Nous')
    st.write(
        "L'Alliance StellAzurra est une initiative mondiale dédiée à la promotion des talents, à la stimulation de l'engagement communautaire, "
        "et à la création d'opportunités dans le monde du sport. Notre mission est de construire un écosystème prospère qui habilite "
        "les athlètes, attire les investissements et favorise le sport à l'échelle mondiale."
    )

# Talent Showcase Section (modified to Scientific Showcase)
def scientific_showcase():
    st.header('Vitrine Scientifique')
    st.write(
        "Découvrez les travaux scientifiques exceptionnels présentés lors de l'Atelier sur l'Évolution de la Cryosphère. "
        "Explorez les profils des chercheurs, découvrez leurs réalisations et plongez dans le potentiel de la prochaine génération "
        "de scientifiques de la cryosphère."
    )

# Investment Opportunities Section
def investment_opportunities():
    st.header('Opportunités d\'Investissement')
    st.write(
        "Alors que nous nous lançons dans cette aventure ambitieuse, nous invitons les investisseurs à nous rejoindre. "
        "Explorez les opportunités d'investissement qui correspondent à notre vision et contribuez à l'avenir de l'excellence scientifique."
    )

# Community Engagement Section
def community_engagement():
    st.header('Engagement Communautaire')
    st.write(
        "Notre engagement va au-delà du domaine scientifique. Rejoignez-nous dans divers programmes d'engagement communautaire, d'événements scientifiques et "
        "d'initiatives éducatives. Ensemble, nous pouvons avoir un impact positif et inspirer le changement."
    )

# Researcher Dashboard Section (modified from Investor Dashboard)
def researcher_dashboard():
    st.header('Tableau de Bord du Chercheur')
    st.write(
        "Les chercheurs peuvent accéder à un tableau de bord personnalisé pour suivre les progrès de leurs travaux, "
        "visualiser les métriques de performance et rester informés sur l'impact de leurs contributions."
    )

# ... (other sections remain unchanged)

# Streamlit app with tabs
def main():
    st.title('Atelier sur l\'Évolution de la Cryosphère')

    # Create tabs
    tabs = ["Accueil", "À Propos de Nous", "Opportunités d'Investissement", "Vitrine Scientifique",
            "Engagement Communautaire", "Tableau de Bord du Chercheur", "Tableau de Bord Interactif",
            "Contactez-Nous", "Soutenez-Nous", "Sondage"]

    _tabs = st.tabs(tabs)

    # Display content based on selected tab
    # Iterate over tabs and show content based on selected tab
    for i, selected_tab in enumerate(tabs):
        with _tabs[i]:
            if selected_tab == "Accueil":
                landing_page()
            elif selected_tab == "À Propos de Nous":
                about_us()
            elif selected_tab == "Opportunités d'Investissement":
                investment_opportunities()
            elif selected_tab == "Vitrine Scientifique":
                scientific_showcase()
            elif selected_tab == "Engagement Communautaire":
                community_engagement()
            elif selected_tab == "Tableau de Bord du Chercheur":
                researcher_dashboard()
            elif selected_tab == "Tableau de Bord Interactif":
                researcher_dashboard()
            # elif selected_tab == "Contactez-Nous":
                # contact_us()
            # elif selected_tab == "Soutenez-Nous":
                # support_us()
            # elif selected_tab == "Sondage":
                # survey()

# Run the app
if __name__ == "__main__":
    main()
