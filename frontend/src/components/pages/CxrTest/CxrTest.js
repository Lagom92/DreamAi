import axios from 'axios';
// import { BrowserRouter, Route, Link } from 'react-router-dom';
import HeroSection from '../../HeroSection';
import { homeObjOne } from './Data';

async function makeRequest() {
    const config = {
        method: 'get',
        url: 'http://localhost:8000/predict/image/1'
    }
    let res = await axios(config)
    console.log(res.data);
}
makeRequest();

export default function CxrTest() {
    return (
      <>
        <HeroSection {...homeObjOne} />
      </>
    );
  }
