import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <img src="/octofitapp-small.png" alt="OctoFit Logo" className="navbar-logo" />
              <strong>OctoFit Tracker</strong>
            </Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">
                    Activities
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">
                    Leaderboard
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">
                    Teams
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">
                    Users
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">
                    Workouts
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="container mt-5">
              <div className="jumbotron text-center">
                <h1 className="display-4">Welcome to OctoFit Tracker!</h1>
                <p className="lead">Track your fitness journey, compete with teams, and achieve your goals.</p>
                <hr className="my-4" />
                <p>Use the navigation menu above to explore your fitness data.</p>
                
                <div className="row mt-5">
                  <div className="col-md-6 col-lg-3 mb-4">
                    <Link to="/activities" className="card-link">
                      <div className="card clickable-card">
                        <div className="card-body text-center">
                          <h2 className="display-6">🏃</h2>
                          <h5 className="card-title">Activities</h5>
                          <p className="card-text">Log your workouts and monitor your daily fitness activities.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  
                  <div className="col-md-6 col-lg-3 mb-4">
                    <Link to="/leaderboard" className="card-link">
                      <div className="card clickable-card">
                        <div className="card-body text-center">
                          <h2 className="display-6">🏆</h2>
                          <h5 className="card-title">Leaderboard</h5>
                          <p className="card-text">Check the leaderboard and see how you rank against others.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  
                  <div className="col-md-6 col-lg-3 mb-4">
                    <Link to="/users" className="card-link">
                      <div className="card clickable-card">
                        <div className="card-body text-center">
                          <h2 className="display-6">👤</h2>
                          <h5 className="card-title">Users</h5>
                          <p className="card-text">View all registered members and their team affiliations.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  
                  <div className="col-md-6 col-lg-3 mb-4">
                    <Link to="/workouts" className="card-link">
                      <div className="card clickable-card">
                        <div className="card-body text-center">
                          <h2 className="display-6">💪</h2>
                          <h5 className="card-title">Workouts</h5>
                          <p className="card-text">Access personalized workout plans tailored to your goals.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          } />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/users" element={<Users />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
