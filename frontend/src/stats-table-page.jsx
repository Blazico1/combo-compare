import { useEffect, useMemo, useState } from 'react'

function formatValue(value) {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'number') {
    return Number(value.toFixed(4)).toString()
  }
  return String(value)
}

function SortableStatsTable({ rows, columns }) {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: null })

  const sortedRows = useMemo(() => {
    if (!sortConfig.key || !sortConfig.direction) {
      return rows
    }

    return [...rows].sort((a, b) => {
      const aVal = a[sortConfig.key]
      const bVal = b[sortConfig.key]

      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return sortConfig.direction === 'asc' ? aVal - bVal : bVal - aVal
      }

      return sortConfig.direction === 'asc'
        ? String(aVal).localeCompare(String(bVal))
        : String(bVal).localeCompare(String(aVal))
    })
  }, [rows, sortConfig])

  const handleSort = (key) => {
    setSortConfig((prev) => {
      if (prev.key !== key) {
        return { key, direction: 'asc' }
      }
      if (prev.direction === 'asc') {
        return { key, direction: 'desc' }
      }
      return { key: null, direction: null }
    })
  }

  return (
    <div className="stats-section-panel">
      <div className="stats-table-shell">
        <table className="stats-data-table">
          <thead>
            <tr>
              {columns.map((column) => {
                const isActive = sortConfig.key === column.key
                const arrow = sortConfig.direction === 'asc' ? '↑' : '↓'

                return (
                  <th
                    key={column.key}
                    className={isActive ? 'active-sort' : ''}
                    onClick={() => handleSort(column.key)}
                  >
                    <span>{column.label}</span>
                    <span className="sort-indicator">{isActive ? arrow : '↕'}</span>
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody>
            {sortedRows.map((row) => (
              <tr key={row.id}>
                {columns.map((column) => (
                  <td key={column.key}>{formatValue(row[column.key])}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function StatsTablePage({ title, endpoint, columns, currentTable }) {
  const [statsMode, setStatsMode] = useState('limitless')
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const visibleColumns = useMemo(
    () => columns.filter((column) => !column.limitlessOnly || statsMode === 'limitless'),
    [columns, statsMode]
  )

  useEffect(() => {
    let cancelled = false

    async function loadRows() {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(`${endpoint}?mode=${statsMode}`)
        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.detail || `Failed to load ${title.toLowerCase()}`)
        }

        if (!cancelled) {
          setRows(data.rows || [])
          setLoading(false)
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message)
          setLoading(false)
        }
      }
    }

    loadRows()
    return () => {
      cancelled = true
    }
  }, [endpoint, statsMode, title])

  return (
    <div className="app stats-browser">
      <header className="stats-browser-header">
        <h1>{title}</h1>
        <div className="mode-selector">
          <button
            className={statsMode === 'vanilla' ? 'active' : ''}
            onClick={() => setStatsMode('vanilla')}
          >
            Vanilla Stats
          </button>
          <button
            className={statsMode === 'limitless' ? 'active' : ''}
            onClick={() => setStatsMode('limitless')}
          >
            Limitless Stats
          </button>
        </div>
        <div className="stats-browser-links">
          <a href="/combo-compare/">To Combo-Compare</a>
          {currentTable === 'vehicles' ? (
            <a href="/combo-compare/characters">To Characters</a>
          ) : (
            <a href="/combo-compare/vehicles">To Vehicles</a>
          )}
        </div>
      </header>

      <main>
        {loading && <div className="stats-loading">Loading {title.toLowerCase()}...</div>}
        {error && <div className="stats-error">Error: {error}</div>}
        {!loading && !error && <SortableStatsTable rows={rows} columns={visibleColumns} />}
      </main>
    </div>
  )
}

export default StatsTablePage
