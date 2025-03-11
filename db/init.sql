-- Create the prediction_logs table
CREATE TABLE IF NOT EXISTS prediction_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    input_features JSONB NOT NULL,
    prediction INTEGER NOT NULL,
    model_version TEXT DEFAULT '1.0',
    confidence FLOAT,
    processing_time FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_prediction_logs_timestamp ON prediction_logs(timestamp);
CREATE INDEX idx_prediction_logs_prediction ON prediction_logs(prediction);

-- Create a view for recent predictions
CREATE OR REPLACE VIEW recent_predictions AS
SELECT 
    timestamp,
    input_features,
    prediction,
    model_version,
    confidence
FROM prediction_logs
ORDER BY timestamp DESC
LIMIT 100;

-- Grants for the default user
GRANT ALL PRIVILEGES ON TABLE prediction_logs TO postgres;
GRANT ALL PRIVILEGES ON SEQUENCE prediction_logs_id_seq TO postgres;
GRANT ALL PRIVILEGES ON recent_predictions TO postgres; 