import React, { Component } from "react";
import "../style.css"

export default class Report extends Component {
  render() {
    const current = new Date();
    const date = `${current.getDate()}/${current.getMonth()+1}/${current.getFullYear()}`;

    return (
      <div id="box">
        <div id="fecha">
          <p><b>{date}</b></p>
        </div>
        <h2>Reporte Generado</h2>
        <div id="detalles">
          <h4>Detalles del Bache</h4>
          <p>{this.props.details}</p>
        </div>
        <div>
          <h4 id="foto">Evidencia Detectada</h4>
          <img className="uploadedImage2" src={this.props.imageSrc} alt="processedImage"/>
        </div>
        <div id="firma">
          <p>Firma</p>
        </div>
        <div>
          <button onClick={this.props.closeCallback}>Cerrar</button>
        </div>
      </div>
    )
  }
}