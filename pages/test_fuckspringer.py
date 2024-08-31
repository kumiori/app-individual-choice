import streamlit as st
import pandas as pd

# Connect to the SQLite database

# Retrieve the list of all journals

journals_list = [
    {
        "name": "Journal of the Mechanics and Physics of Solids (JMPS)",
        "publishing_company": "Elsevier",
        "scope": "Publishes research on the mechanics of solids, including fracture mechanics, plasticity, and material stability.",
        "relevance": "Numerical stability and phase field modeling",
    },
    {
        "name": "Computer Methods in Applied Mechanics and Engineering (CMAME)",
        "publishing_company": "Elsevier",
        "scope": "Covers new methods and computational techniques in mechanics, including fracture modeling.",
        "relevance": "Numerical stability issues",
    },
    {
        "name": "Journal of Computational Physics",
        "publishing_company": "Elsevier",
        "scope": "Publishes papers on computational techniques and their applications, especially those related to physical systems.",
        "relevance": "Computational aspects of the phase field model",
    },
    {
        "name": "International Journal of Fracture",
        "publishing_company": "Springer",
        "scope": "Dedicated to the field of fracture mechanics, including both theoretical and applied research.",
        "relevance": "Fracture phenomena",
    },
    {
        "name": "International Journal for Numerical Methods in Engineering (IJNME)",
        "publishing_company": "Wiley",
        "scope": "Covers numerical methods and their applications in engineering, particularly those involving mechanical problems.",
        "relevance": "Numerical stability",
    },
    {
        "name": "Journal of Applied Mechanics (ASME)",
        "publishing_company": "ASME",
        "scope": "Covers a broad range of topics in applied mechanics, including computational mechanics and fracture.",
        "relevance": "Applied mechanics principles",
    },
    {
        "name": "Mechanics of Materials",
        "publishing_company": "Elsevier",
        "scope": "Publishes on the mechanics of materials, including fracture and phase transitions.",
        "relevance": "Material behavior in phase field model",
    },
    {
        "name": "Engineering Fracture Mechanics",
        "publishing_company": "Elsevier",
        "scope": "Specializes in the mechanics of fracture and failure in engineering materials and structures.",
        "relevance": "Engineering applications of fracture",
    },
    {
        "name": "Acta Materialia",
        "publishing_company": "Elsevier",
        "scope": "Publishes research on the structure and properties of materials, with a strong emphasis on mechanics and fracture.",
        "relevance": "Material science aspects",
    },
    {
        "name": "European Journal of Mechanics A/Solids",
        "publishing_company": "Elsevier",
        "scope": "Focuses on the mechanics of solids, with applications in various fields including materials science.",
        "relevance": "Solid mechanics applications",
    },
]

journal_list = [
    (1, 'Journal of the Mechanics and Physics of Solids (JMPS)', 'Elsevier', 
     'Publishes research on the mechanics of solids, including fracture mechanics, plasticity, and material stability.', 
     None, None, None, None),
    
    (2, 'Computer Methods in Applied Mechanics and Engineering (CMAME)', 'Elsevier', 
     'Covers new methods and computational techniques in mechanics, including fracture modeling.', 
     None, None, None, None),
    
    (3, 'Journal of Computational Physics', 'Elsevier', 
     'Publishes papers on computational techniques and their applications, especially those related to physical systems.', 
     None, None, None, None),
    
    (4, 'International Journal of Fracture', 'Springer', 
     'Dedicated to the field of fracture mechanics, including both theoretical and applied research.', 
     None, None, None, None),
    
    (5, 'International Journal for Numerical Methods in Engineering (IJNME)', 'Wiley', 
     'Covers numerical methods and their applications in engineering, particularly those involving mechanical problems.', 
     None, None, None, None),
    
    (6, 'Journal of Applied Mechanics (ASME)', 'ASME', 
     'Covers a broad range of topics in applied mechanics, including computational mechanics and fracture.', 
     None, None, None, None),
    
    (7, 'Mechanics of Materials', 'Elsevier', 
     'Publishes on the mechanics of materials, including fracture and phase transitions.', 
     None, None, None, None),
    
    (8, 'Engineering Fracture Mechanics', 'Elsevier', 
     'Specializes in the mechanics of fracture and failure in engineering materials and structures.', 
     None, None, None, None),
    
    (9, 'Acta Materialia', 'Elsevier', 
     'Publishes research on the structure and properties of materials, with a strong emphasis on mechanics and fracture.', 
     None, None, None, None),
    
    (10, 'European Journal of Mechanics A/Solids', 'Elsevier', 
     'Focuses on the mechanics of solids, with applications in various fields including materials science.', 
     None, None, None, None)
]
# Convert the data into a pandas DataFrame
df = pd.DataFrame(journal_list, columns=["JournalID", "Name", "PublishingCompany", "Scope", "ImpactFactor", "HIndex", "AverageReviewTime", "AverageAcceptanceTime"])

# Close the connection

# Streamlit app layout
st.title("Journal Database")

st.write("This app displays a list of journals relevant to the phase field model of fracture.")

# Display the DataFrame in Streamlit
st.dataframe(df)

# Option to filter journals by name
journal_filter = st.text_input("Filter journals by name:")
if journal_filter:
    filtered_df = df[df['Name'].str.contains(journal_filter, case=False)]
    st.write(f"Filtered results for: {journal_filter}")
    st.dataframe(filtered_df)
else:
    st.write("Showing all journals")
    st.dataframe(df)