import streamlit as st
import pandas as pd
journal_list = [
    (1, 'Journal of the Mechanics and Physics of Solids (JMPS)', 'Elsevier', 
     'Publishes research on the mechanics of solids, including fracture mechanics, plasticity, and material stability.', 
     None, None, None, 'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids'),
    
    (2, 'Computer Methods in Applied Mechanics and Engineering (CMAME)', 'Elsevier', 
     'Covers new methods and computational techniques in mechanics, including fracture modeling.', 
     None, None, None, 'https://www.sciencedirect.com/journal/computer-methods-in-applied-mechanics-and-engineering'),
    
    (3, 'Journal of Computational Physics', 'Elsevier', 
     'Publishes papers on computational techniques and their applications, especially those related to physical systems.', 
     None, None, None, 'https://www.sciencedirect.com/journal/journal-of-computational-physics'),
    
    (4, 'International Journal of Fracture', 'Springer', 
     'Dedicated to the field of fracture mechanics, including both theoretical and applied research.', 
     None, None, None, 'https://www.springer.com/journal/10704'),
    
    (5, 'International Journal for Numerical Methods in Engineering (IJNME)', 'Wiley', 
     'Covers numerical methods and their applications in engineering, particularly those involving mechanical problems.', 
     None, None, None, 'https://onlinelibrary.wiley.com/journal/10970207'),
    
    (6, 'Journal of Applied Mechanics (ASME)', 'ASME', 
     'Covers a broad range of topics in applied mechanics, including computational mechanics and fracture.', 
     None, None, None, 'https://asmedigitalcollection.asme.org/appliedmechanics'),
    
    (7, 'Mechanics of Materials', 'Elsevier', 
     'Publishes on the mechanics of materials, including fracture and phase transitions.', 
     None, None, None, 'https://www.sciencedirect.com/journal/mechanics-of-materials'),
    
    (8, 'Engineering Fracture Mechanics', 'Elsevier', 
     'Specializes in the mechanics of fracture and failure in engineering materials and structures.', 
     None, None, None, 'https://www.sciencedirect.com/journal/engineering-fracture-mechanics'),
    
    (9, 'Acta Materialia', 'Elsevier', 
     'Publishes research on the structure and properties of materials, with a strong emphasis on mechanics and fracture.', 
     None, None, None, 'https://www.sciencedirect.com/journal/acta-materialia'),
    
    (10, 'European Journal of Mechanics A/Solids', 'Elsevier', 
     'Focuses on the mechanics of solids, with applications in various fields including materials science.', 
     None, None, None, 'https://www.sciencedirect.com/journal/european-journal-of-mechanics-a-solids')
]

# Convert the data into a pandas DataFrame
df = pd.DataFrame(journal_list, columns=["JournalID", "Name", "PublishingCompany", "Scope", "ImpactFactor", "HIndex", "AverageReviewTime", "URL"])


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