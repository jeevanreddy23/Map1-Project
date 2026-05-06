import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import '@geoman-io/leaflet-geoman-free';
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css';
import 'leaflet/dist/leaflet.css';

// Component to initialize Geoman controls
const GeomanControls = () => {
  const map = useMap();

  useEffect(() => {
    // Add Geoman controls
    map.pm.addControls({
      position: 'topleft',
      drawCircleMarker: false,
      drawPolyline: true,
      drawRectangle: true,
      drawPolygon: true,
      drawCircle: false,
      editMode: true,
      dragMode: true,
      cutPolygon: false,
      removalMode: true,
    });

    // Listen to draw events
    map.on('pm:create', (e) => {
      console.log('Shape created:', e.layer.toGeoJSON());
      // Here we would dispatch to Zustand/Context to show the property panel
      // and eventually POST to /api/features
    });

    return () => {
      map.pm.removeControls();
    };
  }, [map]);

  return null;
};

const SiteMap = () => {
  const defaultCenter = [-33.8688, 151.2093]; // Sydney CBD as default

  return (
    <MapContainer center={defaultCenter} zoom={13} style={{ width: '100%', height: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      
      <GeomanControls />

      {/* Sample Marker (BH01) */}
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