import React, { Component } from "react";

export default class UploadComponent extends Component {
  state = {
      selectedFile: null,
      imgSrc: null,
      textAreaValue: ""
  }

  onFileChange = (e) => {
    var file = e.target.files[0]
    if(!file)
      return
    
    var url = URL.createObjectURL(file)
    this.setState({ imgSrc: url, selectedFile: file })
  }

  onFileUpload = async (event) => {
    if(!this.state.selectedFile) {
      alert("Choose an image before uploading")
      return
    }

    const formData = new FormData()
    formData.append('image', this.state.selectedFile)
    
    const data = await fetch("/processImage", {
      method: "post",
      body: formData,
    })
    const jsonResponse = await data.json();
    if(jsonResponse) {
      const bytestring = jsonResponse['image']
      const img = bytestring.split('\'')[1]
      const imgSrcString = 'data:image/jpeg;base64,' + img
      this.props.uploadCallback(imgSrcString, this.state.textAreaValue)
    } else {
      console.log("Error found")
    }
  }

  onTextAreaChange = (event) => {
    this.setState({ textAreaValue: event.target.value })
  }

  renderImage = () => {
    if(this.state.imgSrc) {
      return (
        <div>
          <h2 id="imgTitle">Imagen:</h2>
          <img className="uploadedImage1" src={this.state.imgSrc} alt="uploadedImage"/>
        </div>
      )
    } else {
      return (
        <div>
          <p id="alert">Selecciona un archivo antes de generar el reporte.</p>
        </div>
      )
    }
  }

  render() {
    return (
      <div id="form">
        <div>
          <p className="instructions">Ingresa los detalles del bache (ubicación, tamaño, etc): </p>
          <textarea id="textarea"
            value={this.state.textAreaValue}
            onChange={this.onTextAreaChange}
          />
        </div>
        <div>
          <p className="instructions">Selecciona una imagen para analizar en el reporte:</p>
          <input type="file" onChange={this.onFileChange} /><br />
        </div>
        {this.renderImage()}
        <button onClick={this.onFileUpload}>Generar Reporte</button>
      </div>
    )
  }
}