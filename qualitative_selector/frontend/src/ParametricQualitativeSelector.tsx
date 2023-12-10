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

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class QualitativeParametricSelector extends StreamlitComponentBase<State> {
  public state = { numClicks: 0, isFocused: false, clickedValue: null }

  public render = (): ReactNode => {
    const name = this.props.args["name"]
    const question = this.props.args["question"]
    const areas = this.props.args["areas"]
    const dataValues: number[] = this.props.args['data_values'];
    const lastIndex = dataValues.length-1;

    // const { theme } = this.props
    // const style: React.CSSProperties = {}

    function handleElementLeave(event: React.MouseEvent<SVGElement>): void {
      const hoveredElement = event.target as SVGElement;
      hoveredElement.style.filter = "none";
    }
    function handleElementHover(event: React.MouseEvent<SVGElement>): void {
      const hoveredElement = event.target as SVGElement;
      const customDataValue = hoveredElement.getAttribute('data-value');
      const blurRadius = customDataValue ? 40 / Number(customDataValue) : 0; // You can adjust this formula as needed
      hoveredElement.style.filter = `blur(${blurRadius}px)`;
    }
    function handleElementEvent(event: React.MouseEvent<SVGElement>): void {
      const clickedElement = event.target as SVGElement;
      const elementId = clickedElement.id;
      const customDataValue = clickedElement.getAttribute('data-value');

      // console.log("Clicked element ID: " + elementId);
      Streamlit.setComponentValue(customDataValue);
    }

    const renderActiveAreas = (numberOfActiveAreas: number, dataValues: number[]) => {
      const activeAreas = [];

      for (let i = 0; i < numberOfActiveAreas; i++) {
        // Customize the appearance and position of each area here
        const areaProps: React.SVGProps<SVGEllipseElement> & { 'data-value': number } = {
          className: 'interface',
          'data-value': i,
          onClick: handleElementEvent,
        };

        if (i === 0) {
          areaProps.width = '100%';
          areaProps.height = '100%';
          areaProps.fill = '#383838';
          areaProps.cx = 300;
          areaProps.cy = 100;
          areaProps.rx = 450; // Customize ellipse properties
          areaProps.ry = 250;
          areaProps.fill = '#444444'; // Alternate colors
        } else {
          areaProps.cx = 300;
          areaProps.cy = 100;
          areaProps.rx = 250 - 2*i * 60; // Customize ellipse properties
          areaProps.ry = 150 - 2*i * 20;
          areaProps.fill = i % 2 === 0 ? '#000000' : '#878787'; // Alternate colors
          areaProps.onMouseEnter = handleElementHover;
          areaProps.onMouseLeave = handleElementLeave;
        }

        activeAreas.push(
          <ellipse key={i} {...areaProps} />
        );
        // console.log(activeAreas)
      }

      return activeAreas;
    };

    function displayEllipses(areas: number, dataValues: number[]) {
      const radius = 20; // Adjust as needed
      const spacing = 30; // Adjust as needed
      const centerX = 100; // Adjust as needed
      const centerY = 100; // Adjust as needed
    
      const ellipses = dataValues.map((value, index) => {
        const areaProps: React.SVGProps<SVGEllipseElement> & { 'data-value': number } = {
          className: 'interface',
          'data-value': value,
          onClick: handleElementEvent,
        };

        if (index === 0) {
          areaProps.width = '100%';
          areaProps.height = '100%';
          areaProps.fill = '#383838';
          areaProps.cx = 300;
          areaProps.cy = 100;
          areaProps.rx = 450; // Customize ellipse properties
          areaProps.ry = 250;
          areaProps.fill = '#444444'; // Alternate colors
        } else {
          areaProps.cx = 300;
          areaProps.cy = 100;
          areaProps.rx = 250 - 2*index * 60; // Customize ellipse properties
          areaProps.ry = 150 - 2*index * 20;
          areaProps.fill = index % 2 === 0 ? '#000000' : '#878787'; // Alternate colors
          areaProps.onMouseEnter = handleElementHover;
          areaProps.onMouseLeave = handleElementLeave;
        }

        return (
          <ellipse key={index} {...areaProps} />
        );
      }
      );
    
      return (
        <svg className="col-md-12 col-sm-12" height="200" xmlns="http://www.w3.org/2000/svg">
          {ellipses}
        </svg>
      );
    }

    return (
      <div id="happy">
        <span>
          For you to decide, {name}!
          <p>Beware: boundaries always fade...</p>
          <p>Make a move, pick your choice among: {dataValues.map((value, index) => index === lastIndex ? value : `${value}, `)}</p>
        </span>
        <svg className="col-md-12 col-sm-12" height="200">
          {/* {renderActiveAreas(areas, dataValues)} */}
          {displayEllipses(areas, dataValues)}
        </svg>
        <hr />
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

  // handleElementClick = () => {
  handleElementClick = (elementId: string) => {
    // If you need to access the clicked element, you can use the elementId
    const clickedElement = document.getElementById(elementId);
    // You can perform additional actions with the clicked element if needed
    // console.log(clickedElement);
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

export default QualitativeParametricSelector
