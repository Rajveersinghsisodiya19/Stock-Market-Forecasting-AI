import { buildForecastSeries, formatAxisValue } from '../utils/chartGeometry';

/**
 * Single-field forecast chart — actual history + predicted path,
 * with a vertical forecast boundary and horizontal start/end price guides.
 */
function ForecastChart({ title, field, history, predictions, modelColorVar }) {
  if (!history?.length || !predictions?.length) {
    return (
      <div className="fc-card">
        <h4 className="fc-title">{title}</h4>
        <div className="fc-placeholder">Run a prediction to see this chart.</div>
      </div>
    );
  }

  const historyValues = history.map((p) => p[field]);
  const predValues = predictions.map((p) => p[field]);
  const historyDates = history.map((p) => p.date);
  const predDates = predictions.map((p) => p.date);

  const geo = buildForecastSeries(historyValues, predValues, historyDates, predDates);
  if (!geo) return null;

  const {
    historyPolyline,
    predPolyline,
    forecastX,
    endX,
    startY,
    endY,
    startValue,
    endValue,
    yTicks,
    xLabels,
  } = geo;

  const startLabel = formatAxisValue(startValue);
  const endLabel = formatAxisValue(endValue);

  return (
    <div className="fc-card">
      <h4 className="fc-title">{title}</h4>

      <div className="fc-legend">
        <span className="fc-legend-item">
          <span className="fc-swatch fc-swatch-actual" />
          Actual (60 days)
        </span>
        <span className="fc-legend-item">
          <span
            className="fc-swatch fc-swatch-pred"
            style={{ backgroundColor: `var(${modelColorVar})` }}
          />
          Predicted
        </span>
        <span className="fc-legend-item">
          <span className="fc-swatch fc-swatch-start-hline" />
          Start price
        </span>
        <span className="fc-legend-item">
          <span className="fc-swatch fc-swatch-end-hline" />
          End price
        </span>
      </div>

      <svg className="fc-svg" viewBox="0 0 960 300" role="img" aria-label={title}>
        <g className="chart-grid-lines">
          <line x1="56" y1="24" x2="56" y2="250" />
          {yTicks.map((tick, i) => (
            <line
              key={i}
              x1="56"
              y1={tick.y.toFixed(2)}
              x2="860"
              y2={tick.y.toFixed(2)}
              strokeDasharray={i === yTicks.length - 1 ? undefined : '4 4'}
            />
          ))}
        </g>

        <g className="chart-axis-labels">
          {yTicks.map((tick, i) => (
            <text key={i} x="50" y={(tick.y + 4).toFixed(2)} textAnchor="end">
              {formatAxisValue(tick.value)}
            </text>
          ))}
          <text x="56" y="270" textAnchor="start">
            {xLabels.first}
          </text>
          <text x={forecastX.toFixed(1)} y="270" textAnchor="middle">
            {xLabels.boundary}
          </text>
          <text x="860" y="270" textAnchor="end">
            {xLabels.last}
          </text>
          <text x="458" y="290" textAnchor="middle" className="axis-title">
            Date
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

        {/* Shaded band + two boundary lines marking the predicted trading day */}
        <rect
          className="fc-forecast-region"
          x={forecastX.toFixed(2)}
          y="24"
          width={Math.max(endX - forecastX, 1).toFixed(2)}
          height="226"
        />
        <line
          className="fc-forecast-vline"
          x1={forecastX.toFixed(1)}
          y1="18"
          x2={forecastX.toFixed(1)}
          y2="250"
        />
        <line
          className="fc-forecast-vline"
          x1={endX.toFixed(1)}
          y1="18"
          x2={endX.toFixed(1)}
          y2="250"
        />

        {/* Horizontal guide at last actual price (forecast start level) */}
        <line
          className="fc-hline-start"
          x1="56"
          y1={startY.toFixed(2)}
          x2="860"
          y2={startY.toFixed(2)}
        />
        <text
          className="fc-hline-label fc-hline-label-start"
          x="864"
          y={(startY - 3).toFixed(2)}
          textAnchor="start"
        >
          {startLabel}
        </text>

        {/* Horizontal guide at final predicted price */}
        <line
          className="fc-hline-end"
          x1="56"
          y1={endY.toFixed(2)}
          x2="860"
          y2={endY.toFixed(2)}
          style={{ stroke: `var(${modelColorVar})` }}
        />
        <text
          className="fc-hline-label fc-hline-label-end"
          x="864"
          y={(endY + 11).toFixed(2)}
          textAnchor="start"
          style={{ fill: `var(${modelColorVar})` }}
        >
          {endLabel}
        </text>

        <polyline className="fc-line-actual" points={historyPolyline} />

        <polyline
          className="fc-line-pred"
          points={predPolyline}
          style={{ stroke: `var(${modelColorVar})` }}
        />

        {/* Endpoint marker on final predicted day */}
        <circle
          className="fc-end-point"
          cx={endX.toFixed(2)}
          cy={endY.toFixed(2)}
          r="4"
          style={{ fill: `var(${modelColorVar})` }}
        />
      </svg>
    </div>
  );
}

export default ForecastChart;
