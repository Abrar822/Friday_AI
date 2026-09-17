import "../stylesheets/memory.css";
import { useEffect, useState, useRef } from "react";
import { FetchLocations } from "../helper/MemoryConnect";
import { SearchLocations } from "../helper/MemoryConnect";

export default function Memory() {
  const searchRef = useRef(null);
  const checkboxRef = useRef(null);
  const [locations, setLocations] = useState({
    details: [],
    error: "",
  });
  const [searchedQuery, setSearchedQuery] = useState("");
  const [toDelete, setToDelete] = useState([]);

  // Runs only initially to fetch location
  useEffect(() => {
    const fetchData = async () => {
      let data = await FetchLocations();
      setLocations({ details: data, error: "" });
    };
    try {
      fetchData();
    } catch (err) {
      setError(err.message);
    }
  }, []);

  // To indirectly run the fetch location when user erases the input
  useEffect(() => {
    const runFetchLocationIndirect = async () => {
      if (searchedQuery.trim().length == 0) {
        await searchRef.current.click();
      }
    };
    runFetchLocationIndirect();
  }, [searchedQuery]);

  useEffect(() => {
    console.log(toDelete);
  }, [toDelete]);

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
          <table className="memory-table">
            <thead>
              <tr>
                <th>
                  <input type="checkbox" />
                </th>
                <th>Foldername</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
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
              {!locations.error &&
                locations.details.map((loc) => (
                  <tr key={loc[0]}>
                    <td>
                      <input
                        ref={checkboxRef}
                        type="checkbox"
                        onClick={() => {
                          if (checkboxRef.current.checked) {
                            setToDelete((prev) => [...prev, loc[1]]);
                          } else {
                            let filtered_locations = toDelete.filter(
                              (ele) => ele !== loc[1],
                            );
                            setToDelete([...filtered_locations]);
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
          <button className="delete-btn">
            <i className="ti ti-trash"></i>
          </button>
        </div>
        <div className="section-2">
          <button className="upsert-btn">
            <i className="ti ti-plus"></i> Add Path
          </button>
          <table className="upsert-table">
            <thead>
              <tr>
                <th>Path</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
    </>
  );
}
