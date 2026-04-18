import { useState, useEffect, Fragment, useMemo, useCallback } from 'react'
import './App.css'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js'
import { Radar } from 'react-chartjs-2'
import TimePlot from './TimePlot'

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

// Inline SVG icon components so colour can follow CSS variables (currentColor)
function SunIcon({ className, style }) {
  return (
    <svg className={className} style={style} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle cx="12" cy="12" r="5" stroke="currentColor" strokeWidth="1.5" />
      <path d="M12 2V4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M12 20V22" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M4 12L2 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M22 12L20 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M19.7778 4.22266L17.5558 6.25424" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M4.22217 4.22266L6.44418 6.25424" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M6.44434 17.5557L4.22211 19.7779" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      <path d="M19.7778 19.7773L17.5558 17.5551" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  )
}

function MoonIcon({ className, style }) {
  return (
    <svg className={className} style={style} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path fillRule="evenodd" clipRule="evenodd" d="M11.0174 2.80157C6.37072 3.29221 2.75 7.22328 2.75 12C2.75 17.1086 6.89137 21.25 12 21.25C16.7767 21.25 20.7078 17.6293 21.1984 12.9826C19.8717 14.6669 17.8126 15.75 15.5 15.75C11.4959 15.75 8.25 12.5041 8.25 8.5C8.25 6.18738 9.33315 4.1283 11.0174 2.80157ZM1.25 12C1.25 6.06294 6.06294 1.25 12 1.25C12.7166 1.25 13.0754 1.82126 13.1368 2.27627C13.196 2.71398 13.0342 3.27065 12.531 3.57467C10.8627 4.5828 9.75 6.41182 9.75 8.5C9.75 11.6756 12.3244 14.25 15.5 14.25C17.5882 14.25 19.4172 13.1373 20.4253 11.469C20.7293 10.9658 21.286 10.804 21.7237 10.8632C22.1787 10.9246 22.75 11.2834 22.75 12C22.75 17.9371 17.9371 22.75 12 22.75C6.06294 22.75 1.25 17.9371 1.25 12Z" fill="currentColor" />
    </svg>
  )
}

function App() {
  const [activeTab, setActiveTab] = useState('basic')
  const [statsMode, setStatsMode] = useState('vanilla')
  const [vehicles, setVehicles] = useState([])
  const [characters, setCharacters] = useState([])
  const [selectedVehicle1, setSelectedVehicle1] = useState('')
  const [selectedCharacter1, setSelectedCharacter1] = useState('')
  const [selectedVehicle2, setSelectedVehicle2] = useState('')
  const [selectedCharacter2, setSelectedCharacter2] = useState('')
  const [basicStats1, setBasicStats1] = useState(null)
  const [basicStats2, setBasicStats2] = useState(null)
  const [advancedStats1, setAdvancedStats1] = useState(null)
  const [advancedStats2, setAdvancedStats2] = useState(null)
  const [simulationType, setSimulationType] = useState('acceleration')
  const [differentialMode, setDifferentialMode] = useState(false)
  const [simulationTime, setSimulationTime] = useState(10)
  const [wheelie1, setWheelie1] = useState(false)
  const [wheelie2, setWheelie2] = useState(false)
  const [smt1, setSmt1] = useState(false)
  const [smt2, setSmt2] = useState(false)
  const [ssmt1, setSsmt1] = useState(false)
  const [ssmt2, setSsmt2] = useState(false)
  const [simulationResult, setSimulationResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [speedUnit, setSpeedUnit] = useState('akm/h')
  const [theme, setTheme] = useState('dark')
  const [isPortraitMobile, setIsPortraitMobile] = useState(false)

  useEffect(() => {
    const mediaQuery = window.matchMedia('(max-width: 768px) and (orientation: portrait)')
    const updateIsPortraitMobile = (event) => {
      setIsPortraitMobile(event.matches)
    }

    setIsPortraitMobile(mediaQuery.matches)

    if (typeof mediaQuery.addEventListener === 'function') {
      mediaQuery.addEventListener('change', updateIsPortraitMobile)
      return () => mediaQuery.removeEventListener('change', updateIsPortraitMobile)
    }

    mediaQuery.addListener(updateIsPortraitMobile)
    return () => mediaQuery.removeListener(updateIsPortraitMobile)
  }, [])

  const toggleTheme = () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark'
    try {
      document.documentElement.setAttribute('data-theme', newTheme)
    } catch (err) {
      console.error('toggleTheme error', err)
    }
    setTheme(newTheme)
  }

  // Read CSS variables (if available) so chart dataset colours follow the theme variables.
  const getCssVar = (name) => {
    try {
      // Read from :root (documentElement) where variables are centralized
      const el = document.documentElement
      const val = getComputedStyle(el).getPropertyValue(name)
      return val ? val.trim() : ''
    } catch (err) {
      console.error('getCssVar error for', name, err)
      return ''
    }
  }

  const chartTextColor = getCssVar('--chart-text')
  const chartGridColor = getCssVar('--grid')

  const combo1BorderColor = getCssVar('--accent-2')
  const combo2BorderColor = getCssVar('--accent-3')

  // Collapsible sections state: default all closed except core
  const [openSections, setOpenSections] = useState({
    classification: false,
    core: true,
    acceleration: false,
    speed: false,
    rotation: false,
    misc: false,
  })

  // Load initial data
  // Load initial data (moved below so callbacks exist before use)

  // Update stats when selections change (moved below after callbacks are defined)

  const loadVehicles = useCallback(async () => {
    try {
      const response = await fetch(`/api/vehicles?mode=${statsMode}`)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to load vehicles')
      }

      setVehicles(Array.isArray(data.vehicles) ? data.vehicles : [])
    } catch (err) {
      console.error('loadVehicles failed', err)
      setVehicles([])
    }
  }, [statsMode])

  const loadCharacters = useCallback(async () => {
    try {
      const response = await fetch(`/api/characters?mode=${statsMode}`)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to load characters')
      }

      setCharacters(Array.isArray(data.characters) ? data.characters : [])
    } catch (err) {
      console.error('loadCharacters failed', err)
      setCharacters([])
    }
  }, [statsMode])

  const changeStatsMode = (mode) => {
    // If the user clicked the currently-active mode, do nothing.
    // This prevents accidentally clearing the loaded stats when the button is clicked repeatedly.
    if (mode === statsMode) return

    setStatsMode(mode)
    setBasicStats1(null)
    setBasicStats2(null)
    setAdvancedStats1(null)
    setAdvancedStats2(null)
    loadVehicles()
    loadCharacters()
  }

  const loadBasicStats = useCallback(async (comboNum) => {
    const vehicle = comboNum === 1 ? selectedVehicle1 : selectedVehicle2
    const character = comboNum === 1 ? selectedCharacter1 : selectedCharacter2

    if (!vehicle && !character) return

    try {
      let url = ''
      if (vehicle && character) {
        url = `/api/basic-stats/${vehicle}/${character}?mode=${statsMode}`
      } else if (vehicle) {
        url = `/api/basic-stats/vehicle/${vehicle}?mode=${statsMode}`
      } else {
        url = `/api/basic-stats/character/${character}?mode=${statsMode}`
      }

      const response = await fetch(url)
      const data = await response.json()
      // backend returns { stats: {...} }
      const statsObj = data && data.stats ? data.stats : data
      if (comboNum === 1) {
        setBasicStats1(statsObj)
      } else {
        setBasicStats2(statsObj)
      }
    } catch (err) {
      console.error('loadBasicStats failed', err)
    }
  }, [selectedVehicle1, selectedVehicle2, selectedCharacter1, selectedCharacter2, statsMode])

  const loadAdvancedStats = useCallback(async (comboNum) => {
    const vehicle = comboNum === 1 ? selectedVehicle1 : selectedVehicle2
    const character = comboNum === 1 ? selectedCharacter1 : selectedCharacter2

    if (!vehicle && !character) return

    try {
      let url = ''
      if (vehicle && character) {
        url = `/api/advanced-stats/${vehicle}/${character}?mode=${statsMode}`
      } else if (vehicle) {
        url = `/api/advanced-stats/vehicle/${vehicle}?mode=${statsMode}`
      } else {
        url = `/api/advanced-stats/character/${character}?mode=${statsMode}`
      }

      const response = await fetch(url)
      const data = await response.json()
      const statsObj = data && data.stats ? data.stats : data
      if (comboNum === 1) {
        setAdvancedStats1(statsObj)
      } else {
        setAdvancedStats2(statsObj)
      }
    } catch (err) {
      console.error('loadAdvancedStats failed', err)
    }
  }, [selectedVehicle1, selectedVehicle2, selectedCharacter1, selectedCharacter2, statsMode])

  const runSimulation = useCallback(async () => {
    // Require at least one fully-selected combo (vehicle + character)
    const combo1Ready = selectedVehicle1 && selectedCharacter1
    const combo2Ready = selectedVehicle2 && selectedCharacter2
    if (!combo1Ready && !combo2Ready) {
      // nothing to simulate
      return
    }

    setLoading(true)
    try {
      // Build combo payload expected by the backend: { combo1: {...}, combo2: {...}, sim_type: 'accel'|'mini_turbo' }
      const simTypeMap = {
        'acceleration': 'accel',
        'mini-turbo': 'mini_turbo'
      }

      const payload = {
        sim_type: simTypeMap[simulationType] || 'accel',
        differential: differentialMode,
        time: simulationTime,
        mode: statsMode,
      }

      if (combo1Ready) {
        payload.combo1 = {
          vehicle_id: parseInt(selectedVehicle1, 10),
          character_id: parseInt(selectedCharacter1, 10),
          wheelie: wheelie1,
          ssmt: ssmt1,
          smt: smt1,
        }
      }

      if (combo2Ready) {
        payload.combo2 = {
          vehicle_id: parseInt(selectedVehicle2, 10),
          character_id: parseInt(selectedCharacter2, 10),
          wheelie: wheelie2,
          ssmt: ssmt2,
          smt: smt2,
        }
      }

      // Client-side validation: ensure provided ids exist in the loaded lists for the selected mode
      const findVehicle = (id) => vehicles.find(v => String(v.id) === String(id))
      const findCharacter = (id) => characters.find(c => String(c.id) === String(id))
      if (payload.combo1) {
        if (!findVehicle(payload.combo1.vehicle_id) || !findCharacter(payload.combo1.character_id)) {
          alert('Combo 1 vehicle or character not found for current stats mode. Check your selections or switch mode to Vanilla/Limitless.')
          setLoading(false)
          return
        }
      }
      if (payload.combo2) {
        if (!findVehicle(payload.combo2.vehicle_id) || !findCharacter(payload.combo2.character_id)) {
          alert('Combo 2 vehicle or character not found for current stats mode. Check your selections or switch mode to Vanilla/Limitless.')
          setLoading(false)
          return
        }
      }

      const response = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })

      if (!response.ok) {
        const txt = await response.text()
        throw new Error(`Simulation failed: ${response.status} ${txt}`)
      }

      const data = await response.json()
      setSimulationResult(data)
    } catch (err) {
      console.error('runSimulation error', err)
      alert('Simulation error: ' + (err.message || err))
    } finally {
      setLoading(false)
    }
  }, [
    selectedVehicle1,
    selectedCharacter1,
    selectedVehicle2,
    selectedCharacter2,
    differentialMode,
    simulationTime,
    statsMode,
    vehicles,
    characters,
    wheelie1,
    wheelie2,
    smt1,
    smt2,
    ssmt1,
    ssmt2,
    simulationType,
  ])

  // Load initial data
  useEffect(() => {
    loadVehicles()
    loadCharacters()
  }, [statsMode, loadVehicles, loadCharacters])

  // Update stats when selections change
  useEffect(() => {
    if (selectedVehicle1 || selectedCharacter1) {
      loadBasicStats(1)
      loadAdvancedStats(1)
    } else {
      // Clear if nothing is selected
      setBasicStats1(null)
      setAdvancedStats1(null)
    }
  }, [selectedVehicle1, selectedCharacter1, statsMode, loadBasicStats, loadAdvancedStats])

  useEffect(() => {
    if (selectedVehicle2 || selectedCharacter2) {
      loadBasicStats(2)
      loadAdvancedStats(2)
    } else {
      setBasicStats2(null)
      setAdvancedStats2(null)
    }
  }, [selectedVehicle2, selectedCharacter2, statsMode, loadBasicStats, loadAdvancedStats])

  // Auto-run simulation when either combo selection changes (user requested)
  useEffect(() => {
    const combo1Ready = selectedVehicle1 && selectedCharacter1
    const combo2Ready = selectedVehicle2 && selectedCharacter2
    if (combo1Ready || combo2Ready) {
      // Debounce briefly to avoid rapid duplicate calls when user changes multiple selects
      const id = setTimeout(() => runSimulation(), 120)
      return () => clearTimeout(id)
    }
    // if neither combo is ready, clear previous result
    setSimulationResult(null)
  }, [
    selectedVehicle1,
    selectedCharacter1,
    selectedVehicle2,
    selectedCharacter2,
    simulationType,
    differentialMode,
    simulationTime,
    wheelie1,
    wheelie2,
    smt1,
    smt2,
    ssmt1,
    ssmt2,
    statsMode,
    runSimulation,
  ])

  // Keep UI checkbox state consistent with selection and simulation type.
  // Clearing disabled options must happen inside an effect (not during render).
  useEffect(() => {
    const combo1Ready = selectedVehicle1 && selectedCharacter1
    const combo2Ready = selectedVehicle2 && selectedCharacter2
    const smtEnabled = simulationType === 'mini-turbo'
    const ssmtEnabled = simulationType === 'acceleration'

    if (!combo1Ready) {
      if (wheelie1) setWheelie1(false)
      if (smt1) setSmt1(false)
      if (ssmt1) setSsmt1(false)
    } else {
      if (!smtEnabled && smt1) setSmt1(false)
      if (!ssmtEnabled && ssmt1) setSsmt1(false)
    }

    if (!combo2Ready) {
      if (wheelie2) setWheelie2(false)
      if (smt2) setSmt2(false)
      if (ssmt2) setSsmt2(false)
    } else {
      if (!smtEnabled && smt2) setSmt2(false)
      if (!ssmtEnabled && ssmt2) setSsmt2(false)
    }
  }, [
    selectedVehicle1,
    selectedCharacter1,
    selectedVehicle2,
    selectedCharacter2,
    simulationType,
    differentialMode,
    wheelie1,
    wheelie2,
    smt1,
    smt2,
    ssmt1,
    ssmt2,
  ])

  const getRadarData = useCallback(() => {
  const labels = ['Speed', 'Mini Turbo', 'Weight', 'Handling', 'Offroad', 'Acceleration', 'Drift']
  const keys = ['speed', 'mini_turbo', 'weight', 'handling', 'offroad', 'acceleration', 'drift']
    const datasets = []
    // Always include Combo 1 dataset
    const data1 = basicStats1 ? keys.map(key => basicStats1[key] || 0) : [0, 0, 0, 0, 0, 0, 0]
    datasets.push({
      label: 'Combo 1',
      data: data1,
      backgroundColor: getCssVar('--combo1-bg'),
      borderColor: combo1BorderColor,
      borderWidth: 2,
      pointRadius: 0,
    })
    // Always include Combo 2 dataset
    const data2 = basicStats2 ? keys.map(key => basicStats2[key] || 0) : [0, 0, 0, 0, 0, 0, 0]
    datasets.push({
      label: 'Combo 2',
      data: data2,
      backgroundColor: getCssVar('--combo2-bg'),
      borderColor: combo2BorderColor,
      borderWidth: 2,
      pointRadius: 0,
    })
    return {
      labels,
      datasets,
    }
  }, [basicStats1, basicStats2, combo1BorderColor, combo2BorderColor])

  const radarData = useMemo(() => getRadarData(), [getRadarData])

  const renderBasicStats = () => (
    <div className="basic-stats-layout">
      <div className="chart-column" style={{ width: '100%', padding: 0, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div className="basic-stats-legend">
          {/* Combo 1 */}
          <div className="basic-stats-legend-row">
            <div className="basic-stats-swatch combo1-swatch" />
            <span className="basic-stats-legend-text">
              {vehicles.find(v => String(v.id) === selectedVehicle1)?.name || '-'} +{' '}
              {characters.find(c => String(c.id) === selectedCharacter1)?.name || '-'}
            </span>
          </div>
          {/* Combo 2 */}
          <div className="basic-stats-legend-row">
            <div className="basic-stats-swatch combo2-swatch" />
            <span className="basic-stats-legend-text">
              {vehicles.find(v => String(v.id) === selectedVehicle2)?.name || '-'} +{' '}
              {characters.find(c => String(c.id) === selectedCharacter2)?.name || '-'}
            </span>
          </div>
        </div>
        <div className="radar-container">
          <div className="radar-chart">
            <Radar key={theme} data={radarData} options={{
              responsive: true,
              maintainAspectRatio: false,
              layout: {
                padding: isPortraitMobile
                  ? { left: 2, right: 2, top: 2, bottom: 2 }
                  : { left: 40, right: 40, top: 20, bottom: 20 }
              },
                scales: {
                  r: {
                    min: -0.1,
                    max: 1.1,
                    ticks: { display: false },
                    grid: { color: chartGridColor },
                    angleLines: { color: chartGridColor },
                    pointLabels: {
                      color: chartTextColor,
                      font: { size: isPortraitMobile ? 6 : 12 },
                    },
                  },
                },
              plugins: { legend: { display: false } },
              elements: { point: { radius: 0 } },
            }} />
          </div>
        </div>
      </div>
    </div>
  )

  // Helper to format values
  const formatValue = (value, key) => {
    if (value === null || value === undefined) return '-'

    // Special parsing for 3 specific stats
    if (key === 'weight_class') {
      const wcMap = { 0: 'Light', 1: 'Medium', 2: 'Heavy' }
      return wcMap[value] || String(value)
    }
    if (key === 'num_tires') {
      const tiresMap = {
        0: '4 Tires', 1: '2 Tires (Handle Rel)',
        2: '2 Tires (Vehicle Rel)', 3: '3 Tires'
      }
      return tiresMap[value] || String(value)
    }
    if (key === 'drift_type') {
      const driftMap = { 0: 'Outside (Kart)', 1: 'Outside (Bike)', 2: 'Inside' }
      return driftMap[value] || String(value)
    }

    const formatNumber = (n) => {
      if (n === null || n === undefined) return '-'
      if (Number.isInteger(n)) return String(n)
      const p = Number(n).toPrecision(5)
      if (p.includes('e') || p.includes('E')) return p
      let s = p.replace(/(\.\d*?[1-9])0+$/, '$1')
      s = s.replace(/\.0+$/, '')
      return s
    }

    if (Array.isArray(value)) {
      return '[' + value.map(v => typeof v === 'number' ? formatNumber(v) : String(v)).join(', ') + ']'
    }
    if (typeof value === 'number') {
      return formatNumber(value)
    }
    return String(value)
  }

  // Helper to extract values for expanded multiplier keys like 'speed_multipliers_0'
  const getStatValue = (statsObj, key) => {
    if (!statsObj) return undefined
    if (!key) return undefined
    const speedPrefix = 'speed_multipliers_'
    const rotPrefix = 'rotation_multipliers_'
    if (key.startsWith(speedPrefix) || key.startsWith(rotPrefix)) {
      const parts = key.split('_')
      const idx = parseInt(parts[parts.length - 1], 10)
      const base = parts.slice(0, parts.length - 1).join('_') // 'speed_multipliers' or 'rotation_multipliers'
      const arr = statsObj[base]
      if (Array.isArray(arr) && Number.isInteger(idx) && idx >= 0 && idx < arr.length) {
        return arr[idx]
      }
      return undefined
    }
    return statsObj[key]
  }

  // Render simulation sidebar stats based on type
  const renderSimSidebarStats = (adv) => {
    if (!adv) return null

    if (simulationType === 'acceleration') {
      const speedVal = adv.speed
      const As = [adv.std_accel_a0, adv.std_accel_a1, adv.std_accel_a2, adv.std_accel_a3]
      const Ts = [adv.std_accel_t1, adv.std_accel_t2, adv.std_accel_t3]

      return (
        <div>
          <div className="sim-stat-line">Speed: {formatValue(speedVal)}</div>
          <div className="sim-stat-line">A0: {formatValue(As[0])}</div>
          <div className="sim-stat-line">A1: {formatValue(As[1])}</div>
          <div className="sim-stat-line">A2: {formatValue(As[2])}</div>
          <div className="sim-stat-line">A3: {formatValue(As[3])}</div>
          <div className="sim-stat-line">T1: {formatValue(Ts[0])}</div>
          <div className="sim-stat-line">T2: {formatValue(Ts[1])}</div>
          <div className="sim-stat-line">T3: {formatValue(Ts[2])}</div>
        </div>
      )
    }

    // Mini-turbo: show speed and mini-turbo duration
    const speedVal = adv.speed
    const mt = adv.mini_turbo_duration
    return (
      <div>
        <div className="sim-stat-line">Speed: {formatValue(speedVal)}</div>
        <div className="sim-stat-line">Mini Turbo: {mt != null ? String(Math.round(mt)) : '-'}</div>
      </div>
    )
  }

  // Toggle section open/closed
  const toggleSection = (id) => {
    setOpenSections(prev => ({ ...prev, [id]: !prev[id] }))
  }

  const renderAdvancedStats = () => {
    // Multiplier labels for indices 0x00..0x1F
    const multiplierLabels = [
      'Road (0x00)', // 0
      'Slippery Road 1 (0x01)',
      'Weak Off-road (0x02)',
      'Off-road (0x03)',
      'Heavy Off-road (0x04)',
      'Slippery Road 2 (0x05)',
      'Boost [DASH] (0x06)',
      'Boost Ramp [DASHJ] (0x07)',
      'Jump Pad (0x08)',
      'Item Road (0x09)',
      'Solid Fall (0x0A)',
      'Moving Water (0x0B)',
      'Wall (0x0C)',
      'Invisible Wall (0x0D)',
      'Item Wall (0x0E)',
      'Wall 2 (0x0F)',
      'Fall Boundary (0x10)',
      'Cannon Trigger (0x11)',
      'Force Recalculation (0x12)',
      'Half-Pipe Ramp (0x13)',
      'Player-Only Wall (0x14)',
      'Moving Road (0x15)',
      'Sticky Road [ATTACH] (0x16)',
      'Road 2 (0x17)',
      'Sound Trigger (0x18)',
      'Weak Wall (0x19)',
      'Effect Trigger (0x1A)',
      'Item State Modifier (0x1B)',
      'Half-Pipe Invisible Wall (0x1C)',
      'Rotating Road (0x1D)',
      'Special Wall (0x1E)',
      'Invisible Wall 2 (0x1F)',
    ];

    const classificationItems = [
      { display: "Number of Tires", key: "num_tires" },
      { display: "Drift Type", key: "drift_type" },
      { display: "Weight Class", key: "weight_class" },
    ];

    const coreItems = [
      { display: "Weight", key: "weight" },
      { display: "Speed", key: "speed" },
      { display: "Speed in Turn", key: "speed_in_turn" },
      { display: "Manual Handling", key: "manual_handling" },
      { display: "Auto Handling", key: "auto_handling" },
      { display: "Handling Reactivity", key: "handling_reactivity" },
      { display: "Manual Drift", key: "manual_drift" },
      { display: "Auto Drift", key: "auto_drift" },
      { display: "Drift Reactivity", key: "drift_reactivity" },
      { display: "Outside Drift Angle", key: "outside_drift_angle" },
      { display: "Outside Drift Decrement", key: "outside_drift_decrement" },
      { display: "Mini Turbo Duration", key: "mini_turbo_duration" },
      ...(statsMode === 'limitless' ? [
        { display: "MT Charge Time", key: "speed_multipliers_12" },
        { display: "SMT Charge Time", key: "speed_multipliers_13" },
      ] : []),
    ];

    const accelItems = [
      { display: "Std Accel A0", key: "std_accel_a0" },
      { display: "Std Accel A1", key: "std_accel_a1" },
      { display: "Std Accel A2", key: "std_accel_a2" },
      { display: "Std Accel A3", key: "std_accel_a3" },
      { display: "Std Accel T1", key: "std_accel_t1" },
      { display: "Std Accel T2", key: "std_accel_t2" },
      { display: "Std Accel T3", key: "std_accel_t3" },
      { display: "Drift Accel A0", key: "drift_accel_a0" },
      { display: "Drift Accel A1", key: "drift_accel_a1" },
      { display: "Drift Accel T1", key: "drift_accel_t1" },
    ];

    const speedItems = multiplierLabels.map((label, i) => ({ display: `Speed - ${label}`, key: `speed_multipliers_${i}` }));
    const rotationItems = multiplierLabels.map((label, i) => ({ display: `Rotation - ${label}`, key: `rotation_multipliers_${i}` }));

    const miscItems = [
      { display: "Bump Deviation", key: "bump_deviation" },
      { display: "Tilt", key: "tilt" },
      { display: "Rotating Items Z Radius", key: "rotating_items_z_radius" },
      { display: "Rotating Items X Radius", key: "rotating_items_x_radius" },
      { display: "Rotating Items Y Distance", key: "rotating_items_y_distance" },
      { display: "Rotating Items Z Distance", key: "rotating_items_z_distance" },
      { display: "Max Normal Accel", key: "max_normal_accel" },
      { display: "Mega Mushroom Scale", key: "mega_mushroom_scale" },
      { display: "Shock Scale", key: "shock_scale" },
    ];

    // Order: core first (open by default), then acceleration, speed, rotation,
    // classification (moved down), and misc last.
    const sections = [
      { id: 'core', title: 'Core Stats', items: coreItems },
      { id: 'acceleration', title: 'Acceleration', items: accelItems },
      { id: 'speed', title: 'Speed Multipliers', items: speedItems },
      { id: 'rotation', title: 'Rotation Multipliers', items: rotationItems },
      { id: 'classification', title: 'Classification', items: classificationItems },
      { id: 'misc', title: 'Misc', items: miscItems },
    ];

    return (
      <div className="advanced-stats-container">
        <div className="advanced-stats-scroll">
          <table className="advanced-stats-table" style={{ tableLayout: 'fixed', width: '100%' }}>
            <colgroup>
              <col style={{ width: '33.33%' }} />
              <col style={{ width: '33.33%' }} />
              <col style={{ width: '33.33%' }} />
            </colgroup>
            <thead>
              <tr>
                <th className="combo1-header">Combo 1</th>
                <th className="stat-name-header">Stat</th>
                <th className="combo2-header">Combo 2</th>
              </tr>
            </thead>
            <tbody>
              {sections.map(section => (
                <Fragment key={section.id}>
                  <tr className="section-header" onClick={() => toggleSection(section.id)} style={{ cursor: 'pointer' }}>
                    <td colSpan={3} className="section-title">
                      <strong>{openSections[section.id] ? '▾' : '▸'} {section.title}</strong>
                    </td>
                  </tr>

                  {openSections[section.id] && section.items.map(stat => (
                    <tr key={stat.key}>
                      <td className="value-cell combo1-value">{formatValue(getStatValue(advancedStats1, stat.key), stat.key)}</td>
                      <td className="stat-name-cell">{stat.display}</td>
                      <td className="value-cell combo2-value">{formatValue(getStatValue(advancedStats2, stat.key), stat.key)}</td>
                    </tr>
                  ))}

                </Fragment>
              ))}

            </tbody>
          </table>
        </div>
      </div>
    )
  }

  const renderSimulation = () => (
    <div className="simulation-grid">
      {/* determine if each combo has both vehicle+character selected */}
      {null}
      <div className="sim-panel combo1-panel">
        <h4>Combo 1</h4>
        {/* Selected combo display: show vehicle + character names centered */}
        <div className="combo-display">
          {(() => {
            const v = vehicles.find(vv => String(vv.id) === String(selectedVehicle1))
            const c = characters.find(cc => String(cc.id) === String(selectedCharacter1))
            if (!v && !c) return (
              <div className="combo-display-lines">
                <div className="combo-vehicle"><strong>-</strong></div>
                <div className="combo-character"><strong>-</strong></div>
              </div>
            )
            return (
              <div className="combo-display-lines">
                <div className="combo-vehicle">{v ? v.name : '-'}</div>
                <div className="combo-character">{c ? c.name : '-'}</div>
              </div>
            )
          })()}
        </div>
        <div className="sim-panel-controls">
          {(() => {
            const combo1Ready = selectedVehicle1 && selectedCharacter1
            const smtEnabled = simulationType === 'mini-turbo'
            const ssmtEnabled = simulationType === 'acceleration'

            return (
              <>
                <label className={combo1Ready ? '' : 'disabled-option'}>
                  <input type="checkbox" disabled={!combo1Ready} checked={wheelie1} onChange={(e) => setWheelie1(e.target.checked)} /> Wheelie
                </label>
                <label className={combo1Ready && smtEnabled ? '' : 'disabled-option'}>
                  <input type="checkbox" disabled={!(combo1Ready && smtEnabled)} checked={smt1} onChange={(e) => setSmt1(e.target.checked)} /> SMT
                </label>
                <label className={combo1Ready && ssmtEnabled ? '' : 'disabled-option'}>
                  <input type="checkbox" disabled={!(combo1Ready && ssmtEnabled)} checked={ssmt1} onChange={(e) => setSsmt1(e.target.checked)} /> SSMT
                </label>
              </>
            )
          })()}
        </div>
        <div className="sim-panel-stats">
          {renderSimSidebarStats(advancedStats1 ?? basicStats1)}
        </div>
      </div>

      <div className="sim-middle">
        <div className="simulation-controls-row">
          <div className="sim-controls-group">
            <label style={{ marginRight: 8 }}>Simulation Type:</label>
            <select className="sim-type-select" value={simulationType} onChange={(e) => setSimulationType(e.target.value)}>
              <option value="acceleration">Acceleration</option>
              <option value="mini-turbo">Mini-turbo</option>
            </select>
            <label style={{ marginLeft: 12 }} className={selectedVehicle1 && selectedCharacter1 && selectedVehicle2 && selectedCharacter2 ? '' : 'disabled-option'}>
              <input type="checkbox" disabled={!(selectedVehicle1 && selectedCharacter1 && selectedVehicle2 && selectedCharacter2)} checked={differentialMode} onChange={(e) => setDifferentialMode(e.target.checked)} /> Differential Mode
            </label>
          </div>
          {loading && <div className="sim-loading-indicator">Running...</div>}
        </div>

        <div className="simulation-plot">
          <TimePlot simulationResult={simulationResult} differential={differentialMode} unit={speedUnit} simulationTime={simulationTime} />
        </div>

        <div className="simulation-footer">
          <div className="simulation-time-group">
            <label style={{ marginRight: 8 }}>Simulation Time: {simulationTime}s</label>
            <input className="simulation-slider" type="range" min={3} max={20} value={simulationTime} onChange={(e) => setSimulationTime(parseInt(e.target.value, 10))} />
          </div>

          <div className="simulation-units-group">
            <label style={{ marginRight: 6 }}>Units:</label>
            <div className="simulation-unit-toggle-row">
              <span style={{ fontSize: 12 }}>akm/h</span>
              <label className="unit-toggle" aria-label="Toggle speed units">
                <input
                  type="checkbox"
                  className="unit-toggle-checkbox"
                  checked={speedUnit === 'u/f'}
                  onChange={(e) => setSpeedUnit(e.target.checked ? 'u/f' : 'akm/h')}
                />
                <span className="unit-toggle-slider" aria-hidden="true" />
              </label>
              <span style={{ fontSize: 12 }}>u/f</span>
            </div>
          </div>
        </div>
      </div>

      <div className="sim-panel combo2-panel">
        <h4>Combo 2</h4>
        {/* Selected combo display: show vehicle + character names centered */}
        <div className="combo-display">
          {(() => {
            const v = vehicles.find(vv => String(vv.id) === String(selectedVehicle2))
            const c = characters.find(cc => String(cc.id) === String(selectedCharacter2))
            if (!v && !c) return (
              <div className="combo-display-lines">
                <div className="combo-vehicle"><strong>-</strong></div>
                <div className="combo-character"><strong>-</strong></div>
              </div>
            )
            return (
              <div className="combo-display-lines">
                <div className="combo-vehicle">{v ? v.name : '-'}</div>
                <div className="combo-character">{c ? c.name : '-'}</div>
              </div>
            )
          })()}
        </div>
        <div className="sim-panel-controls">
          {(() => {
            const combo2Ready = selectedVehicle2 && selectedCharacter2
            const smtEnabled = simulationType === 'mini-turbo'
            const ssmtEnabled = simulationType === 'acceleration'

            return (
              <>
                <label className={combo2Ready ? '' : 'disabled-option'}>
                  <input type="checkbox" disabled={!combo2Ready} checked={wheelie2} onChange={(e) => setWheelie2(e.target.checked)} /> Wheelie
                </label>
                <label className={combo2Ready && smtEnabled ? '' : 'disabled-option'}>
                  <input type="checkbox" disabled={!(combo2Ready && smtEnabled)} checked={smt2} onChange={(e) => setSmt2(e.target.checked)} /> SMT
                </label>
                <label className={combo2Ready && ssmtEnabled ? '' : 'disabled-option'}>
                  <input type="checkbox" disabled={!(combo2Ready && ssmtEnabled)} checked={ssmt2} onChange={(e) => setSsmt2(e.target.checked)} /> SSMT
                </label>
              </>
            )
          })()}
        </div>
        <div className="sim-panel-stats">
          {renderSimSidebarStats(advancedStats2 ?? basicStats2)}
        </div>
      </div>
    </div>
  )

  return (
    <div className="app" data-theme={theme}>
      <header>
        <div className="header-combo combo1">
          <h4>Combo 1</h4>
          <select className="combo1-select" value={selectedVehicle1} onChange={(e) => setSelectedVehicle1(e.target.value)}>
            <option value="">Select Vehicle</option>
            {vehicles.map(vehicle => (
              <option key={vehicle.id} value={vehicle.id}>{vehicle.name}</option>
            ))}
          </select>
          <select className="combo1-select" value={selectedCharacter1} onChange={(e) => setSelectedCharacter1(e.target.value)}>
            <option value="">Select Character</option>
            {characters.map(character => (
              <option key={character.id} value={character.id}>{character.name}</option>
            ))}
          </select>
        </div>

        <div className="header-center">
          <h1>Combo Compare</h1>
          <div className="mode-selector">
            <button
              className={statsMode === 'vanilla' ? 'active' : ''}
              onClick={() => changeStatsMode('vanilla')}
            >
              Vanilla Stats
            </button>
            <button
              className={statsMode === 'limitless' ? 'active' : ''}
              onClick={() => changeStatsMode('limitless')}
            >
              Limitless Stats
            </button>
          </div>
          <div className="theme-toggle">
            <button
              className="theme-toggle-button"
              onClick={toggleTheme}
              title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              aria-pressed={theme === 'dark'}
            >
              {theme === 'dark' ? <MoonIcon className="theme-toggle-icon" /> : <SunIcon className="theme-toggle-icon" />}
            </button>
          </div>
        </div>

        <div className="header-combo combo2">
          <div className="combo-label">Combo 2</div>
          <select className="combo2-select" value={selectedVehicle2} onChange={(e) => setSelectedVehicle2(e.target.value)}>
            <option value="">Select Vehicle</option>
            {vehicles.map(vehicle => (
              <option key={vehicle.id} value={vehicle.id}>{vehicle.name}</option>
            ))}
          </select>
          <select className="combo2-select" value={selectedCharacter2} onChange={(e) => setSelectedCharacter2(e.target.value)}>
            <option value="">Select Character</option>
            {characters.map(character => (
              <option key={character.id} value={character.id}>{character.name}</option>
            ))}
          </select>
        </div>
      </header>

      <div className="tabs">
        <button
          className={activeTab === 'basic' ? 'active' : ''}
          onClick={() => setActiveTab('basic')}
        >
          Basic Stats
        </button>
        <button
          className={activeTab === 'advanced' ? 'active' : ''}
          onClick={() => setActiveTab('advanced')}
        >
          Advanced Stats
        </button>
        <button
          className={activeTab === 'simulation' ? 'active' : ''}
          onClick={() => setActiveTab('simulation')}
        >
          Simulation
        </button>
      </div>

      <main>
        {activeTab === 'basic' && renderBasicStats()}
        {activeTab === 'advanced' && renderAdvancedStats()}
          
        {activeTab === 'simulation' && renderSimulation()}
      </main>
      
      <footer className="app-footer">
        <div className="footer-inner">
          <div className="footer-about">
            <div className="footer-title">About</div>
            <div className="about-text">Combo Compare is a tool to compare Mario Kart Wii vehicle &amp; character combinations with support for MKW: Limitless rebalanced stats. It also provides simple simulations to compare combo effectiveness.</div>
          </div>
          <div className="footer-links">
            <div className="footer-title">Links</div>
            <a href="https://wiki.tockdom.com/wiki/KartParam.bin" target="_blank" rel="noopener noreferrer">Stats on the Wiki</a>
            <a href="https://wiki.tockdom.com/wiki/Mario_Kart_Wii:_Limitless" target="_blank" rel="noopener noreferrer">Limitless Wiki</a>
            <a href="https://discord.com/invite/98cfKG5mz4" target="_blank" rel="noopener noreferrer">Limitless Discord</a>
             <a href="https://github.com/Blazico1/combo-compare" target="_blank" rel="noopener noreferrer">GitHub</a>
             <a href="/combo-compare/vehicles" target="_self">Vehicle Stats</a>
             <a href="/combo-compare/characters" target="_self">Character Stats</a>
          </div>
          <div className="footer-credits">
            <div className="footer-title">Credits</div>
            <div>Thanks to <a className="credit-link" href="https://www.youtube.com/@campbellmop355" target="_blank" rel="noopener noreferrer">CampbellMop</a> for providing useful information on the physics of Mario Kart Wii.</div>
            <div>Built by <a className="credit-link" href="https://github.com/Blazico1" target="_blank" rel="noopener noreferrer">Blazico</a>.</div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App



