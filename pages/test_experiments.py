import os
import pandas as pd
import streamlit as st
import yaml
from streamlit_pills import pills

if 'global_dataframe' not in st.session_state:
    st.session_state.global_dataframe = pd.DataFrame()

# Function to recursively search for parameters.yaml files
def find_parameters_files(folder_path):
    parameters_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "parameters.yaml":
                parameters_files.append(os.path.join(root, file))
    return parameters_files

# Function to filter columns with varying values
def filter_varying_columns(df):
    # Identify columns with varying values
    varying_columns = [col for col in df.columns if df[col].nunique() > 1]
    # Filter the DataFrame to only include these columns
    filtered_df = df[varying_columns]
    return filtered_df

# Function to read parameters.yaml and return as dictionary
def read_parameters_file(file_path):
    with open(file_path, "r") as file:
        parameters_data = yaml.load(file, Loader=yaml.FullLoader)
    return parameters_data

# Function to add parameters to global dataframe
def add_parameters_to_dataframe(parameters_data, dataframe):
    dataframe = dataframe.append(parameters_data, ignore_index=True)
    return dataframe

def load_parameters(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to update the global dataframe
def update_global_dataframe(folder_path):
    parameters_files = find_parameters_files(folder_path)
    dataframe_rows = []

    for parameters_file in parameters_files:
        parameters_data = load_parameters(parameters_file)
        signature_path = os.path.join(os.path.dirname(parameters_file), "signature.md5")
        image_path = os.path.join(os.path.dirname(parameters_file), "traction_state.png")
        
        with open(signature_path, 'r') as sig_file:
            signature = sig_file.read().strip()
        
        # Flatten the parameters_data dictionary and add additional information
        flat_data = {f'{outer_key}.{inner_key}': value 
                     for outer_key, inner_dict in parameters_data.items() 
                     for inner_key, value in inner_dict.items()}
        flat_data['signature'] = signature
        flat_data['file_path'] = parameters_file
        flat_data['image_path'] = image_path
        
        dataframe_rows.append(flat_data)
    
    if dataframe_rows:
        new_dataframe = pd.DataFrame(dataframe_rows)
        st.session_state.global_dataframe = pd.concat([st.session_state.global_dataframe, new_dataframe], ignore_index=True)

# Main function to run the Streamlit app
def main():
    global_dataframe = pd.DataFrame()

    # Set up Streamlit page
    st.title("Parameters.yaml File Search")
    parameters_files = []
    # Create dataframe to store parameters
    parameters_df = pd.DataFrame(columns=["Parameter1", "Parameter2", "Parameter3"]) # Add relevant columns
    
    # Define folder path
    folder_path = "pages/crunch"  # Change this to your desired folder path
    
    # Find parameters.yaml files
    if st.button("Find parameters.yaml files"):
        parameters_files = find_parameters_files(folder_path)
        st.write(f"{len(parameters_files)} parameters.yaml files found")
    # Process each parameters.yaml file found
        parameters_data = read_parameters_file(parameters_files[0])
        st.write(pd.json_normalize(parameters_data))
        parameters_df = pd.DataFrame(pd.json_normalize(parameters_data))  # Convert dict to DataFrame
        st.dataframe(parameters_df)

    def display_filtered_dataframe(dataframe, filter = None):

        # Set the float format for specific columns
        def format_exponential(x):
            return f"{x:.0e}"
        
        # Select columns to be displayed in exponential format
        columns_to_format = ['solvers.damage.snes_atol', 
                             'solvers.damage_elasticity.alpha_rtol', 'stability.cone.cone_atol', 
                             'stability.cone.cone_rtol', 'solver.newton.snes_atol', 'solver.newton.snes_rtol',]
        filtered_varying_df = filter_varying_columns(dataframe)

        # Apply formatting to these columns
        for col in columns_to_format:
            if col in filtered_varying_df.columns:
                print(f"Formatting column: {col}")
                filtered_varying_df[col] = filtered_varying_df[col].apply(format_exponential)
                print(filtered_varying_df[col])
        st.dataframe(filtered_varying_df)


    if st.button("Process parameters.yaml files"):
        progress_bar = st.progress(0)
        parameters_files = find_parameters_files(folder_path)
        total_items = len(parameters_files)
        for idx, parameters_file in enumerate(parameters_files):
            # Read parameters.yaml file
            parameters_data = read_parameters_file(parameters_file)
            parameters_df = pd.DataFrame(pd.json_normalize(parameters_data))  # Convert dict to DataFrame
            signature_path = os.path.join(os.path.dirname(parameters_file), "signature.md5")

            with open(signature_path, "r") as f:
                signature = f.read().strip()

            computation_folder = os.path.dirname(parameters_file)
            traction_state_image_filepath = os.path.join(computation_folder, "traction_state.png")
            parameters_df["signature"] = signature
            parameters_df["filepath"] = computation_folder
            parameters_df["traction_state_image_filepath"] = traction_state_image_filepath
            # Add parameters to dataframe
            # st.write(parameters_data)
            global_dataframe = pd.concat([parameters_df, global_dataframe], ignore_index=True)
            progress_bar.progress((idx + 1) / total_items)

    # Display dataframe
    if not st.session_state.global_dataframe.empty:
        global_dataframe = st.session_state.global_dataframe
        
    same_entry_columns = global_dataframe.columns[global_dataframe.nunique() == 1]
    st.write("Columns with the same entry across all elements:")
    st.write(same_entry_columns)
    
    # Drop same entry colomns from dataframe
    global_dataframe.drop(columns=same_entry_columns, inplace=True)
    st.write("Dropped Dataframe:", global_dataframe)
    
    st.write(global_dataframe['geometry.geom_type'].unique())
    experiment_types = global_dataframe['geometry.geom_type'].unique().tolist()
    selected = pills("Experiments", experiment_types)
    st.write(selected)
    # Filter the global database based on the selected geom_type
    filtered_dataframe = global_dataframe[global_dataframe['geometry.geom_type'] == selected]

    _nunique = filtered_dataframe.columns[filtered_dataframe.nunique() == 1]
    st.write("Filtered Data")
    st.dataframe(filter_varying_columns(filtered_dataframe))
    
    # st.write(filtered_dataframe.columns[filtered_dataframe.nunique() == 1])
    
    # Display the filtered dataframe
    # st.dataframe(filtered_dataframe)
    
    if st.session_state.global_dataframe.empty:
        st.session_state.global_dataframe = global_dataframe
    
    st.title("Parameter Files Analysis")

    if st.button("Update DataFrame"):
        if os.path.isdir(folder_path):
            st.write(folder_path)
            update_global_dataframe(folder_path)
        else:
            st.error("Invalid folder path")

    if not st.session_state.global_dataframe.empty:
        # st.dataframe(st.session_state.global_dataframe)
        display_filtered_dataframe(st.session_state.global_dataframe)
    else:
        st.write("No data available. Please update the dataframe.")
if __name__ == "__main__":
    main()
