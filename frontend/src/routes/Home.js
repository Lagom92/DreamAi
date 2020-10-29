import React from 'react';
import HeroSection from '../components/HeroSection';
import { homeObjOne, homeObjTwo, homeObjThree, homeObjFour } from '../components/HomeData';
// import Intro from '../../Intro';

function Home() {
  
  return (
    <>
      <HeroSection {...homeObjOne} />
      <HeroSection {...homeObjThree} />
      <HeroSection {...homeObjTwo} />
      {/* <Intro /> */}
      <HeroSection {...homeObjFour} />
    </>
  );
}

export default Home;