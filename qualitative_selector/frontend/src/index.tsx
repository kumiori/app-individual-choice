import React from "react"
import ReactDOM from "react-dom"
import QualitativeSelector from "./QualitativeSelector"
import QualitativeParametricSelector from "./ParametricQualitativeSelector"
import Dichotomy from "./Dichotomy"

ReactDOM.render(
  <React.StrictMode>
    {/* <QualitativeSelector /> */}
    {/* <QualitativeParametricSelector /> */}
    <Dichotomy />
  </React.StrictMode>,
  document.getElementById("root")
)

