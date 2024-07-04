import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  const httpHandler = async () => {
    const url = "http://localhost:8000/fastapi/download";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "api-rest-model": {
            "psm-model": {
              so: {
                "so-name": "LINUX",
              },
              technology: {
                "tech-name": "NEST.JS",
                version: "0.0.0",
              },
              project: {
                name: "TIENDA",
              },
            },
            "csm-model": {
              package: [
                {
                  name: "USER",
                  table: {
                    name: "CLIENTE",
                  },
                },
                {
                  name: "BUY",
                  table: {
                    name: "FACTURA",
                  },
                },
              ],
            },
            "relational-model": {
              table: [
                {
                  name: "CLIENTE",
                  attributes: {
                    attribute: [
                      {
                        "data-type": "INT",
                        name: "ID_CLIENTE",
                        PK: "true",
                      },
                      {
                        "data-type": "VARCHAR",
                        name: "name",
                      },
                    ],
                  },
                  relations: {
                    relation: {
                      multiplicity: "1:n",
                      table: "FACTURA",
                    },
                  },
                },
                {
                  name: "FACTURA",
                  attributes: {
                    attribute: [
                      {
                        "data-type": "INT",
                        name: "ID_FACTURA",
                        PK: "true",
                      },
                      {
                        "data-type": "VARCHAR",
                        name: "FECHA",
                      },
                    ],
                  },
                  relations: {
                    relation: {
                      multiplicity: "1:n",
                      table: "CLIENTE",
                    },
                  },
                },
              ],
            },
          },
        }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const blob = await response.blob();
      const urlObject = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = urlObject;
      link.download = "mi_script.sh"; // Nombre del archivo para descargar
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