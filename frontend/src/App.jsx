import { useState } from 'react';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';
import SummaryBar from './components/SummaryBar';
import ModelForecastSection from './components/ModelForecastSection';
import ModelResults from './components/ModelResults';
import Comparison from './components/Comparison';
import Footer from './components/Footer';
import { computeModelMetrics } from './utils/predictionMetrics';

const initialSummary = {
  symbol: '--',
  currentPrice: '--',
  horizon: '--',
  targetDate: '--',
};

const initialModels = {
  randomForest: null,
  lstm: null,
  xgboost: null,
};

function formatMoney(value) {
  if (value == null || value === '--') return '--';
  const n = Number(value);
  if (Number.isNaN(n)) return String(value);
  return `$${n.toFixed(2)}`;
}

function App() {
  const [symbol, setSymbol]   = useState('');
  const [horizon, setHorizon] = useState('1');
  const [summary, setSummary] = useState(initialSummary);
  const [models, setModels]   = useState(initialModels);
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');

  // Forecast chart data — set after a successful /api/predict call
  const [forecastData, setForecastData] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol: symbol.toUpperCase(),
          horizon_days: Number(horizon),
        }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const detail = data.detail;
        throw new Error(
          typeof detail === 'string'
            ? detail
            : Array.isArray(detail)
              ? detail.map((d) => d.msg || JSON.stringify(d)).join('; ')
              : 'Prediction request failed'
        );
      }

      setSummary({
        symbol: data.symbol,
        currentPrice: formatMoney(data.current_price),
        horizon: `${data.horizon_days} day${data.horizon_days === 1 ? '' : 's'}`,
        targetDate: data.target_date,
      });

      setModels({
        randomForest: computeModelMetrics(data.history, data.random_forest.predictions),
        lstm: computeModelMetrics(data.history, data.lstm.predictions),
        xgboost: computeModelMetrics(data.history, data.xgboost.predictions),
      });

      // Store history + per-model predictions for the forecast charts
      setForecastData({
        history:       data.history,
        randomForest:  data.random_forest.predictions,
        lstm:          data.lstm.predictions,
        xgboost:       data.xgboost.predictions,
      });

    } catch (err) {
      setError(err.message || 'Something went wrong');
      setModels(initialModels);
      setForecastData(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Header />

      <main className="container">
        <PredictionForm
          symbol={symbol}
          horizon={horizon}
          onSymbolChange={setSymbol}
          onHorizonChange={setHorizon}
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
        />

        <SummaryBar
          symbol={summary.symbol}
          currentPrice={summary.currentPrice}
          horizon={summary.horizon}
          targetDate={summary.targetDate}
        />

        {/* Forecast charts — shown only after a prediction */}
        {forecastData && (
          <section id="charts-section" className="panel">
            <h2 className="panel-title">Forecast Charts</h2>
            <p className="section-subtitle">
              Past 60 trading days from Twelve Data (blue) plus each model's next-day forecast
              (model color). The shaded band marks the predicted trading day.
            </p>

            <div className="forecast-models">
              <ModelForecastSection
                modelName="Random Forest"
                modelKey="rf"
                colorVar="--color-rf"
                history={forecastData.history}
                predictions={forecastData.randomForest}
              />
              <ModelForecastSection
                modelName="XGBoost"
                modelKey="xgb"
                colorVar="--color-xgb"
                history={forecastData.history}
                predictions={forecastData.xgboost}
              />
              <ModelForecastSection
                modelName="LSTM"
                modelKey="lstm"
                colorVar="--color-lstm"
                history={forecastData.history}
                predictions={forecastData.lstm}
              />
            </div>
          </section>
        )}

        {!forecastData && (
          <section id="charts-section" className="panel forecast-empty-panel">
            <h2 className="panel-title">Forecast Charts</h2>
            <p className="section-subtitle forecast-empty-msg">
              Select a stock above, then click Predict to see the 60-day history and
              each model's next-day forecast charts.
            </p>
          </section>
        )}

        <ModelResults models={models} />
        <Comparison models={models} />
      </main>

      <Footer />
    </>
  );
}

export default App;
