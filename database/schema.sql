CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE projects (
  id uuid PRIMARY KEY,
  name text NOT NULL,
  client_name text,
  project_number text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE sites (
  id uuid PRIMARY KEY,
  project_id uuid NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  name text NOT NULL,
  address text,
  coordinate_system text NOT NULL DEFAULT 'WGS84',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE features (
  id uuid PRIMARY KEY,
  site_id uuid NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
  feature_type text NOT NULL CHECK (feature_type IN ('borehole', 'dcp', 'test_pit', 'sample_point', 'site_boundary', 'access_path', 'exclusion_zone')),
  label text NOT NULL,
  geom geometry(Geometry, 4326) NOT NULL,
  properties jsonb NOT NULL DEFAULT '{}'::jsonb,
  source text NOT NULL DEFAULT 'manual',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX features_geom_gix ON features USING gist (geom);
CREATE INDEX features_type_idx ON features (feature_type);
CREATE INDEX features_properties_gin ON features USING gin (properties);

CREATE TABLE overlays (
  id uuid PRIMARY KEY,
  site_id uuid NOT NULL REFERENCES sites(id) ON DELETE CASCADE,
  filename text NOT NULL,
  media_type text NOT NULL,
  storage_uri text NOT NULL,
  bounds geometry(Polygon, 4326),
  opacity numeric(4, 3) NOT NULL DEFAULT 0.650,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE calibrations (
  id uuid PRIMARY KEY,
  overlay_id uuid NOT NULL REFERENCES overlays(id) ON DELETE CASCADE,
  coordinate_system text NOT NULL DEFAULT 'WGS84',
  method text NOT NULL,
  coefficients jsonb,
  residual_error numeric,
  confidence text NOT NULL DEFAULT 'low',
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE calibration_points (
  id uuid PRIMARY KEY,
  calibration_id uuid NOT NULL REFERENCES calibrations(id) ON DELETE CASCADE,
  pixel_x numeric NOT NULL,
  pixel_y numeric NOT NULL,
  geom geometry(Point, 4326),
  easting numeric,
  northing numeric,
  mga_zone text,
  description text
);

CREATE TABLE attachments (
  id uuid PRIMARY KEY,
  feature_id uuid REFERENCES features(id) ON DELETE CASCADE,
  attachment_type text NOT NULL CHECK (attachment_type IN ('borehole_log_pdf', 'dcp_report', 'gint_data', 'photo', 'other')),
  filename text NOT NULL,
  storage_uri text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

