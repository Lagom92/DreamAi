import React from 'react'
// import { BrowserRouter, Route, Link } from 'react-router-dom';
import HeroSection from '../../HeroSection';
import { homeObjOne } from './Data';
import Results from './Results';

// async function makeRequest() {
//     const config = {
//         method: 'get',
//         url: 'http://localhost:8000/predict/image/1'
//     }
//     let res = await axios(config)
//     console.log(res.data);
// }
// makeRequest();
function CxrTest() {
  return (
    <>
      <HeroSection {...homeObjOne} />
      <Results />
    </>
  );
}

export default CxrTest;

// export default function CxrTest() {
// }
