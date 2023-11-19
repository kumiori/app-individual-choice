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

class Dichotomy extends StreamlitComponentBase<State> {
    public state = { numClicks: 0, isFocused: false, clickedValue: null }

    public render = (): ReactNode => {
        const name = this.props.args["name"]
        const greeting = this.props.args["greeting"]
        const rotationAngle = 0; // Specify the desired rotation angle in degrees

        function inverseRotatePoint(x: number, y: number, rotationAngle: number): { x: number; y: number } {
            // Convert rotation angle to radians
            const thetaRad = (rotationAngle * Math.PI) / 180;

            // Calculate the inverse rotation matrix
            const cosTheta = Math.cos(-thetaRad);
            const sinTheta = Math.sin(-thetaRad);
          
            // Apply the inverse rotation to the point
            const newX = x * cosTheta - y * sinTheta;
            const newY = x * sinTheta + y * cosTheta;
          
            return { x: newX, y: newY };
          }
          
        function distanceToRectangleBoundary(x: number, y: number, width: number, height: number): number {
            // Calculate distances to rectangle edges
            const dx = Math.max(0, Math.abs(x) - width / 2);
            const dy = Math.max(0, Math.abs(y) - height / 2);
          
            // Return the distance to the rectangle boundary
            return Math.sqrt(dx * dx + dy * dy);
          }
        
        function getRotationAngle(transformValue: string): number {
            // Extract the rotation components from the matrix
            const match = transformValue.match(/matrix\(([^,]+),([^,]+),([^,]+),([^,]+),([^,]+),([^,]+)\)/);
          
            if (!match) {
              console.error("Invalid matrix format");
              return 0;
            }
          
            // Extract the rotation angle (theta) from the components
            const a = parseFloat(match[1]);
            const b = parseFloat(match[2]);
          
            const thetaRad = Math.atan2(b, a);
            const thetaDeg = (thetaRad * 180) / Math.PI;
          
            return thetaDeg;
          }
        
        function handleElementClickTransition(event: React.MouseEvent<SVGElement>): void {
            const clickedElement = event.target as SVGElement;
            const x = event.nativeEvent.offsetX;
            const y = event.nativeEvent.offsetY;
            console.log("");
            console.log("Clicked element coordinates:", x, y);
            const computedStyle = window.getComputedStyle(clickedElement);
            console.log("clickedElement:", clickedElement);

            const rect = clickedElement.getBoundingClientRect();

            const absoluteWidth = rect.width;
            const absoluteHeight = rect.height;
        
            const xPosition = parseFloat(clickedElement.getAttribute('x') || '0'); // Default to 0 if 'x' attribute is not present
            const svgWidth = clickedElement.ownerSVGElement?.width.baseVal.value || 0;
            const absoluteX = (xPosition / 100) * svgWidth;
            const transformValue = computedStyle.transform || computedStyle.webkitTransform;
            const rotationAngle = getRotationAngle(transformValue);
            const rotatedClickPoint = inverseRotatePoint(x, y, rotationAngle);
            // const distanceToBoundary = distanceToRectangleBoundary(rotatedClickPoint.x, rotatedClickPoint.y, absoluteWidth, absoluteHeight);
            const _offset = 15;
            const _value = (rotatedClickPoint.x-_offset-absoluteX)/absoluteWidth;
            console.log("relative value:", _value);

            const elementId = clickedElement.id;
            const customDataValue = _value.toFixed(2);
      
            console.log("Clicked element ID: " + elementId);
            Streamlit.setComponentValue(customDataValue);

            // console.log("Absolute Width:", absoluteWidth);
            // console.log("Absolute Height:", absoluteHeight);
            // console.log(clickedElement)
            // console.log("SVG Width:", svgWidth);
            // console.log('Absolute X-position of the clicked rectangle:', absoluteX);
            // console.log('X-position of the clicked, relative:', xPosition, "%");
            // console.log('X-position of the clicked, absolute:', x-absoluteX);
            // console.log('X-position of the clicked, relative to width:', (x-absoluteX)/absoluteWidth);
            // console.log("Transform value:", transformValue);
            // console.log("Angle value:", rotationAngle);
            // console.log("rotatedClickPoint:", rotatedClickPoint);
            // console.log("projectedClickPoint:", rotatedClickPoint.x-absoluteX);
            // console.log("relative projectedClickPoint:", (rotatedClickPoint.x-_offset-absoluteX)/absoluteWidth);
            // console.log("Distance to boundary:", distanceToBoundary);

        }

        function handleElementClickBoundary(event: React.MouseEvent<SVGElement>): void {
            const clickedElement = event.target as SVGElement;
            const x = event.nativeEvent.offsetX;
            const y = event.nativeEvent.offsetY;
            console.log("Clicked limit element:", x, y);
            const elementId = clickedElement.id;
            const customDataValue = clickedElement.getAttribute('data-value');
      
            console.log("Clicked element ID: " + elementId);
            Streamlit.setComponentValue(customDataValue);
            console.log("Clicked element value: " + customDataValue)
        }
        
        return (
            <div id="happy">
                <span>
                    {greeting}, {name}! &nbsp;
                    <br />
                    <p>Boundaries matter, see below...</p>
                </span>
                <svg className="col-md-12 col-sm-12" height="200" >
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" style={{ stopColor: '#000' }} />
                            <stop offset="100%" style={{ stopColor: '#eee' }} />
                        </linearGradient>
                    </defs>
                    
                    <rect
                        width="40%"
                        height="200%"
                        fill="#000" // Solid color for the first rectangle
                        transform={`rotate(${rotationAngle} 0 0)`} // Rotate the first rectangle
                        y="-200"  // Adjusted y position for the third rectangle
                        onClick={(e) => handleElementClickBoundary(e)}
                        data-value='0'
                    />
                    <rect
                        width="20%"
                        height="300%"
                        x="39.9%" // Shift the second rectangle by 30% of the width
                        fill="url(#gradient)" // Gradient background for the third rectangle
                        transform={`rotate(${rotationAngle} 0 0)`} // Rotate the second rectangle
                        y="-300"  // Adjusted y position for the third rectangle
                        onClick={(e) => handleElementClickTransition(e)}
                    />
                    <rect
                        width="40%"
                        height="300%"
                        x="59.8%" // Shift the third rectangle by 60% of the width
                        fill="#eee" // Solid color for the second rectangle
                        transform={`rotate(${rotationAngle} 0 0)`} // Rotate the third rectangle
                        y="-400"  // Adjusted y position for the third rectangle
                        onClick={(e) => handleElementClickBoundary(e)}
                        data-value='1'
                    />
                </svg>
            </div>
        );
    }


}

export default withStreamlitConnection(Dichotomy)
// export default Dichotomy
