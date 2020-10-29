import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Auth from '../routes/Auth';
import Home from '../routes/Home';
import About from './pages/About/About';
import Record from './pages/Record/Record';
import CxrTest from './pages/CxrTest/CxrTest';
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
          <Route path='/' exact component={Home} />
          <Route path='/about' component={About} />
          <Route path='/record' component={Record} />
          <Route path='/cxrtest' component={CxrTest} />
        </> : <Route>
          <Route path='/' exact component={Home} />
          <Route path='/about' component={About} />
          <Route path='/record' component={Record} />
        </Route>}
      </Switch>
      <Footer />
    </Router>
  )
}
export default AppRouter;