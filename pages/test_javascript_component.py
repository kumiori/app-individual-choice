import streamlit as st
from streamlit_javascript import st_javascript

st.subheader("Javascript API call")

return_value = st_javascript("""await fetch("https://reqres.in/api/products/3").then(function(response) {
    return response.json();
}) """)

st.markdown(f"Return value was: {return_value}")
print(f"Return value was: {return_value}")


# Create a placeholder for the JavaScript output
st.markdown("<div id='content'></div>", unsafe_allow_html=True)

# JavaScript to add a div and write text inside it
js_code = """
(function() {
    // Create a new div element
    const newDiv = document.createElement('div');
    newDiv.id = 'dummy-div';
    newDiv.innerHTML = 'Hello, this is a dynamically added div!';
    console.log('New div created:', newDiv);
    // Append the new div to the content div
    document.getElementById('content').appendChild(newDiv);
})();
"""

# Execute the JavaScript
return_value = st_javascript(js_code)

# Output the result of the JavaScript execution
st.write(f"Return value was: {return_value}")


js_code = """
(function() {
    // Ensure the DOM is fully loaded before executing the script
    document.addEventListener("DOMContentLoaded", function(event) {
        console.log('DOM fully loaded and parsed');
        
        // Create a new div element
        const newDiv = document.createElement('div');
        newDiv.id = 'dummy-div';
        newDiv.innerHTML = 'Hello, this is a dynamically added div!';
        console.log('New div created:', newDiv);
        
        // Append the new div to the content div
        document.getElementById('content').appendChild(newDiv);
        console.log('New div appended to content');
    });
})();
"""


# Execute the JavaScript
return_value = st_javascript(js_code)

# Output the result of the JavaScript execution
st.write(f"Return value was: {return_value}")


html_code = """
<div id="content"></div>
<script src="https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js"></script>
<script>
    document.addEventListener("DOMContentLoaded", function(event) {
        const newDiv = document.createElement('div');
        newDiv.id = 'dummy-div';
        newDiv.innerHTML = 'Hello, this is a dynamically added div!';
        document.getElementById('content').appendChild(newDiv);
    });
</script>
"""

# Display the HTML code in Streamlit app
st.components.v1.html(html_code, height=100)

# JavaScript to load the SDK and log the result
js_code = """
(async function() {
    // Load SumUp SDK
    const script = document.createElement('script');
    script.src = "https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js";
    script.onload = () => {
        // Log a message when the SDK is loaded
        console.log('SumUp SDK loaded successfully.');
    };
    script.onerror = () => {
        console.error('Failed to load the SumUp SDK.');
    };
    document.head.appendChild(script);
})();
"""

# Execute the JavaScript
return_value = st_javascript(js_code)

# Output the result of the JavaScript execution
st.write(f"Return value was: {return_value}")


# Placeholder for the SumUp card div
st.markdown("<div id='sumup-card'></div>", unsafe_allow_html=True)

# Checkout ID - replace with your actual checkout ID
checkout_id = "YOUR_CHECKOUT_ID"

# JavaScript to load the SDK and mount the SumUp card
js_code = f"""
(async function() {{
    // Load SumUp SDK
    console.log('Loading SumUp SDK');
    const script = document.createElement('script');
    script.src = "https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js";
    script.onload = () => {{
        console.log('SumUp SDK loading');
        // Initialize SumUp card after SDK is loaded
        SumUpCard.mount({{
            id: 'sumup-card',
            checkoutId: '{checkout_id}',
            donateSubmitButton: false,
            showInstallments: true,
            onResponse: function (type, body) {{
                console.log('Type', type);
                console.log('Body', body);
                SumUpCard.unmount();
            }},
        }});
    }};
    document.head.appendChild(script);
}})();
"""

# Execute the JavaScript
return_value = st_javascript(js_code)

# Output the result of the JavaScript execution
st.write(f"Return value was: {return_value}")