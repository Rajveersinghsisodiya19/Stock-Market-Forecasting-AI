import { buildMultiSeries } from '../utils/chartGeometry';

const SERIES = [
  { key: 'actual_open', label: 'Actual Open', className: 'eval-actual-open' },
  { key: 'predicted_open', label: 'Predicted Open', className: 'eval-pred-open' },
  { key: 'actual_close', label: 'Actual Close', className: 'eval-actual-close' },
  { key: 'predicted_close', label: 'Predicted Close', className: 'eval-pred-close' },
  { key: 'actual_high', label: 'Actual High', className: 'eval-actual-high' },
  { key: 'predicted_high', label: 'Predicted High', className: 'eval-pred-high' },
  { key: 'actual_low', label: 'Actual Low', className: 'eval-actual-low' },
  { key: 'predicted_low', label: 'Predicted Low', className: 'eval-pred-low' },
];

function EvaluationChart({ modelKey, data }) {
  if (!data) {
    return (
      <div className={`chart-card chart-card-${modelKey}`}>
        <h3 className="chart-card-title">Loading…</h3>
      </div>
    );
  }

  const seriesMap = Object.fromEntries(SERIES.map((s) => [s.key, data[s.key]]));
  const geometry = buildMultiSeries(seriesMap);

  return (
    <div className={`chart-card chart-card-${modelKey} eval-chart-card`}>
      <h3 className="chart-card-title">{data.title}</h3>

      <div className="eval-legend">
        {SERIES.map((s) => (
          <span key={s.key} className="legend-item">
            <span className={`legend-swatch ${s.className}`} />
            {s.label}
          </span>
        ))}
      </div>

      <svg
        className="price-chart eval-chart"
        viewBox="0 0 900 300"
        role="img"
        aria-label={data.title}
      >
        <g className="chart-grid-lines">
          <line x1="56" y1="24" x2="56" y2="250" />
          <line x1="56" y1="250" x2="860" y2="250" />
          <line x1="56" y1="80" x2="860" y2="80" strokeDasharray="4 4" />
          <line x1="56" y1="136" x2="860" y2="136" strokeDasharray="4 4" />
          <line x1="56" y1="192" x2="860" y2="192" strokeDasharray="4 4" />
        </g>

        <g className="chart-axis-labels">
          <text x="48" y="28" textAnchor="end">
            {geometry.yMaxLabel}
          </text>
          <text x="48" y="254" textAnchor="end">
            {geometry.yMinLabel}
          </text>
          <text x="56" y="274">
            0
          </text>
          <text x="458" y="274" textAnchor="middle">
            {geometry.xMidLabel}
          </text>
          <text x="860" y="274" textAnchor="end">
            {geometry.xEndLabel}
          </text>
          <text x="458" y="294" textAnchor="middle" className="axis-title">
            Test Sample
          </text>
          <text
            x="16"
            y="140"
            textAnchor="middle"
            className="axis-title"
            transform="rotate(-90 16 140)"
          >
            Price
          </text>
        </g>

        {SERIES.map((s) => (
          <polyline
            key={s.key}
            className={`eval-line ${s.className}`}
            points={geometry.polylines[s.key]}
          />
        ))}
      </svg>
    </div>
  );
}

function PriceCharts({ evaluation }) {
  return (
    <section id="charts-section" className="panel">
      <h2 className="panel-title">Model Evaluation Charts</h2>
      <p className="section-subtitle">
        Actual vs predicted Open, Close, High, and Low on the first 150 test samples (same test
        set and inverse-scaling used in model evaluation).
      </p>

      {evaluation?.error && <p className="form-error">{evaluation.error}</p>}

      <div className="chart-models">
        <EvaluationChart modelKey="rf" data={evaluation?.random_forest} />
        <EvaluationChart modelKey="xgb" data={evaluation?.xgboost} />
        <EvaluationChart modelKey="lstm" data={evaluation?.lstm} />
      </div>
    </section>
  );
}

export default PriceCharts;
