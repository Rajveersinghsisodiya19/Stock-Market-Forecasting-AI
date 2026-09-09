import { directionArrow, directionClass, formatPct } from '../utils/predictionMetrics';

const EVALUATION_METRICS = [
  { model: 'Random Forest', mae: '0.1882', mse: '0.1495', rmse: '0.3867', r2: '0.99934' },
  { model: 'XGBoost', mae: '0.2411', mse: '0.1862', rmse: '0.4315', r2: '0.99918' },
  { model: 'LSTM', mae: '0.6465', mse: '1.5233', rmse: '1.2342', r2: '0.9933' },
];

const FIELDS = [
  { key: 'open', label: 'Open' },
  { key: 'high', label: 'High' },
  { key: 'low', label: 'Low' },
  { key: 'close', label: 'Close' },
];

const ROWS = [
  { key: 'randomForest', label: 'Random Forest' },
  { key: 'xgboost', label: 'XGBoost' },
  { key: 'lstm', label: 'LSTM' },
];

function ComparisonCell({ metric }) {
  if (!metric) return <td>--</td>;
  return (
    <td>
      <span className={`direction-cell ${directionClass(metric.direction)}`}>
        {directionArrow(metric.direction)} {formatPct(metric.pct)}
      </span>
    </td>
  );
}

function Comparison({ models }) {
  return (
    <section id="comparison-section" className="panel">
      <h2 className="panel-title">Model Comparison</h2>
      <p className="section-subtitle">
        Direction and percentage change from the last actual trading day to each model's
        next-day prediction, for every OHLC value.
      </p>

      <div className="table-wrapper">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Model</th>
              {FIELDS.map(({ key, label }) => (
                <th key={key}>{label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {ROWS.map((row) => (
              <tr key={row.key}>
                <td>{row.label}</td>
                {FIELDS.map(({ key }) => (
                  <ComparisonCell key={key} metric={models[row.key]?.[key]} />
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2 className="panel-title panel-title-spaced">Model Evaluation Metrics</h2>
      <p className="section-subtitle">Test-set performance recorded when each model was trained.</p>

      <div className="table-wrapper">
        <table className="comparison-table">
          <thead>
            <tr>
              <th>Model</th>
              <th>Test MAE ↓</th>
              <th>Test MSE ↓</th>
              <th>Test RMSE ↓</th>
              <th>Test R² ↑</th>
            </tr>
          </thead>
          <tbody>
            {EVALUATION_METRICS.map((row) => (
              <tr key={row.model}>
                <td>{row.model}</td>
                <td>{row.mae}</td>
                <td>{row.mse}</td>
                <td>{row.rmse}</td>
                <td>{row.r2}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default Comparison;
