import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  const httpHandler = async () => {
    const url = "http://localhost:8000/fastapi/download";
    let so = "WINDOWS";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/xml",
        },
        body: `<?xml version="1.0" encoding="UTF-8"?>
<api-rest-model xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="schema.xsd">
  <psm-model>
    <so so-name="${so}"/>
    <technology tech-name="FASTAPI" version="0.0.0" port="4321"/>
    <project name="TIENDA"/>
  </psm-model>

  <csm-model>
    <login has="true">
      <table name="CLIENTE"/>
      <unique-field attribute="ID_CLIENTE"/>
      <encrypt-field attribute="name"/>
    </login>
    <package name="USER">
      <table name="CLIENTE"/>
    </package>
    <package name="BUY">
      <table name="FACTURA"/>
    </package>
  </csm-model>

  <relational-model>
    <table name="CLIENTE">
      <attributes>
        <attribute data-type="INT" name="ID_CLIENTE" PK="true"/>
        <attribute data-type="VARCHAR" name="name" />
      </attributes>

      <relations>
        <relation multiplicity="1:n" table="FACTURA" attribute="ID_FACTURA"/>
      </relations>
    </table>

    <table name="FACTURA">
      <attributes>
        <attribute data-type="INT" name="ID_FACTURA"  PK="true"/>
        <attribute data-type="VARCHAR" name="FECHA" />
      </attributes>

      <relations>
        <relation multiplicity="1:n" table="CLIENTE" attribute="ID_CLIENTE"/>
      </relations>
    </table>
  </relational-model>
</api-rest-model>`,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const blob = await response.blob();
      const urlObject = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = urlObject;
      link.download = "mi_script." + (so == "WINDOWS" ? "bat" : "sh");
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(urlObject);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => httpHandler()}>file</button>
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
