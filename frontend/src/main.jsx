import React, { useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { GeoJSON, MapContainer, Marker, Popup, TileLayer, Tooltip, useMap, useMapEvents } from "react-leaflet";
import L from "leaflet";
import "leaflet-draw";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import { Download, FileInput, MapPin, Pentagon, Route, ShieldAlert, SquarePen, TestTube2 } from "lucide-react";
import "./styles.css";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

const featureTypes = {
  borehole: { prefix: "BH", label: "Borehole", icon: MapPin },
  dcp: { prefix: "DCP", label: "DCP", icon: TestTube2 },
  test_pit: { prefix: "TP", label: "Test pit", icon: SquarePen },
  sample_point: { prefix: "SP", label: "Sample", icon: MapPin },
  site_boundary: { prefix: "SB", label: "Boundary", icon: Pentagon },
  access_path: { prefix: "AP", label: "Access", icon: Route },
  exclusion_zone: { prefix: "EZ", label: "Exclusion", icon: ShieldAlert }
};

function nextLabel(type, features) {
  const prefix = featureTypes[type].prefix;
  const count = features.filter((feature) => feature.properties.feature_type === type).length + 1;
  return `${prefix}${String(count).padStart(2, "0")}`;
}

function makeMarkerIcon(type, selected) {
  const colors = {
    borehole: "#0f766e",
    dcp: "#b45309",
    test_pit: "#7c3aed",
    sample_point: "#2563eb",
    access_path: "#334155",
    exclusion_zone: "#dc2626"
  };
  const color = colors[type] ?? "#0f172a";
  return L.divIcon({
    className: "",
    html: `<span class="map1-marker ${selected ? "selected" : ""}" style="--marker-color:${color}"></span>`,
    iconSize: [22, 22],
    iconAnchor: [11, 11]
  });
}

function buildFeature(type, label, latlng) {
  const common = {
    id: crypto.randomUUID(),
    feature_type: type,
    label,
    coordinate_system: "WGS84",
    latitude: Number(latlng.lat.toFixed(7)),
    longitude: Number(latlng.lng.toFixed(7)),
    easting: null,
    northing: null,
    mga_zone: null,
    source: "map_click",
    linked_autosoil_record: null
  };

  const byType = {
    borehole: {
      borehole_id: label,
      surface_rl: null,
      total_depth: null,
      start_date: null,
      end_date: null,
      drilling_method: null,
      logged_by: null,
      water_level: null,
      remarks: null,
      linked_log_pdf: null,
      linked_gint_data: null
    },
    dcp: {
      dcp_id: label,
      test_depth: null,
      blows_per_100mm: null,
      refusal_depth: null,
      notes: null,
      linked_report: null
    },
    test_pit: {
      test_pit_id: label,
      depth: null,
      excavation_method: null,
      logged_by: null,
      groundwater_observed: null,
      notes: null
    },
    sample_point: {
      sample_id: label,
      sample_type: null,
      depth: null,
      notes: null
    }
  };

  return {
    type: "Feature",
    geometry: {
      type: "Point",
      coordinates: [Number(latlng.lng.toFixed(7)), Number(latlng.lat.toFixed(7))]
    },
    properties: { ...common, ...(byType[type] ?? {}) }
  };
}

function buildDrawFeature(type, layer) {
  const geojson = layer.toGeoJSON();
  const label = type === "access_path" ? "Access path" : type === "exclusion_zone" ? "Exclusion zone" : "Site boundary";
  return {
    ...geojson,
    properties: {
      id: crypto.randomUUID(),
      feature_type: type,
      label,
      coordinate_system: "WGS84",
      source: "draw_tool",
      remarks: null
    }
  };
}

function PlacementEvents({ mode, features, onCreate, onCoordinate }) {
  useMapEvents({
    mousemove(event) {
      onCoordinate(event.latlng);
    },
    click(event) {
      if (!["borehole", "dcp", "test_pit", "sample_point"].includes(mode)) return;
      const label = nextLabel(mode, features);
      onCreate(buildFeature(mode, label, event.latlng));
    }
  });
  return null;
}

function DrawControls({ mode, onCreate }) {
  const map = useMap();
  const modeRef = useRef(mode);
  const onCreateRef = useRef(onCreate);

  useEffect(() => {
    modeRef.current = mode;
  }, [mode]);

  useEffect(() => {
    onCreateRef.current = onCreate;
  }, [onCreate]);

  useEffect(() => {
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const control = new L.Control.Draw({
      position: "topleft",
      draw: {
        marker: false,
        circle: false,
        circlemarker: false,
        rectangle: false,
        polygon: {
          allowIntersection: false,
          showArea: true,
          shapeOptions: { color: "#0f766e", weight: 3 }
        },
        polyline: {
          shapeOptions: { color: "#334155", weight: 4 }
        }
      },
      edit: {
        featureGroup: drawnItems,
        remove: true
      }
    });

    map.addControl(control);
    map.on(L.Draw.Event.CREATED, (event) => {
      drawnItems.addLayer(event.layer);
      const currentMode = modeRef.current;
      const type = currentMode === "exclusion_zone" ? "exclusion_zone" : event.layerType === "polyline" ? "access_path" : "site_boundary";
      onCreateRef.current(buildDrawFeature(type, event.layer));
    });

    return () => {
      map.removeControl(control);
      map.removeLayer(drawnItems);
    };
  }, [map]);

  return null;
}

function ToolBar({ mode, setMode, onExportGeoJson, onExportCsv, onImportCsv, onSave, onLoad }) {
  return (
    <div className="toolbar" aria-label="Map tools">
      {["borehole", "dcp", "test_pit", "sample_point", "site_boundary", "access_path", "exclusion_zone"].map((type) => {
        const Icon = featureTypes[type].icon;
        return (
          <button key={type} className={mode === type ? "active" : ""} onClick={() => setMode(type)} title={`Add ${featureTypes[type].label}`}>
            <Icon size={18} />
            <span>{featureTypes[type].label}</span>
          </button>
        );
      })}
      <label className="button-like" title="Import borehole CSV">
        <FileInput size={18} />
        <span>Import CSV</span>
        <input type="file" accept=".csv,text/csv" onChange={onImportCsv} />
      </label>
      <button onClick={onExportGeoJson} title="Export GeoJSON">
        <Download size={18} />
        <span>GeoJSON</span>
      </button>
      <button onClick={onExportCsv} title="Export CSV">
        <Download size={18} />
        <span>CSV</span>
      </button>
      <button onClick={onSave}>Save</button>
      <button onClick={onLoad}>Load</button>
    </div>
  );
}

function FeatureEditor({ feature, onChange, onClose }) {
  if (!feature) {
    return (
      <aside className="editor empty">
        <h2>Map1</h2>
        <p>Select or place an investigation point to edit AS1726-style metadata.</p>
      </aside>
    );
  }

  const props = feature.properties;
  const set = (key, value) => {
    const updated = {
      ...feature,
      properties: { ...props, [key]: value }
    };
    if (key === "latitude" || key === "longitude") {
      const lat = key === "latitude" ? Number(value) : Number(props.latitude);
      const lng = key === "longitude" ? Number(value) : Number(props.longitude);
      if (Number.isFinite(lat) && Number.isFinite(lng)) {
        updated.geometry = { ...feature.geometry, coordinates: [lng, lat] };
      }
    }
    onChange(updated);
  };

  const type = props.feature_type;
  const fields = {
    borehole: ["borehole_id", "latitude", "longitude", "surface_rl", "total_depth", "start_date", "end_date", "drilling_method", "logged_by", "water_level", "remarks", "linked_log_pdf", "linked_gint_data"],
    dcp: ["dcp_id", "latitude", "longitude", "test_depth", "blows_per_100mm", "refusal_depth", "notes", "linked_report"],
    test_pit: ["test_pit_id", "latitude", "longitude", "depth", "excavation_method", "logged_by", "groundwater_observed", "notes"],
    sample_point: ["sample_id", "latitude", "longitude", "sample_type", "depth", "notes"]
  }[type] ?? ["label", "remarks"];

  return (
    <aside className="editor">
      <div className="editor-header">
        <div>
          <span className="eyebrow">{featureTypes[type]?.label ?? "Feature"}</span>
          <h2>{props.label}</h2>
        </div>
        <button className="icon-button" onClick={onClose}>x</button>
      </div>
      <div className="field-grid">
        {fields.map((field) => (
          <label key={field}>
            <span>{field.replaceAll("_", " ")}</span>
            <input value={props[field] ?? ""} onChange={(event) => set(field, event.target.value)} />
          </label>
        ))}
      </div>
    </aside>
  );
}

function download(filename, text, type) {
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

function toCsv(features) {
  const headers = ["type", "id", "latitude", "longitude", "easting", "northing", "zone", "surface_rl", "total_depth", "start_date", "end_date", "method", "logged_by", "water_level", "remarks", "linked_log_pdf"];
  const rows = features.map((feature) => {
    const p = feature.properties;
    return [
      p.feature_type,
      p.borehole_id ?? p.dcp_id ?? p.test_pit_id ?? p.sample_id ?? p.label,
      p.latitude,
      p.longitude,
      p.easting ?? "",
      p.northing ?? "",
      p.mga_zone ?? "",
      p.surface_rl ?? "",
      p.total_depth ?? p.test_depth ?? p.depth ?? "",
      p.start_date ?? "",
      p.end_date ?? "",
      p.drilling_method ?? p.excavation_method ?? "",
      p.logged_by ?? "",
      p.water_level ?? "",
      p.remarks ?? p.notes ?? "",
      p.linked_log_pdf ?? p.linked_report ?? ""
    ].map((value) => `"${String(value ?? "").replaceAll('"', '""')}"`).join(",");
  });
  return [headers.join(","), ...rows].join("\n");
}

function parseCsv(text) {
  const [headerLine, ...lines] = text.trim().split(/\r?\n/);
  const headers = parseCsvLine(headerLine).map((h) => h.trim());
  return lines.filter(Boolean).map((line) => {
    const values = parseCsvLine(line);
    return Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""]));
  });
}

