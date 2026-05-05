import React from 'react';
import SiteMap from './components/map/SiteMap';
import './index.css';

function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1>AutoSoil Map1 🗺️</h1>
        <p>Geotechnical Site Investigation Mapping</p>
      </header>
      <main className="map-workspace">
        <SiteMap />
      </main>
    </div>
  );
}

export default App;