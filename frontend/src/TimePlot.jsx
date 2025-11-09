import React, { useMemo } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from 'chart.js'
import { Line } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

// Helper to read CSS variables
const getCssVar = (name) => {
  try {
    const val = getComputedStyle(document.documentElement).getPropertyValue(name)
    return val ? val.trim() : ''
  } catch (e) {
    return ''
  }
}

// Build contiguous sign-based segment datasets with zero-cross interpolation.
// Returns an array of dataset objects suitable for Chart.js when using a linear x axis.
function buildSegmentDatasets(times, values, posColor, negColor, solid = true) {
  if (!times || !values || times.length < 2 || values.length < 2) return []

  const segments = []
  let i = 0
  while (i < values.length) {
    const v = values[i]
    let type = 'zero'
    if (v > 0) type = 'positive'
    else if (v < 0) type = 'negative'

    const start = i
    i += 1
    while (i < values.length) {
      const nv = values[i]
      if (type === 'positive' && nv <= 0) break
      if (type === 'negative' && nv >= 0) break
      if (type === 'zero' && nv !== 0) break
      i += 1
    }
    const end = i - 1
    segments.push({ type, start, end })
  }

  const datasets = []
  const linestyle = solid ? '-' : '--'
  const linewidth = solid ? 2 : 1.5

  for (let si = 0; si < segments.length; si++) {
    const seg = segments[si]
    const color = seg.type === 'positive' ? posColor : (seg.type === 'negative' ? negColor : '#FF00FF')

    const pts = []

    // If previous segment has opposite sign, interpolate a zero-cross at the start
    if (si > 0) {
      const prev = segments[si - 1]
      const prevEnd = prev.end
      const currStart = seg.start
      const pv = values[prevEnd]
      const cv = values[currStart]
      const pt = times[prevEnd]
      const ct = times[currStart]
      if ((pv > 0 && cv < 0) || (pv < 0 && cv > 0)) {
        const fraction = -pv / (cv - pv)
        const crossTime = pt + fraction * (ct - pt)
        pts.push({ x: crossTime, y: 0 })
      }
    }

    // Add the actual segment points
    for (let k = seg.start; k <= seg.end; k++) {
      pts.push({ x: times[k], y: values[k] })
    }

    // If next segment has opposite sign, interpolate a zero-cross at the end
    if (si < segments.length - 1) {
      const next = segments[si + 1]
      const currEnd = seg.end
      const nextStart = next.start
      const cv = values[currEnd]
      const nv = values[nextStart]
      const ct = times[currEnd]
      const nt = times[nextStart]
      if ((cv > 0 && nv < 0) || (cv < 0 && nv > 0)) {
        const fraction = -cv / (nv - cv)
        const crossTime = ct + fraction * (nt - ct)
        pts.push({ x: crossTime, y: 0 })
      }
    }

    if (pts.length > 0) {
      datasets.push({
        label: seg.type === 'positive' ? 'Plus' : (seg.type === 'negative' ? 'Minus' : 'Zero'),
        data: pts,
        borderColor: color,
        backgroundColor: 'transparent',
        tension: 0.2,
        pointRadius: 0,
        borderDash: solid ? [] : [6, 4],
        borderWidth: linewidth,
        spanGaps: true,
      })
    }
  }

  return datasets
}

