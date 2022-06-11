import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useState } from 'react';
import UploadComponent from "./components/UploadComponent";
import Report from "./components/Report"

function App() {
  const [details, setDetails] = useState("")
  const [imageSrc, setImageSrc] = useState("")
  const [reportVisible, setReportVisible] = useState(false)

  const handleFileUpload = (imageData, detailsData) => {
    setDetails(detailsData)
    setImageSrc(imageData)
    setReportVisible(true)
  }

  const handleCloseReport = () => {
    setReportVisible(false)
  }

  return (
    <div className="App">
      <h1>Reporte de Baches</h1>
      <UploadComponent uploadCallback={handleFileUpload}></UploadComponent>
      {reportVisible && <Report details={details} imageSrc={imageSrc} closeCallback={handleCloseReport}></Report>}
    </div>
  );
}

export default App;
