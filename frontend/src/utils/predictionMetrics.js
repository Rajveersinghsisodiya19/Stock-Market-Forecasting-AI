const FIELDS = ['open', 'high', 'low', 'close'];

/**
 * Per-field (Open/High/Low/Close) percentage change and direction,
 * comparing the last real Twelve Data day to the model's next-day prediction.
 *
 * predictions[0] is the single next-day forecast (horizon is always 1 day).
 */
export function computeModelMetrics(history, predictions) {
  if (!history?.length || !predictions?.length) return null;

  const lastActual = history[history.length - 1];
  const predicted = predictions[0];

  const metrics = {};
  for (const field of FIELDS) {
    const lastValue = lastActual[field];
    const predictedValue = predicted[field];
    const pct = lastValue !== 0 ? ((predictedValue - lastValue) / lastValue) * 100 : 0;

    let direction = 'No Change';
    if (predictedValue > lastValue) direction = 'Increase';
    else if (predictedValue < lastValue) direction = 'Decrease';

    metrics[field] = { value: predictedValue, lastValue, pct, direction };
  }
  return metrics;
}

export function directionArrow(direction) {
  if (direction === 'Increase') return '↑';
  if (direction === 'Decrease') return '↓';
  return '→';
}

export function directionClass(direction) {
  if (direction === 'Increase') return 'direction-up';
  if (direction === 'Decrease') return 'direction-down';
  return 'direction-flat';
}

export function formatPct(pct) {
  if (pct > 0) return `+${pct.toFixed(2)}%`;
  if (pct < 0) return `${pct.toFixed(2)}%`;
  return '0.00%';
}
