import React from 'react'
import './App.css';
import Header from './Header';
import BookCards from './BookCards';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

function App() {
  return (
    <div className="App">
      {/* {HEADER} */}
      <Header />
      <Router>
        <Switch>
          <Route path="/list">
            <h1>I am list</h1>
          </Route>
          <Route path="/profile">
            <h1>I am profile</h1>
          </Route>
          <Route path="/">
            <BookCards />
          </Route>
        </Switch>

        {/* {Tinder cards} */}
        {/* {Buttons below Tinder cards} */}
      </Router>
    </div>
  );
}

export default App;
