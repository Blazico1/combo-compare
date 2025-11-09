import { useState, useEffect, Fragment } from 'react'
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

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
)

function App() {
  console.log('App component rendering')
  const [activeTab, setActiveTab] = useState('basic')
  const [statsMode, setStatsMode] = useState('vanilla')
  const [activeMode, setActiveMode] = useState('compare')
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
  const [hide1, setHide1] = useState(false)
  const [hide2, setHide2] = useState(false)
  const [simulationResult, setSimulationResult] = useState(null)
  const [loading, setLoading] = useState(false)

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
  useEffect(() => {
    loadVehicles()
    loadCharacters()
  }, [statsMode])

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
  }, [selectedVehicle1, selectedCharacter1, statsMode])

  useEffect(() => {
    if (selectedVehicle2 || selectedCharacter2) {
      loadBasicStats(2)
      loadAdvancedStats(2)
    } else {
      setBasicStats2(null)
      setAdvancedStats2(null)
    }
  }, [selectedVehicle2, selectedCharacter2, statsMode])

  const loadVehicles = async () => {
    try {
      const response = await fetch(`/api/vehicles?mode=${statsMode}`)
      const data = await response.json()
      setVehicles(data.vehicles)
    } catch (error) {
      console.error('Error loading vehicles:', error)
    }
  }

  const loadCharacters = async () => {
    try {
      const response = await fetch(`/api/characters?mode=${statsMode}`)
      const data = await response.json()
      setCharacters(data.characters)
    } catch (error) {
      console.error('Error loading characters:', error)
    }
  }

  const changeStatsMode = (mode) => {
    // If the user clicked the currently-active mode, do nothing.
    // This prevents accidentally clearing the loaded stats when the button is clicked repeatedly.
    if (mode === statsMode) return

    setStatsMode(mode)
    // Clear current stats when mode changes
    setBasicStats1(null)
    setBasicStats2(null)
    setAdvancedStats1(null)
    setAdvancedStats2(null)
    // Reload vehicles and characters for new mode
    loadVehicles()
    loadCharacters()
  }

  const loadBasicStats = async (comboNum) => {
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
    } catch (error) {
      console.error('Error loading basic stats:', error)
    }
  }

  const loadAdvancedStats = async (comboNum) => {
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
    } catch (error) {
      console.error('Error loading advanced stats:', error)
    }
  }

  const runSimulation = async () => {
    if (!selectedVehicle1 || !selectedCharacter1 || !selectedVehicle2 || !selectedCharacter2) {
      alert('Please select both combos')
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
        combo1: {
          vehicle_id: parseInt(selectedVehicle1, 10),
          character_id: parseInt(selectedCharacter1, 10),
          wheelie: wheelie1,
          ssmt: ssmt1,
          smt: smt1,
          hide: hide1
        },
        combo2: {
          vehicle_id: parseInt(selectedVehicle2, 10),
          character_id: parseInt(selectedCharacter2, 10),
          wheelie: wheelie2,
          ssmt: ssmt2,
          smt: smt2,
          hide: hide2
        },
        sim_type: simTypeMap[simulationType] || 'accel',
        differential: differentialMode,
        time: simulationTime
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
    } catch (error) {
      console.error('Error running simulation:', error)
      alert('Simulation error: ' + (error.message || error))
    } finally {
      setLoading(false)
    }
  }

  const getRadarData = () => {
    const labels = ['Speed', 'Weight', 'Acceleration', 'Handling', 'Drift', 'Offroad', 'Mini Turbo']
    const keys = ['speed', 'weight', 'acceleration', 'handling', 'drift', 'offroad', 'mini_turbo']
    const datasets = []
    if (basicStats1) {
      const data1 = keys.map(key => basicStats1[key] || 0)
      datasets.push({
        label: 'Combo 1',
        data: data1,
        backgroundColor: 'rgba(34, 68, 255, 0.25)',
        borderColor: '#2244FF',
        borderWidth: 2,
        pointRadius: 0, // No markers
      })
    }
    if (basicStats2) {
      const data2 = keys.map(key => basicStats2[key] || 0)
      datasets.push({
        label: 'Combo 2',
        data: data2,
        backgroundColor: 'rgba(255, 34, 34, 0.25)',
        borderColor: '#FF2222',
        borderWidth: 2,
        pointRadius: 0, // No markers
      })
    }
    return {
      labels,
      datasets,
    }
  }

  const renderBasicStats = () => (
    <div className="basic-stats-layout">
      <div className="combo-column combo1">
        <h3>Combo 1</h3>
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

      <div className="chart-column">
        <div className="radar-container">
          <div className="radar-chart">
            <Radar data={getRadarData()} width={600} height={600} options={{
              responsive: false,
              scales: {
                r: {
                  beginAtZero: true,
                  max: 1,
                  ticks: {
                    display: false, // Hide numbers like original
                  },
                  grid: {
                    color: '#888888',
                  },
                  angleLines: {
                    color: '#888888',
                  },
                  pointLabels: {
                    color: '#ffffff',
                    font: {
                      size: 12,
                    },
                  },
                },
              },
              plugins: {
                legend: {
                  display: false, // Remove legend
                },
              },
              elements: {
                point: {
                  radius: 0, // Ensure no markers
                },
              },
            }} />
          </div>
        </div>
      </div>

      <div className="combo-column combo2">
        <h3>Combo 2</h3>
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

    if (Array.isArray(value)) {
      return '[' + value.map(v => typeof v === 'number' ? v.toFixed(5) : String(v)).join(', ') + ']'
    }
    if (typeof value === 'number') {
      // If it's an integer, show as integer, otherwise 5 significant digits
      return Number.isInteger(value) ? String(value) : value.toFixed(5)
    }
    return String(value)
  }

  // Helper to extract values for expanded multiplier keys like 'speed_multipliers_0'
  const getStatValue = (statsObj, key) => {
    if (!statsObj) return undefined
    if (!key) return undefined
    // handle expanded multiplier keys
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
      { display: "Bump Deviation", key: "bump_deviation" },
      { display: "Speed", key: "speed" },
      { display: "Speed in Turn", key: "speed_in_turn" },
      { display: "Tilt", key: "tilt" },
      { display: "Manual Handling", key: "manual_handling" },
      { display: "Auto Handling", key: "auto_handling" },
      { display: "Handling Reactivity", key: "handling_reactivity" },
      { display: "Manual Drift", key: "manual_drift" },
      { display: "Auto Drift", key: "auto_drift" },
      { display: "Drift Reactivity", key: "drift_reactivity" },
      { display: "Outside Drift Angle", key: "outside_drift_angle" },
      { display: "Outside Drift Decrement", key: "outside_drift_decrement" },
      { display: "Mini Turbo Duration", key: "mini_turbo_duration" },
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
      { display: "Rotating Items Z Radius", key: "rotating_items_z_radius" },
      { display: "Rotating Items X Radius", key: "rotating_items_x_radius" },
      { display: "Rotating Items Y Distance", key: "rotating_items_y_distance" },
      { display: "Rotating Items Z Distance", key: "rotating_items_z_distance" },
      { display: "Max Normal Accel", key: "max_normal_accel" },
      { display: "Mega Mushroom Scale", key: "mega_mushroom_scale" },
      { display: "Tire Distance", key: "tire_distance" },
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
              <tr>
                <td>
                  <select className="combo1-select" value={selectedVehicle1} onChange={(e) => setSelectedVehicle1(e.target.value)}>
                    <option value="">Select Vehicle</option>
                    {vehicles.map(vehicle => (
                      <option key={vehicle.id} value={vehicle.id}>{vehicle.name}</option>
                    ))}
                  </select>
                </td>
                <td className="center-cell"><strong>Vehicle</strong></td>
                <td>
                  <select className="combo2-select" value={selectedVehicle2} onChange={(e) => setSelectedVehicle2(e.target.value)}>
                    <option value="">Select Vehicle</option>
                    {vehicles.map(vehicle => (
                      <option key={vehicle.id} value={vehicle.id}>{vehicle.name}</option>
                    ))}
                  </select>
                </td>
              </tr>

              <tr>
                <td>
                  <select className="combo1-select" value={selectedCharacter1} onChange={(e) => setSelectedCharacter1(e.target.value)}>
                    <option value="">Select Character</option>
                    {characters.map(character => (
                      <option key={character.id} value={character.id}>{character.name}</option>
                    ))}
                  </select>
                </td>
                <td className="center-cell"><strong>Character</strong></td>
                <td>
                  <select className="combo2-select" value={selectedCharacter2} onChange={(e) => setSelectedCharacter2(e.target.value)}>
                    <option value="">Select Character</option>
                    {characters.map(character => (
                      <option key={character.id} value={character.id}>{character.name}</option>
                    ))}
                  </select>
                </td>
              </tr>

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

  // Simulation UI has been removed. Show a lightweight placeholder so the tab remains available.
  const renderSimulation = () => (
    <div className="simulation-placeholder">
      <h2>Simulation — Placeholder</h2>
      <p>The simulation feature has been temporarily disabled and removed from this build.</p>
      <p>If you need it restored, open an issue or re-enable the simulation tab in development.</p>
    </div>
  )

  return (
    <div className="app">
      <header>
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
    </div>
  )
}

export default App