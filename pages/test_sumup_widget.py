import streamlit as st

def main():
    st.title("SumUp Card Widget")

    # Embed the HTML code and JavaScript script for the SumUp Card widget
    sumup_card_html = """
    <div id="sumup-card"></div>
    <script
      type="text/javascript"
      src="https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js"
    ></script>
    <script type="text/javascript">
      SumUpCard.mount({
        id: 'sumup-card',
        checkoutId: '2ceffb63-cbbe-4227-87cf-0409dd191a98',
        onResponse: function (type, body) {
          console.log('Type', type);
          console.log('Body', body);
        },
      });
    </script>
    """

    # Display the SumUp Card widget
    st.components.v1.html(sumup_card_html, height=600)

if __name__ == "__main__":
    main()