function parseCsvLine(line) {
  const values = [];
  let value = "";
  let quoted = false;

  for (let index = 0; index < line.length; index += 1) {
    const char = line[index];
    const next = line[index + 1];

    if (char === '"' && quoted && next === '"') {
      value += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      values.push(value);
      value = "";
    } else {
      value += char;
    }
  }

  values.push(value);
  return values;
}

function App() {
  const [features, setFeatures] = useState([]);
  const [mode, setMode] = useState("borehole");
  const [selectedId, setSelectedId] = useState(null);
  const [coordinate, setCoordinate] = useState(null);
  const projectId = useRef("demo-project");

  const selectedFeature = useMemo(() => features.find((feature) => feature.properties.id === selectedId), [features, selectedId]);
  const pointFeatures = features.filter((feature) => feature.geometry.type === "Point");
  const drawnFeatures = features.filter((feature) => feature.geometry.type !== "Point");

  const upsertFeature = (feature) => {
    setFeatures((current) => current.map((item) => item.properties.id === feature.properties.id ? feature : item));
  };

  const addFeature = (feature) => {
    setFeatures((current) => [...current, feature]);
    setSelectedId(feature.properties.id);
  };

  const featureCollection = { type: "FeatureCollection", features };

  const importCsv = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    const rows = parseCsv(await file.text());
    const imported = rows.map((row) => {
      const type = row.type || "borehole";
      const lat = Number(row.latitude);
      const lng = Number(row.longitude);
      const label = row.id || nextLabel(type, features);
      return buildFeature(type, label, { lat, lng });
    }).filter((feature) => Number.isFinite(feature.properties.latitude) && Number.isFinite(feature.properties.longitude));
    setFeatures((current) => [...current, ...imported]);
  };

  const saveProject = async () => {
    await fetch(`${API_BASE}/api/projects/${projectId.current}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: projectId.current, name: "Demo Site Investigation", geojson: featureCollection })
    });
  };

  const loadProject = async () => {
    const response = await fetch(`${API_BASE}/api/projects/${projectId.current}`);
    if (!response.ok) return;
    const project = await response.json();
    setFeatures(project.geojson?.features ?? []);
  };

  return (
    <main className="app-shell">
      <section className="map-section">
        <div className="top-strip">
          <div>
            <strong>AutoSoil Logger Map1</strong>
            <span>WGS84 field map | calibration pending</span>
          </div>
          <span>{coordinate ? `${coordinate.lat.toFixed(6)}, ${coordinate.lng.toFixed(6)}` : "Move over map"}</span>
        </div>
        <ToolBar
          mode={mode}
          setMode={setMode}
          onExportGeoJson={() => download("map1-project.geojson", JSON.stringify(featureCollection, null, 2), "application/geo+json")}
          onExportCsv={() => download("map1-investigation-points.csv", toCsv(features), "text/csv")}
          onImportCsv={importCsv}
          onSave={saveProject}
          onLoad={loadProject}
        />
        <MapContainer center={[-33.8688, 151.2093]} zoom={17} className="map">
          <TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <PlacementEvents mode={mode} features={features} onCreate={addFeature} onCoordinate={setCoordinate} />
          <DrawControls mode={mode} onCreate={addFeature} />
          {drawnFeatures.map((feature) => (
            <GeoJSON
              key={feature.properties.id}
              data={feature}
              style={() => ({
                color: feature.properties.feature_type === "exclusion_zone" ? "#dc2626" : feature.properties.feature_type === "access_path" ? "#334155" : "#0f766e",
                weight: feature.properties.feature_type === "access_path" ? 4 : 3,
                fillOpacity: feature.properties.feature_type === "exclusion_zone" ? 0.16 : 0.08
              })}
              eventHandlers={{ click: () => setSelectedId(feature.properties.id) }}
            />
          ))}
          {pointFeatures.map((feature) => {
            const [lng, lat] = feature.geometry.coordinates;
            const selected = selectedId === feature.properties.id;
            return (
              <Marker
                key={feature.properties.id}
                position={[lat, lng]}
                icon={makeMarkerIcon(feature.properties.feature_type, selected)}
                eventHandlers={{ click: () => setSelectedId(feature.properties.id) }}
              >
                <Tooltip permanent direction="top" offset={[0, -10]}>{feature.properties.label}</Tooltip>
                <Popup>{featureTypes[feature.properties.feature_type]?.label}: {feature.properties.label}</Popup>
              </Marker>
            );
          })}
        </MapContainer>
      </section>
      <FeatureEditor feature={selectedFeature} onChange={upsertFeature} onClose={() => setSelectedId(null)} />
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
