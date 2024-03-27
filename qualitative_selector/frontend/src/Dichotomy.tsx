import {
    Streamlit,
    StreamlitComponentBase,
    withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { useRef, useState, useEffect } from 'react';
interface State {
    numClicks: number;
    isFocused: boolean;
    clickedValue: null;
  }

class Dichotomy extends StreamlitComponentBase<State> {
    public state: State = { numClicks: 0, isFocused: false, clickedValue: null };

    private svgRef = React.createRef<SVGSVGElement>();
    // const [svgWidth: any, setSvgWidth: any] = useState<number>(0);

    public render = (): ReactNode => {
        const name = this.props.args["name"]
        const question = this.props.args["question"]
        const label = this.props.args["label"]
        const width = this.props.args["width"]; // or any other value
        const height = this.props.args["height"]
        const rotationAngle = this.props.args["rotationAngle"]; // Specify the desired rotation angle in degrees
        const gradientWidth = this.props.args["gradientWidth"]; // Specify the desired rotation angle in degrees
        // const shift = this.props.args["shift"]; // Specify the desired rotation angle in degrees
        const invertColors = this.props.args["invert"] ?? false;
        const shift = this.props.args["shift"] ?? false;
        // const shift = 40;
        const color1 = invertColors ? '#fff' : '#000';
        const color2 = invertColors ? '#000' : '#fff';
        let svgWidth = 10;

        if (this.svgRef.current) {
            const rect = this.svgRef.current.getBoundingClientRect();
            svgWidth = rect.width;
        }
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
            const computedStyle = window.getComputedStyle(clickedElement);

            const rect = clickedElement.getBoundingClientRect();

            const absoluteWidth = rect.width;
            const absoluteHeight = rect.height;
            const xPosition = parseFloat(clickedElement.getAttribute('x') || '0'); // Default to 0 if 'x' attribute is not present
            const svgWidth = clickedElement.ownerSVGElement?.width.baseVal.value || 0;
            // const rotationAngle = getRotationAngle(transformValue);
            // const rotatedClickPoint = inverseRotatePoint(x, y, rotationAngle);
            // const distanceToBoundary = distanceToRectangleBoundary(rotatedClickPoint.x, rotatedClickPoint.y, absoluteWidth, absoluteHeight);
            const _offset = 0;
            // const _value = (rotatedClickPoint.x-_offset-absoluteX)/absoluteWidth;
            const _value = (x-rect.x)/absoluteWidth;

            const elementId = clickedElement.id;
            const customDataValue = _value.toFixed(2);

            Streamlit.setComponentValue(customDataValue);

        }

        function handleElementClickBoundary(event: React.MouseEvent<SVGElement>): void {
            const clickedElement = event.target as SVGElement;
            const x = event.nativeEvent.offsetX;
            const y = event.nativeEvent.offsetY;
            const elementId = clickedElement.id;
            const customDataValue = clickedElement.getAttribute('data-value');
      
            Streamlit.setComponentValue(customDataValue);
            // console.log("Clicked limit element:", x, y);
            // console.log("Clicked element ID: " + elementId);
            // console.log("Clicked element value: " + customDataValue)
        }
        
        return (
            <div id="happy">
                <p>Hello, {name}. {question}</p>
                <svg className="col-md-12 col-sm-12" width="100%"  height={height}  style={{ paddingLeft: 15 }}>
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" style={{ stopColor: color1 }} />
                            <stop offset="100%" style={{ stopColor: color2 }} />
                        </linearGradient>
                    </defs>
                    
                    <rect
                        // rx="15" ry="15" 
                        width="100%"
                        height="100%"
                        fill={color1}
                        transform={`rotate(${rotationAngle} 0 0)`} // Rotate the first rectangle
                        // y="-300"  // Adjusted y position for the third rectangle
                        onClick={(e) => handleElementClickBoundary(e)}
                        data-value='0'
                    />
                    <rect
                        width={gradientWidth ? `${gradientWidth}%` : '0'}
                        height="100%"
                        x={gradientWidth ? `calc(50% - ${gradientWidth / 2}%)` : '0'}
                        fill="url(#gradient)" // Gradient background for the third rectangle
                        transform={`rotate(${rotationAngle} 0 0)`} // Rotate the second rectangle
                        onClick={(e) => handleElementClickTransition(e)}
                    />
                    <rect
                        rx="00" ry="0" 
                        width="100%"
                        height="100%"
                        x={gradientWidth ? `calc(50% + ${gradientWidth / 2 - .1}%)` : '0'}
                        fill={color2}
                        transform={`rotate(${rotationAngle} 0 0)`} // Rotate the third rectangle
                        onClick={(e) => handleElementClickBoundary(e)}
                        data-value='1'
                    />
                </svg>
            </div>
        );
    }


}

// export default withStreamlitConnection(Dichotomy)
export default Dichotomy
