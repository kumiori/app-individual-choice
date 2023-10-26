import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"

interface State {
  numClicks: number
  isFocused: boolean
}

class MyComponent extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false, clickedValue: null }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const name = this.props.args["name"]
    const greeting = this.props.args["greeting"]

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    // Maintain compatibility with older versions of Streamlit that don't send
    // a theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${
        this.state.isFocused ? theme.primaryColor : "gray"
      }`
      style.border = borderStyling
      style.outline = borderStyling
    }
    function handleElementLeave(event: React.MouseEvent<SVGElement>): void {
      const hoveredElement = event.target as SVGElement;
      // Reset the shadow
      hoveredElement.style.filter = "none";
    }
    function handleElementHover(event: React.MouseEvent<SVGElement>): void {
      const hoveredElement = event.target as SVGElement;
      // Example: Add a subtle shadow to the element on hover
      const customDataValue = hoveredElement.getAttribute('data-value');
      const blurRadius = customDataValue ? 200 / Number(customDataValue) : 0; // You can adjust this formula as needed

      hoveredElement.style.filter = `blur(${blurRadius}px)`;
    }
    function handleElementEvent(event: React.MouseEvent<SVGElement>): void {
      const clickedElement = event.target as SVGElement;
      const elementId = clickedElement.id;
      const customDataValue = clickedElement.getAttribute('data-value');

      console.log("Clicked element ID: " + elementId);
      Streamlit.setComponentValue(customDataValue);
    }

    return (
      <div id="happy">
      <span>
        {greeting}, {name}! &nbsp;
        <button
          style={style}
          onClick={this.onClicked}
          disabled={this.props.disabled}
          onFocus={this._onFocus}
          onBlur={this._onBlur}
        >
          Don't click Me!
        </button>
        <br />
        <p>Pick a number below</p>
      </span>
      <svg className="col-md-12 col-sm-12" height="200">
      <rect
        className="interface"
        id="button5"
        data-value='5'
        width="100%"
        height="100%"
        fill="#383838"
        onClick={handleElementEvent}
      ></rect>
      <ellipse
        className="interface"
        id="button10"
        data-value='10'
        cx="300"
        cy="100"
        rx="250"
        ry="150"
        fill="#c9c9c9"
        onClick={handleElementEvent}
        onMouseEnter={handleElementHover}
        onMouseLeave={handleElementLeave}
      ></ellipse>
      <ellipse
        className="interface"
        id="button15"
        data-value='15'
        cx="300"
        cy="100"
        rx="160"
        fill="#878787"
        onClick={handleElementEvent}
        onMouseEnter={handleElementHover}
        onMouseLeave={handleElementLeave}
      ></ellipse>
      <circle
        className="interface"
        id="button25"
        data-value='25'
        cx="280"
        cy="100"
        r="40"
        fill="black"
        onClick={handleElementEvent}
      ></circle>
      <circle className="interface" id="target" cx="-330" cy="-100" r="4" fill="red"></circle>
      <text x="5" y="15" fill="darkGrey">
        5
      </text>
      <text x="272" y="90" fill="white">
        25
      </text>
      <text x="180" y="65" fill="lightGrey">
        15
      </text>
      <text x="90" y="43" fill="#606060">
        10
      </text>
    </svg>
    </div>
    )
  }

  
  handleClick = (event: React.MouseEvent<SVGElement>) => {
    const clickedElement = event.target as SVGElement;
    const elementId = clickedElement.id;
  
    // Check if the clicked element has a 'data-value' attribute before retrieving it
    const customDataValue = clickedElement.getAttribute('data-value');
  
    console.log("Clicked element ID: " + elementId);
    Streamlit.setComponentValue(customDataValue);
  };

  // handleElementClick = () => {
    handleElementClick = (elementId: string) => {
    // Handle the click event for the clicked element
    // console.log(`Clicked element with ID: ${elementId}`);
    // You can perform any additional actions here based on the elementId
  
    // If you need to access the clicked element, you can use the elementId
    const clickedElement = document.getElementById(elementId);
    // You can perform additional actions with the clicked element if needed
    console.log(clickedElement);
    // If you want to update the state based on the clicked element, you can do so here
    // For example, you can increment a counter or change the appearance of the element
  
    // If you need to communicate with Streamlit and pass data back to Python, you can do so as well
    Streamlit.setComponentValue(elementId);
  };

  /** Click handler for our "Click Me!" button. */
  private onClicked = (): void => {
    // Increment state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      state => ({ numClicks: state.numClicks + 1 }),
      () => Streamlit.setComponentValue(this.state.numClicks)
    )
  }

  /** Focus handler for our "Click Me!" button. */
  private _onFocus = (): void => {
    this.setState({ isFocused: true })
  }

  /** Blur handler for our "Click Me!" button. */
  private _onBlur = (): void => {
    this.setState({ isFocused: false })
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(MyComponent)
