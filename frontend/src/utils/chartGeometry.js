/**
 * Map multiple numeric series onto one SVG plot.
 * viewBox plot area: x 56–860, y 24–250
 */
export function buildMultiSeries(seriesMap) {
  const values = Object.values(seriesMap).flat();
  if (!values.length) return null;

  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;
  const n = Object.values(seriesMap)[0].length;

  const xLeft = 56;
  const xRight = 860;
  const yTop = 24;
  const yBottom = 250;

  const xAt = (i) => {
    if (n <= 1) return xLeft;
    return xLeft + (i / (n - 1)) * (xRight - xLeft);
  };

  const yAt = (v) => yBottom - ((v - min) / range) * (yBottom - yTop);

  const polylines = {};
  for (const [key, arr] of Object.entries(seriesMap)) {
    polylines[key] = arr.map((v, i) => `${xAt(i).toFixed(2)},${yAt(v).toFixed(2)}`).join(' ');
  }

  return {
    polylines,
    yMinLabel: min.toFixed(2),
    yMaxLabel: max.toFixed(2),
    xMidLabel: String(Math.floor(n / 2)),
    xEndLabel: String(n - 1),
  };
}

const Y_TICK_COUNT = 4; // 5 evenly spaced labels from max down to min

/**
 * Evenly spaced Y-axis tick positions + real price values (no scientific notation).
 */
function buildYTicks(min, max, yTop, yBottom) {
  const ticks = [];
  for (let i = 0; i <= Y_TICK_COUNT; i++) {
    const frac = i / Y_TICK_COUNT;
    ticks.push({
      y: yTop + frac * (yBottom - yTop),
      value: max - frac * (max - min),
    });
  }
  return ticks;
}

/** Format a price for axis/label display without scientific notation. */
export function formatAxisValue(value) {
  const abs = Math.abs(value);
  if (abs >= 1000) return value.toFixed(0);
  if (abs >= 1) return value.toFixed(2);
  return value.toFixed(4);
}

/**
 * Build geometry for a forecast chart:
 *   - historyValues: actual prices for the historical window (e.g. 60 days)
 *   - predValues:    predicted prices for the forecast horizon (e.g. 30 days)
 *
 * The prediction line starts at the last actual point so the two lines
 * connect visually at the forecast boundary.
 *
 * SVG viewBox plot area: x 56–860, y 24–250
 */
export function buildForecastSeries(historyValues, predValues, historyDates, predDates) {
  const allValues = [...historyValues, ...predValues];
  if (!allValues.length) return null;

  const min = Math.min(...allValues);
  const max = Math.max(...allValues);
  const range = max - min || 1;

  const nHist = historyValues.length;
  const nPred = predValues.length;
  const total = nHist + nPred;

  const xLeft = 56;
  const xRight = 860;
  const yTop = 24;
  const yBottom = 250;

  const xAt = (i) => {
    if (total <= 1) return xLeft;
    return xLeft + (i / (total - 1)) * (xRight - xLeft);
  };

  const yAt = (v) => yBottom - ((v - min) / range) * (yBottom - yTop);

  const historyPolyline = historyValues
    .map((v, i) => `${xAt(i).toFixed(2)},${yAt(v).toFixed(2)}`)
    .join(' ');

  const predPoints = [
    `${xAt(nHist - 1).toFixed(2)},${yAt(historyValues[nHist - 1]).toFixed(2)}`,
    ...predValues.map((v, i) => `${xAt(nHist + i).toFixed(2)},${yAt(v).toFixed(2)}`),
  ];
  const predPolyline = predPoints.join(' ');

  const forecastX = xAt(nHist - 1);
  const endX = xAt(total - 1);

  // Horizontal reference levels: last actual (forecast start) and final predicted
  const startValue = historyValues[nHist - 1];
  const endValue = predValues[nPred - 1];
  const startY = yAt(startValue);
  const endY = yAt(endValue);

  const xLabels = {
    first: historyDates[0] ?? '0',
    boundary: historyDates[nHist - 1] ?? String(nHist - 1),
    last: predDates[predDates.length - 1] ?? String(total - 1),
  };

  return {
    historyPolyline,
    predPolyline,
    forecastX,
    endX,
    startY,
    endY,
    startValue,
    endValue,
    yTicks: buildYTicks(min, max, yTop, yBottom),
    xLabels,
  };
}

