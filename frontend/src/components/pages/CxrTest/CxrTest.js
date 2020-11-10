import React from 'react'
import HeroSection from '../../HeroSection';
import { homeObjOne } from './Data';
import Results from './Results';
import Dropzone from './Dropzone';
import './Results.css'

function CxrTest() {
  return (
    <>
      <HeroSection {...homeObjOne} />
      <Dropzone />
      <Results />
    </>
  );
}

export default CxrTest;





