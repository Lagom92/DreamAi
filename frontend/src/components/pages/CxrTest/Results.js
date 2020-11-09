import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "./Results.css"


function Results() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchResults = async () => {
      try{
        setError(null);
        setResults(null);
        setLoading(true);

        const response = await axios.get(
          // 'http://localhost:8001/api/boards/'
          'http://localhost:8001/predict/image/'
        );
        // console.log(response.data);
        setResults(response.data);
      } catch (e) {
        setError(e);
      }
      setLoading(false);
    }
    fetchResults();
  }, []);

  // if (loading) return <div>Loading ...</div>
  // if (error) return<div>Error !!</div>
  if (!results) return null;
  
  return(
    <div className="cxrResult">
      <ul>
        {results.map(result => (
          <li key={result.id}>
            {/* {result.title} ({result.contents}) */}
            <img src={result.photo} alt={result.prediction} /> - ({result.prediction})
          </li>
        ))}
      </ul>
    </div>
  );

}

export default Results;