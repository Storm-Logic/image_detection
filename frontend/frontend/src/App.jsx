import { useState } from "react";
import axios from "axios";
import { Row, Col } from "antd"


export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [result_img, setImage] = useState(null);

  const choose_image = (e) => {
    setFile(e.target.files[0])
    const url = URL.createObjectURL(e.target.files[0]);
    setPreview(url);
  }

  const detectObject = async () => {
    if (!file || !prompt) return alert("Please select image and enter prompt");

    const formData = new FormData();
    formData.append("image", file);
    formData.append("prompt", prompt);

    const res = await axios.post("http://127.0.0.1:8000/detect", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    setResult(res.data);
    setImage(res.data.result_img)
  };

  return (
    <div style={{ padding: 30 }}>

      <h2>Image Object Detector</h2>

      <input
        type="file"
        accept="image/*"
        onChange={choose_image}
      />
      <br /><br />
      <Row><Col>
        <section style={{ height: "300px" }}>
          <img
            src={preview}
            alt="preview"
            style={{ height: "300px", }}
          /></ section>

      </Col>
        <Col md={2}></Col>
        <Col>


          {result && (
            <section style={{ height: "300px" }}>
              <div>
                {/* <h3>Result</h3>
            <p>Prompt: {result.prompt}</p>
            <p>Detected: {result.detected ? "Yes" : "No"}</p> */}

                {/* {result.results.map((item, index) => (
                <div key={index}>
                  <p>Object: {item.object}</p>
                  <p>Confidence: {item.confidence}</p>
                  <p>Box: {item.box.join(", ")}</p>
                </div>
              ))} */}

                {result_img && (
                  <img
                    style={{ height: "300px" }}
                    src={`data:image/png;base64,${result_img}`}
                    alt="Generated from prompt"
                    className="generated-image"
                  />
                )}
              </div></section>
          )}</Col>
      </Row>

      <Row style={{ marginTop: "10px" }}>
        <input
          type="text"
          placeholder="cat, person, dog..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />

        <button onClick={detectObject}>Detect</button></Row>
    </div>
  );
}