export default function TimePlot({ simulationResult, differential }) {
  // simulationResult expected shape: { combo1: { times, speeds, distances }, combo2: {...} }
  const chartGridColor = getCssVar('--grid') || '#444'
  const combo1Color = getCssVar('--accent-2') || '#2244FF'
    const combo2Color = getCssVar('--accent-3') || '#FF2222'

  const dataNormal = useMemo(() => {
    // Return null only when there's no data for either combo.
    if (!simulationResult || (!simulationResult.combo1 && !simulationResult.combo2)) return null
    const t1 = simulationResult.combo1?.times || []
    const s1 = simulationResult.combo1?.speeds || []
    const d1 = simulationResult.combo1?.distances || []
    const t2 = simulationResult.combo2?.times || []
    const s2 = simulationResult.combo2?.speeds || []
    const d2 = simulationResult.combo2?.distances || []

    return {
      labels: t1.length >= t2.length ? t1 : t2,
      datasets: [
        {
          label: 'Speed Combo 1',
          data: s1,
          borderColor: combo1Color,
          backgroundColor: 'transparent',
          yAxisID: 'y',
          tension: 0.2,
          pointRadius: 0,
          pointHoverRadius: 0,
        },
        {
          label: 'Speed Combo 2',
          data: s2,
          borderColor: combo2Color,
          backgroundColor: 'transparent',
          yAxisID: 'y',
          tension: 0.2,
          pointRadius: 0,
          pointHoverRadius: 0,
        },
        {
          label: 'Distance Combo 1',
          data: d1,
          borderColor: combo1Color,
          borderDash: [6, 4],
          backgroundColor: 'transparent',
          yAxisID: 'y1',
          tension: 0.2,
          pointRadius: 0,
          pointHoverRadius: 0,
        },
        {
          label: 'Distance Combo 2',
          data: d2,
          borderColor: combo2Color,
          borderDash: [6, 4],
          backgroundColor: 'transparent',
          yAxisID: 'y1',
          tension: 0.2,
          pointRadius: 0,
          pointHoverRadius: 0,
        },
      ],
    }
  }, [simulationResult, combo1Color, combo2Color])

  const dataDiff = useMemo(() => {
    // Differential mode requires both combos present.
    if (!simulationResult || !simulationResult.combo1 || !simulationResult.combo2) return null
    const t = simulationResult.combo1.times || []
    const s1 = simulationResult.combo1.speeds || []
    const s2 = simulationResult.combo2?.speeds || []
    const d1 = simulationResult.combo1.distances || []
    const d2 = simulationResult.combo2?.distances || []

    // make arrays same length
    const minLen = Math.min(t.length, s1.length, s2.length, d1.length, d2.length)
    const times = t.slice(0, minLen)
    const speedDiff = s1.slice(0, minLen).map((v, i) => v - s2[i])
    const distDiff = d1.slice(0, minLen).map((v, i) => v - d2[i])

    // Build segment datasets with zero-cross interpolation so colored
    // segments meet exactly at zero. Use {x,y} points so we can insert
    // interpolated times between samples.
    const speedDatasets = buildSegmentDatasets(times, speedDiff, combo1Color, combo2Color, true)
    const distDatasets = buildSegmentDatasets(times, distDiff, combo1Color, combo2Color, false)

    return {
      labels: times,
      speedDatasets,
      distDatasets,
    }
  }, [simulationResult, combo1Color, combo2Color])

  // If there's no data at all, render a gentle empty-overlay with instructions.
  const hasAnyData = simulationResult && (simulationResult.combo1 || simulationResult.combo2)
  if (!hasAnyData) {
    const muted = getCssVar('--muted') || '#888'
    const height = differential ? 460 : 420
    return (
      <div style={{ height, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ color: muted, fontStyle: 'italic', textAlign: 'center', padding: 12 }}>
          Select at least one vehicle/character combo to run the simulation.
        </div>
      </div>
    )
  }

  const commonOptions = {
    responsive: true,
    maintainAspectRatio: false,
    elements: { point: { radius: 0 } },
    scales: {
      x: {
        title: { display: true, text: 'Time (s)' },
        grid: { color: chartGridColor },
      },
    },
    plugins: { legend: { display: false } },
  }

  // Helper to format tick values: integers as 'N', halves as 'N.5', otherwise empty.
  const formatTick = (raw) => {
    const v = Number(raw)
    if (Number.isNaN(v)) return ''
    // Round to the nearest 0.5 to avoid tiny fp noise
    const twoTimes = Math.round(v * 2)
    // If the value was close to a half-integer, show it.
    if (Math.abs(v * 2 - twoTimes) < 1e-6) {
      // If whole integer, show without decimal
      if (twoTimes % 2 === 0) return String(twoTimes / 2)
      return (twoTimes / 2).toFixed(1).replace(/\.0$/, '')
    }
    return ''
  }

  // Choose labels depending on mode so we can compute x min/max for tick generation.
  // Snap min/max to nearest 0.5 boundaries so ticks like 9.0/10.0 appear even if data ends
  // at a fractional frame time (e.g., 9.9833).
  const labels = differential ? dataDiff?.labels : dataNormal?.labels
  let xMin = labels && labels.length ? Number(labels[0]) : undefined
  let xMax = labels && labels.length ? Number(labels[labels.length - 1]) : undefined
  if (typeof xMin === 'number' && !Number.isNaN(xMin)) xMin = Math.floor(xMin * 2) / 2
  if (typeof xMax === 'number' && !Number.isNaN(xMax)) xMax = Math.ceil(xMax * 2) / 2

  if (!differential) {
    // Compute how many ticks we'd like at 0.5 spacing, cap to a reasonable number.
    const desiredTicks = (typeof xMin === 'number' && typeof xMax === 'number') ? Math.floor((xMax - xMin) / 0.5) + 1 : 12
    const maxTicks = Math.min(Math.max(desiredTicks, 6), 25)

    const xScale = {
      ...commonOptions.scales.x,
      type: 'linear',
      min: xMin,
      max: xMax,
      ticks: {
        stepSize: 0.5,
        maxTicksLimit: maxTicks,
        callback: function (value) {
          // Use scale helper where available to get the real numeric label
          let raw = value
          try {
            if (this && typeof this.getLabelForValue === 'function') raw = this.getLabelForValue(value)
          } catch (e) {
            raw = value
          }
          return formatTick(raw)
        },
      },
    }

    return (
      <div style={{ height: 420 }}>
        <Line
          data={dataNormal}
          options={{
            ...commonOptions,
            scales: {
              x: xScale,
              y: { type: 'linear', position: 'left', title: { display: true, text: 'Speed (km/h)' }, grid: { color: chartGridColor } },
              y1: { type: 'linear', position: 'right', title: { display: true, text: 'Distance (m)' }, grid: { drawOnChartArea: false }, ticks: { display: true } },
            },
          }}
        />
      </div>
    )
  }

  // differential: render two stacked small charts
  const desiredTicksDiff = (typeof xMin === 'number' && typeof xMax === 'number') ? Math.floor((xMax - xMin) / 0.5) + 1 : 8
  const maxTicksDiff = Math.min(Math.max(desiredTicksDiff, 4), 16)
  const xScaleDiff = {
    ...commonOptions.scales.x,
    type: 'linear',
    min: xMin,
    max: xMax,
    ticks: {
      stepSize: 0.5,
      maxTicksLimit: maxTicksDiff,
      callback: function (value) {
        let raw = value
        try {
          if (this && typeof this.getLabelForValue === 'function') raw = this.getLabelForValue(value)
        } catch (e) {
          raw = value
        }
        return formatTick(raw)
      },
    },
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      <div style={{ height: 220 }}>
        <Line data={{ labels: dataDiff.labels, datasets: dataDiff.speedDatasets }} options={{ ...commonOptions, scales: { x: xScaleDiff, y: { title: { display: true, text: 'Speed Difference (km/h)' }, grid: { color: chartGridColor } } } }} />
      </div>
      <div style={{ height: 220 }}>
        <Line data={{ labels: dataDiff.labels, datasets: dataDiff.distDatasets }} options={{ ...commonOptions, scales: { x: xScaleDiff, y: { title: { display: true, text: 'Distance Difference (m)' }, grid: { color: chartGridColor } } } }} />
      </div>
    </div>
  )
}
