import React from "react"
import ReactDOM from "react-dom"
import QualitativeSelector from "./QualitativeSelector"
import QualitativeParametricSelector from "./ParametricQualitativeSelector"
import Dichotomy from "./Dichotomy"
import { ComponentProps, withStreamlitConnection } from "streamlit-component-lib";

const QualiQuantiComponent = (props: ComponentProps) => {
  //get data
  const component = props.args['component']
  const kw = props.args['kw']

  //return component base on component id
  switch (component) {
    case 'dichotomy':
      return <Dichotomy {...props} />;
    case 'qualitative':
      return <QualitativeSelector {...props} />;
      case 'parametric':
      return <QualitativeParametricSelector {...props} />;
    default:
      return <h1>default</h1>
  }
};

const StreamlitQualiQuantiComponent = withStreamlitConnection(QualiQuantiComponent)

ReactDOM.render(
  <React.StrictMode>
    <StreamlitQualiQuantiComponent />
  </React.StrictMode>,
  document.getElementById("root")
)

