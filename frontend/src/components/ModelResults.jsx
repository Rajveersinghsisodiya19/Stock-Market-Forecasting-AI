import { directionArrow, directionClass, formatPct } from '../utils/predictionMetrics';

const FIELDS = [
  { key: 'open', label: 'Open' },
  { key: 'high', label: 'High' },
  { key: 'low', label: 'Low' },
  { key: 'close', label: 'Close' },
];

function formatMoney(value) {
  if (value == null) return '--';
  return `$${Number(value).toFixed(2)}`;
}

function ModelCard({ id, title, cardClass, metrics }) {
  return (
    <article className={`model-card ${cardClass}`} id={id}>
      <header className="model-card-header">
        <h3>{title}</h3>
      </header>
      <dl className="model-stats">
        {FIELDS.map(({ key, label }) => {
          const m = metrics?.[key];
          return (
            <div className="model-stat" key={key}>
              <dt>Predicted {label}</dt>
              <dd className="stat-value-group">
                <span className="stat-value">{m ? formatMoney(m.value) : '--'}</span>
                <span className={m ? `stat-change ${directionClass(m.direction)}` : 'stat-change'}>
                  {m ? `${directionArrow(m.direction)} ${formatPct(m.pct)}` : '--'}
                </span>
              </dd>
            </div>
          );
        })}
      </dl>
    </article>
  );
}

function ModelResults({ models }) {
  return (
    <section id="results-section">
      <h2 className="section-title">Model Predictions</h2>
      <p className="section-subtitle">
        Predicted next-day Open, High, Low, and Close for each model, with percentage change from
        the last actual trading day (Twelve Data) to the predicted day.
      </p>

      <div className="model-grid">
        <ModelCard
          id="card-random-forest"
          title="Random Forest"
          cardClass="model-card-rf"
          metrics={models.randomForest}
        />
        <ModelCard
          id="card-lstm"
          title="LSTM"
          cardClass="model-card-lstm"
          metrics={models.lstm}
        />
        <ModelCard
          id="card-xgboost"
          title="XGBoost"
          cardClass="model-card-xgb"
          metrics={models.xgboost}
        />
      </div>
    </section>
  );
}

export default ModelResults;
