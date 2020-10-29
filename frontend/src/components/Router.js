import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Auth from '../routes/Auth';
import Home from '../routes/Home';
import Navbar from './Navbar';
import Footer from './Footer';


const AppRouter = () => {
  const[isLoggedIn, setIsLoggedIn] = useState(true);
  return (
    <Router>
      <Navbar />
      <Switch>
        {isLoggedIn ? 
        <>
          <Route>
            <Home />
          </Route>
        </> : <Route><Auth /></Route>}
      </Switch>
      <Footer />
    </Router>
  )
}
export default AppRouter;