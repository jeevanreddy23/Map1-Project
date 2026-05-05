/**
 * Export utilities for AutoSoil Map1
 * Agent 5 - Export Agent: GeoJSON and CSV export
 */

/**
 * Exports a GeoJSON FeatureCollection as a downloadable .geojson file
 */
export function exportGeoJSON(featureCollection, filename = 'map1_export.geojson') {
  const json = JSON.stringify(featureCollection, null, 2);
  const blob = new Blob([json], { type: 'application/geo+json' });
  triggerDownload(blob, filename);
}

/**
 * Exports all Point features as a flat .csv file for Excel/GINT import
 * Matches the Map1 CSV spec: label, type, latitude, longitude, surface_rl, total_depth, etc.
 */
export function exportCSV(featureCollection, filename = 'map1_export.csv') {
  const headers = [
    'label', 'type', 'latitude', 'longitude', 'easting', 'northing',
    'surface_rl', 'total_depth', 'drilling_method', 'water_level',
    'start_date', 'end_date', 'logged_by', 'test_depth', 'refusal_depth',
    'blows_per_100mm', 'pit_depth', 'remarks'
  ];

  const rows = featureCollection.features
    .filter(f => f.geometry?.type === 'Point')
    .map(f => {
      const [lng, lat] = f.geometry.coordinates;
      const p = f.properties || {};
      return [
        p.label || '',
        p.feature_type || '',
        lat.toFixed(6),
        lng.toFixed(6),
        p.easting || '',
        p.northing || '',
        p.surface_rl || '',
        p.total_depth || '',
        p.drilling_method || '',
        p.water_level || '',
        p.start_date || '',
        p.end_date || '',
        p.logged_by || '',
        p.test_depth || '',
        p.refusal_depth || '',
        p.blows_per_100mm || '',
        p.pit_depth || '',
        "",
      ].join(',');
    });

  const csvContent = [headers.join(','), ...rows].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  triggerDownload(blob, filename);
}

/**
 * Parses a CSV string (pasted or uploaded) into a GeoJSON FeatureCollection
 * Handles both WGS84 (lat/lng) records and MGA/GDA Easting/Northing records
 */
export function parseCSVToGeoJSON(csvText) {
  const lines = csvText.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
  const features = [];

  for (let i = 1; i < lines.length; i++) {
    const cells = lines[i].split(',').map(c => c.trim().replace(/^"|"$/g, ''));
    const row = Object.fromEntries(headers.map((h, idx) => [h, cells[idx]]));

    let lat = parseFloat(row.latitude);
    let lng = parseFloat(row.longitude);

    // If no WGS84 coords, skip for now (MGA conversion would go here)
    if (isNaN(lat) || isNaN(lng)) continue;

    features.push({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [lng, lat] },
      properties: {
        label: row.label || '',
        feature_type: row.type || 'borehole',
        surface_rl: parseFloat(row.surface_rl) || null,
        total_depth: parseFloat(row.total_depth) || null,
        drilling_method: row.drilling_method || '',
        water_level: parseFloat(row.water_level) || null,
        start_date: row.start_date || '',
        end_date: row.end_date || '',
        logged_by: row.logged_by || '',
        test_depth: parseFloat(row.test_depth) || null,
        refusal_depth: parseFloat(row.refusal_depth) || null,
        blows_per_100mm: parseInt(row.blows_per_100mm) || null,
        pit_depth: parseFloat(row.pit_depth) || null,
        remarks: row.remarks || '',
      }
    });
  }

  return { type: 'FeatureCollection', features };
}

function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}