function SummaryBar({ symbol, currentPrice, horizon, targetDate }) {
  return (
    <section className="summary-bar">
      <div className="summary-item">
        <span className="summary-label">Symbol</span>
        <span className="summary-value">{symbol}</span>
      </div>
      <div className="summary-item">
        <span className="summary-label">Last Actual Open</span>
        <span className="summary-value">{currentPrice}</span>
      </div>
      <div className="summary-item">
        <span className="summary-label">Forecast Horizon</span>
        <span className="summary-value">{horizon}</span>
      </div>
      <div className="summary-item">
        <span className="summary-label">Target Date</span>
        <span className="summary-value">{targetDate}</span>
      </div>
    </section>
  );
}

export default SummaryBar;
