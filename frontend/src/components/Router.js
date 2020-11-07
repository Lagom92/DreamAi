import React from 'react';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Home from '../routes/Home';
import CxrTest from './pages/CxrTest/CxrTest';
import AudioTest from './pages/AudioTest/Audio'
import Navbar from './Navbar';
import Footer from './Footer';


const AppRouter = () => {
  // const[isLoggedIn, setIsLoggedIn] = useState(true);
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route>
          <Route path='/' exact component={Home} />
          <Route path='/audiotest' component={AudioTest} />
          <Route path='/cxrtest' component={CxrTest} />
        </Route>
      </Switch>
      <Footer />
    </Router>
  )
}
export default AppRouter;