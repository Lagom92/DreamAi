import React , { useState }from 'react'
import HeroSection from '../../HeroSection';
import { homeObjOne } from './Data';
import Results from './Results';
// import Dropzone from './Dropzone';
import SimpleDropZone from './Simple-dropzone';
import './Results.css'

function CxrTest() {
  return (
    <>
      <HeroSection {...homeObjOne} />
      <SimpleDropZone />
      <Results />
    </>
  );
}

export default CxrTest;