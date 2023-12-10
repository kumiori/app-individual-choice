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

class QualitativeSelector extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false, clickedValue: null }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const name = this.props.args["name"]
    const question = this.props.args["question"]
    const dataValues: number[] = this.props.args['data_values'];
    const lastIndex = dataValues.length-1;
    const cx = 300;
    const cy = 100;
    
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
      const borderStyling = `1px solid ${this.state.isFocused ? theme.primaryColor : "gray"
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

      Streamlit.setComponentValue(customDataValue);
    }
    return (
      <div id="happy">
        <span>
          Hello, {name},
          <br />

          <p>{question} Let's find {lastIndex+1} tiers</p>
          <p>Data Values: {dataValues.map((value, index) => index === lastIndex ? value : `${value}, `)}</p>

        </span>
        <svg className="col-md-12 col-sm-12" height="200">
          {dataValues.map((value, index) => (
            <React.Fragment key={index}>
              {index === 0 && (
                <rect
                  className="interface"
                  id={`button${value}`}
                  data-value={value}
                  width="100%"
                  height="100%"
                  fill="#383838"
                  onClick={handleElementEvent}
                ></rect>
              )}
              {index > 0 && index < lastIndex && (
                <ellipse
                  className="interface"
                  id={`button${value}`}
                  data-value={value}
                  cx={cx}
                  cy={cy}
                  rx={250 - index * 60}
                  ry={150 - index * 20}
                  fill={index % 2 === 0 ? '#c9c9c9' : '#878787'}
                  onClick={handleElementEvent}
                  onMouseEnter={handleElementHover}
                  onMouseLeave={handleElementLeave}
                ></ellipse>
              )}
              {index === lastIndex && (
                <circle
                  className="interface"
                  id={`button${value}`}
                  data-value={value}
                  cx="290"
                  cy="100"
                  r={30}
                  // fill={index % 2 === 0 ? '#c9c9c9' : '#878787'}
                  fill="black"
                  onClick={handleElementEvent}
                ></circle>
              )}
              {/* <text x={index * 90 + 5} y={index * 11 + 15} fill="darkGrey"> */}
                {/* {value}, {index} */}
              {/* </text> */}
            </React.Fragment>
          ))}

          <circle className="interface" id="target" cx="300" cy="110" r="4" fill="red"></circle>
          {dataValues.map((value, index) => (
            <React.Fragment key={index}>
              <text
                key={`text${index}`}
                x={cx - 0.9*(250 - index * 60)} // Adjusted x position for text
                y={.55*index/lastIndex * cy + 50} // Fixed y position for text
                // fill="red"
                // fill={index % 2 === 0 ? '#c9c9c9' : 'black'}
                fill={index === lastIndex ? 'red' : (index % 2 === 0 ? '#878787' : '#c9c9c9')}
              >
                {value}
              </text>
            </React.Fragment>
          ))}
          <hr />
        </svg>
      </div>
    )
  }


  handleClick = (event: React.MouseEvent<SVGElement>) => {
    const clickedElement = event.target as SVGElement;
    const elementId = clickedElement.id;

    // Check if the clicked element has a 'data-value' attribute before retrieving it
    const customDataValue = clickedElement.getAttribute('data-value');

    // console.log("Clicked element ID: " + elementId);
    Streamlit.setComponentValue(customDataValue);
  };

  handleElementClick = (elementId: string) => {
    // Handle the click event for the clicked element
    // console.log(`Clicked element with ID: ${elementId}`);
    // You can perform any additional actions here based on the elementId

    // If you need to access the clicked element, you can use the elementId
    const clickedElement = document.getElementById(elementId);
    // You can perform additional actions with the clicked element if needed
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
// export default withStreamlitConnection(QualitativeSelector)
export default QualitativeSelector
