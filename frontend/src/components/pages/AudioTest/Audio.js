import React from 'react';
import HeroSection from '../../HeroSection';
import { homeObjOne } from './Data';

function Record() {
  return (
    <>
      <HeroSection {...homeObjOne} />
    </>
  );
}

export default Record;