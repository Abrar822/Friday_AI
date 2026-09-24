import "../stylesheets/memory.css";
import { open } from "@tauri-apps/plugin-dialog";
import { useEffect, useState, useRef } from "react";
import {
  SearchLocations,
  deleteLocations,
  FetchLocations,
  upsertLocations,
} from "../helper/MemoryConnect";

export default function Memory({ setAlert, pickedFolder, setPickFolder }) {
  const searchRef = useRef(null);
  const tableRef = useRef(null);
  const tbodyRef = useRef(null);

  const [locations, setLocations] = useState({
    details: [],
    error: "",
  });
  const [searchedQuery, setSearchedQuery] = useState("");

  const [toDelete, setToDelete] = useState([]);
  const [selectAll, setSelectAll] = useState(false);

  // Runs only initially to fetch location
  useEffect(() => {
    const fetchData = async () => {
      let data = await FetchLocations();
      setLocations({ details: data, error: "" });
    };
    try {
     fetchData();
    } catch (err) {
      setAlert(err.message);
    }
  }, []);

  // To indirectly run the fetch location when user erases the input
  useEffect(() => {
    const runFetchLocationIndirect = async () => {
      if (searchedQuery.trim().length == 0) {
        try {
          await searchRef.current.click();
        } catch (err) {
          setAlert({ msg: err.message, state: true });
        }
      }
    };
    runFetchLocationIndirect();
  }, [searchedQuery]);

  useEffect(() => {
    console.log(pickedFolder);
  }, [pickedFolder]);

  const deletePaths = async () => {
    let foldernameDict = toDelete.map((ele) => ({ f_name: ele }));
    try {
      await deleteLocations(foldernameDict).then((data) => {
        setAlert({ msg: data.message, state: true });
      });
      await FetchLocations().then((data) => {
        setLocations({ details: data, error: "" });
      });
      setToDelete([]);
      tableRef.current
        .querySelectorAll('input[type="checkbox"')
        .forEach((ele) => (ele.checked = false));
    } catch (err) {
      setAlert({ msg: err.message, state: true });
    }
  };

  const openFolderPicker = async () => {
    let selectedPath;
    try {
      selectedPath = await open({
        directory: true,
        multiple: false,
      });
      if (selectedPath && !pickedFolder.find((ele) => ele === selectedPath))
        setPickFolder((prev) => [...prev, selectedPath]);
    } catch (err) {
      setAlert({ msg: err.message, state: true });
    }
  };

  const insertPaths = async () => {
    try {
      if(pickedFolder.length == 0) {
        console.log(pickedFolder)
        setAlert({msg: 'No Paths Selected. Select a path to insert it.', state: true})
        return;
      }
      let response = await upsertLocations(pickedFolder);
      if (response.message) {
        setAlert({ msg: response.message, state: true });
        console.log(locations)
        setPickFolder([])
        await FetchLocations().then(data => {
          setLocations({details: data, error: ''})
        })
      }
    } catch (err) {
      setAlert({ msg: err.message, state: true });
    }
  };

  return (
    <>
      <div className="memory-content">
        <div className="section-1">
          <div className="search-container">
            <div className="title">Locations</div>
            <input
              type="text"
              className="searchbar"
              placeholder="Search Foldername..."
              onChange={(e) => {
                setSearchedQuery(e.target.value);
              }}
              value={searchedQuery}
            />
            <button
              ref={searchRef}
              className="search-btn"
              onClick={async () => {
                try {
                  let data = await SearchLocations(searchedQuery.trim());
                  setLocations({ details: data, error: "" });
                } catch (err) {
                  setLocations({ details: [], error: err.message });
                }
              }}
            >
              <i className="ti ti-search"></i>
            </button>
          </div>
          <table className="memory-table" ref={tableRef}>
            <thead>
              <tr>
                <th>
                  <input
                    title="Select All"
                    type="checkbox"
                    onClick={() => {
                      let names = locations.details.map((ele) => ele[1]);
                      setToDelete(names);
                      if (tbodyRef.current && !selectAll) {
                        tbodyRef.current
                          .querySelectorAll('input[type="checkbox"]')
                          .forEach((ele) => (ele.checked = true));
                        setSelectAll(true);
                      } else if (tbodyRef.current && selectAll) {
                        tbodyRef.current
                          .querySelectorAll('input[type="checkbox"]')
                          .forEach((ele) => (ele.checked = false));
                        setSelectAll(false);
                      }
                    }}
                  />
                </th>
                <th>Foldername</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody ref={tbodyRef}>
              {!locations.error &&
                locations.details.map((loc) => (
                  <tr key={loc[0]}>
                    <td>
                      <input
                        type="checkbox"
                        onClick={(e) => {
                          if (e.target.checked) {
                            setToDelete((prev) => [...prev, loc[1]]);
                          } else {
                            let filteredNames = toDelete.filter(
                              (ele) => ele !== loc[1],
                            );
                            setToDelete(filteredNames);
                          }
                        }}
                      />
                    </td>
                    <td>
                      {loc[2].split("\\").pop()
                        ? loc[2].split("\\").pop()
                        : loc[1].toUpperCase()}
                    </td>
                    <td>{loc[2]}</td>
                  </tr>
                ))}
              {!locations.details && locations.error && (
                <p
                  style={{
                    textAlign: "center",
                    padding: "30px",
                    fontSize: "18px",
                  }}
                >
                  Error Occurred: {locations.error}
                </p>
              )}
            </tbody>
          </table>
          {locations.details.length == 0 && (
            <p
              style={{
                textAlign: "center",
                padding: "30px",
                fontSize: "18px",
              }}
            >
              No Paths Exist!
            </p>
          )}
          <button className="delete-btn" onClick={deletePaths}>
            <i className="ti ti-trash"></i>
          </button>
        </div>
        <div className="section-2">
          <button className="upsert-btn" onClick={openFolderPicker}>
            <i className="ti ti-plus"></i> Add Path
          </button>
          <table className="upsert-table">
            <thead>
              <tr>
                <th>Foldername</th>
                <th>Path</th>
              </tr>
            </thead>
            <tbody>
              {pickedFolder.map((path, id) => (
                <>
                  <tr key={id}>
                    <td>{path.split("\\").pop() ? path.split('\\').pop() : path[0].toUpperCase()}</td>
                    <td>{path}</td>
                  </tr>
                </>
              ))}
            </tbody>
          </table>
          <button className="insert-btn" onClick={insertPaths}>
            Insert Paths
          </button>
        </div>
      </div>
    </>
  );
}
