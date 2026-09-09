import ForecastChart from './ForecastChart';

/**
 * One model's section: heading + 2×2 grid of four ForecastChart instances.
 *
 * Props:
 *   modelName   – display name, e.g. "Random Forest"
 *   modelKey    – CSS key: "rf" | "xgb" | "lstm"
 *   colorVar    – CSS custom-property for the model accent, e.g. "--color-rf"
 *   history     – array of {date, open, close, high, low, volume} (60 points)
 *   predictions – array of {date, open, close, high, low}
 */
function ModelForecastSection({ modelName, modelKey, colorVar, history, predictions }) {
  const FIELDS = [
    { field: 'open',  label: 'Open' },
    { field: 'close', label: 'Close' },
    { field: 'high',  label: 'High' },
    { field: 'low',   label: 'Low' },
  ];

  return (
    <div className={`mfs-block mfs-${modelKey}`}>
      <div className="mfs-header">
        <span className="mfs-dot" style={{ background: `var(${colorVar})` }} />
        <h3 className="mfs-model-name">{modelName}</h3>
      </div>

      <div className="mfs-grid">
        {FIELDS.map(({ field, label }) => (
          <ForecastChart
            key={field}
            title={`${label} \u2014 Actual vs Predicted`}
            field={field}
            history={history}
            predictions={predictions}
            modelColorVar={colorVar}
          />
        ))}
      </div>
    </div>
  );
}

export default ModelForecastSection;
