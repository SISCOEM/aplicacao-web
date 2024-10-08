CREATE TABLE IF NOT EXISTS django_content_type (
  id SERIAL PRIMARY KEY,
  app_label VARCHAR(100) NOT NULL,
  model VARCHAR(100) NOT NULL,
  UNIQUE (app_label, model)
);

INSERT INTO django_content_type (app_label, model) VALUES
  ('admin', 'logentry'),
  ('auth', 'group'),
  ('auth', 'permission'),
  ('contenttypes', 'contenttype'),
  ('equipment', 'bullet'),
  ('equipment', 'equipment'),
  ('equipment', 'model_accessory'),
  ('equipment', 'model_armament'),
  ('equipment', 'model_grenada'),
  ('equipment', 'model_wearable'),
  ('load', 'equipment_load'),
  ('load', 'load'),
  ('police', 'police'),
  ('sessions', 'session');