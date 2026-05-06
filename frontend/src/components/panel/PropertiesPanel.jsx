import React from 'react';
import './PropertiesPanel.css';

const DRILLING_METHODS = [
  'Solid Flight Auger (SFA)',
  'Hollow Flight Auger (HFA)',
  'Wash Boring',
  'Rotary Mud Flush',
  'Cable Percussion',
  'Window Sampler',
];

const PropertiesPanel = ({ feature, onChange, onSave, onClose }) => {
  if (!feature) {
    return (
      <div className="panel panel--empty">
        <div className="panel-hint">
          <span className="panel-hint__icon">📍</span>
          <p>Click the map to place a marker, or select an existing feature to edit its properties.</p>
        </div>
      </div>
    );
  }

  const props = feature.properties || {};
  const type = feature.properties?.feature_type || 'borehole';

  const handleChange = (key, value) => {
    onChange({ ...feature, properties: { ...props, [key]: value } });
  };

  return (
    <div className="panel">
      <div className="panel__header">
        <div className="panel__badge panel__badge--">{type.toUpperCase()}</div>
        <h2 className="panel__title">{props.label || 'New Feature'}</h2>
        <button className="panel__close" onClick={onClose}>✕</button>
      </div>

      <div className="panel__body">
        {/* === SHARED FIELDS === */}
        <div className="field-group">
          <label className="field-label">ID / Label</label>
          <input className="field-input" value={props.label || ''} onChange={e => handleChange('label', e.target.value)} placeholder="BH01" />
        </div>
        <div className="field-row">
          <div className="field-group">
            <label className="field-label">Latitude</label>
            <input className="field-input" value={props.latitude || ''} onChange={e => handleChange('latitude', e.target.value)} placeholder="-33.8688" readOnly />
          </div>
          <div className="field-group">
            <label className="field-label">Longitude</label>
            <input className="field-input" value={props.longitude || ''} onChange={e => handleChange('longitude', e.target.value)} placeholder="151.2093" readOnly />
          </div>
        </div>

        {/* === BOREHOLE FIELDS === */}
        {(type === 'borehole') && (
          <>
            <hr className="panel__divider" />
            <p className="panel__section-label">Borehole Data (AS1726)</p>
            <div className="field-row">
              <div className="field-group">
                <label className="field-label">Surface RL (m)</label>
                <input className="field-input" type="number" value={props.surface_rl || ''} onChange={e => handleChange('surface_rl', e.target.value)} placeholder="12.5" />
              </div>
              <div className="field-group">
                <label className="field-label">Total Depth (m)</label>
                <input className="field-input" type="number" value={props.total_depth || ''} onChange={e => handleChange('total_depth', e.target.value)} placeholder="15.0" />
              </div>
            </div>
            <div className="field-group">
              <label className="field-label">Drilling Method</label>
              <select className="field-select" value={props.drilling_method || ''} onChange={e => handleChange('drilling_method', e.target.value)}>
                <option value="">-- Select --</option>
                {DRILLING_METHODS.map(m => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
            <div className="field-row">
              <div className="field-group">
                <label className="field-label">Start Date</label>
                <input className="field-input" type="date" value={props.start_date || ''} onChange={e => handleChange('start_date', e.target.value)} />
              </div>
              <div className="field-group">
                <label className="field-label">End Date</label>
                <input className="field-input" type="date" value={props.end_date || ''} onChange={e => handleChange('end_date', e.target.value)} />
              </div>
            </div>
            <div className="field-row">
              <div className="field-group">
                <label className="field-label">Water Level (m)</label>
                <input className="field-input" type="number" value={props.water_level || ''} onChange={e => handleChange('water_level', e.target.value)} placeholder="4.5" />
              </div>
              <div className="field-group">
                <label className="field-label">Logged By</label>
                <input className="field-input" value={props.logged_by || ''} onChange={e => handleChange('logged_by', e.target.value)} placeholder="JS" />
              </div>
            </div>
          </>
        )}

        {/* === DCP FIELDS === */}
        {(type === 'dcp') && (
          <>
            <hr className="panel__divider" />
            <p className="panel__section-label">DCP Test Data</p>
            <div className="field-row">
              <div className="field-group">
                <label className="field-label">Test Depth (m)</label>
                <input className="field-input" type="number" value={props.test_depth || ''} onChange={e => handleChange('test_depth', e.target.value)} />
              </div>
              <div className="field-group">
                <label className="field-label">Refusal Depth (m)</label>
                <input className="field-input" type="number" value={props.refusal_depth || ''} onChange={e => handleChange('refusal_depth', e.target.value)} />
              </div>
            </div>
            <div className="field-group">
              <label className="field-label">Blows per 100mm</label>
              <input className="field-input" type="number" value={props.blows_per_100mm || ''} onChange={e => handleChange('blows_per_100mm', e.target.value)} />
            </div>
          </>
        )}

        {/* === TEST PIT FIELDS === */}
        {(type === 'test_pit') && (
          <>
            <hr className="panel__divider" />
            <p className="panel__section-label">Test Pit Data</p>
            <div className="field-row">
              <div className="field-group">
                <label className="field-label">Pit Depth (m)</label>
                <input className="field-input" type="number" value={props.pit_depth || ''} onChange={e => handleChange('pit_depth', e.target.value)} />
              </div>
              <div className="field-group">
                <label className="field-label">Logged By</label>
                <input className="field-input" value={props.logged_by || ''} onChange={e => handleChange('logged_by', e.target.value)} />
              </div>
            </div>
          </>
        )}

        {/* === SHARED REMARKS === */}
        <hr className="panel__divider" />
        <div className="field-group">
          <label className="field-label">Remarks</label>
          <textarea className="field-textarea" value={props.remarks || ''} onChange={e => handleChange('remarks', e.target.value)} placeholder="e.g. Stiff clay from 2m, hit rock at 14.5m..." rows={3} />
        </div>
      </div>

      <div className="panel__footer">
        <button className="btn btn--secondary" onClick={onClose}>Cancel</button>
        <button className="btn btn--primary" onClick={onSave}>Save Feature</button>
      </div>
    </div>
  );
};

export default PropertiesPanel;