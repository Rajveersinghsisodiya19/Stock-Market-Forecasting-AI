const ALLOWED_SYMBOLS = ['INFY', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META'];

function PredictionForm({
  symbol,
  horizon,
  onSymbolChange,
  onHorizonChange,
  onSubmit,
  loading,
  error,
}) {
  return (
    <section id="predict-section" className="panel">
      <h2 className="panel-title">Run a Prediction</h2>

      <form className="input-form" onSubmit={onSubmit}>
        <div className="form-row">
          <div className="form-field">
            <label htmlFor="stock-symbol">Stock Symbol</label>
            <select
              id="stock-symbol"
              name="symbol"
              required
              value={symbol}
              onChange={(e) => onSymbolChange(e.target.value)}
              disabled={loading}
            >
              <option value="" disabled>
                Select symbol
              </option>
              {ALLOWED_SYMBOLS.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>

          <div className="form-field">
            <label htmlFor="prediction-horizon">Predict How Many Days Ahead</label>
            <select
              id="prediction-horizon"
              name="horizon_days"
              required
              value={horizon}
              onChange={(e) => onHorizonChange(e.target.value)}
              disabled={loading}
            >
              <option value="1">1 Day</option>
            </select>
          </div>

          <div className="form-field form-field-button">
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Predicting…' : 'Predict'}
            </button>
          </div>
        </div>
      </form>

      {error && <p className="form-error">{error}</p>}
    </section>
  );
}

export default PredictionForm;
