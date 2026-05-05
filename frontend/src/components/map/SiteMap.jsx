import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css';

const SiteMap = () => {
  const defaultCenter = [-33.8688, 151.2093]; // Sydney CBD as default

  return (
    <MapContainer center={defaultCenter} zoom={13} style={{ width: '100%', height: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {/* Sample Marker */}
      <Marker position={[-33.8688, 151.2093]}>
        <Popup>
          <strong>BH01</strong><br />
          Total Depth: 15.0m<br />
          Drilling Method: Solid Flight Auger
        </Popup>
      </Marker>
    </MapContainer>
  );
};

export default SiteMap;