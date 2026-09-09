function PriceChart({ title, cardClass, lineClass, pointClass, series }) {
  const hasData = Boolean(series?.actualPoints);

  return (
    <div className={`chart-card ${cardClass}`}>
      <h3 className="chart-card-title">{title}</h3>
      <svg
        className="price-chart"
        viewBox="0 0 800 260"
        role="img"
        aria-label={`${title} price chart`}
      >
        <g className="chart-grid-lines">
          <line x1="50" y1="20" x2="50" y2="200" />
          <line x1="50" y1="200" x2="780" y2="200" />
          <line x1="50" y1="73" x2="780" y2="73" strokeDasharray="4 4" />
          <line x1="50" y1="126" x2="780" y2="126" strokeDasharray="4 4" />
          <line x1="50" y1="163" x2="780" y2="163" strokeDasharray="4 4" />
        </g>
        <g className="chart-axis-labels">
          <text x="40" y="24" textAnchor="end">
            {hasData ? series.yMaxLabel : 'High'}
          </text>
          <text x="40" y="204" textAnchor="end">
            {hasData ? series.yMinLabel : 'Low'}
          </text>
          <text x="50" y="218">
            History
          </text>
          <text x="780" y="218" textAnchor="end">
            Target date
          </text>
        </g>

        {hasData ? (
          <>
            <polyline className="line-actual" points={series.actualPoints} />
            <polyline className={lineClass} points={series.predictionPoints} />
            <circle
              className={pointClass}
              cx={series.predictionPoint.cx}
              cy={series.predictionPoint.cy}
              r="5"
            />
          </>
        ) : (
          <g className="chart-placeholder-msg">
            <text x="415" y="108" textAnchor="middle">
              No prediction data yet
            </text>
            <text x="415" y="126" textAnchor="middle" className="chart-placeholder-sub">
              Run a prediction to see this chart
            </text>
          </g>
        )}
      </svg>
    </div>
  );
}

export default PriceChart;
