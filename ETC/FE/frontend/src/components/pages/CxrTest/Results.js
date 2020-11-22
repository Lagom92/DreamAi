import React from 'react';
import axios from 'axios';
import "./Results.css";
import useAsync from "../../useAsync";

async function getResults() {
  const response = await axios.get(
    'http://localhost:8000/predict/image/'
  );
  return response.data;
}

function Results() {

  const [state, refetch] = useAsync(getResults, []);

  const { loading, data: results, error } = state; // state.data 를 users 키워드로 조회
  if (loading) return <div>로딩중..</div>;
  if (error) return <div>에러가 발생했습니다</div>;
  if (!results) return null;

  return (
    <>
      <div className="cxrResult">
      <ul>
        {results.map(result => (
          <li key={result.id}>
            <img src={result.photo} alt={result.prediction} /> - ({result.prediction})
          </li>
        ))}
      </ul>
      {/* <button onClick={refetch}>다시 불러오기</button> */}
    </div>
    </>
  );
}

export default Results;