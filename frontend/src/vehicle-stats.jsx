import StatsTablePage from './stats-table-page.jsx'

const vehicleColumns = [
  { key: 'name', label: 'Vehicle' },
  { key: 'drift', label: 'Drift' },
  { key: 'weight_class', label: 'Weight Class' },
  { key: 'weight', label: 'Weight' },
  { key: 'speed', label: 'Speed' },
  { key: 'turn_speed', label: 'Turn Speed' },
  { key: 'a0_accel', label: 'A0 Accel' },
  { key: 'a1_accel', label: 'A1 Accel' },
  { key: 'a2_accel', label: 'A2 Accel' },
  { key: 'a3_accel', label: 'A3 Accel' },
  { key: 't1_accel', label: 'T1 Accel' },
  { key: 't2_accel', label: 'T2 Accel' },
  { key: 't3_accel', label: 'T3 Accel' },
  { key: 'a0_drift_accel', label: 'A0 Drift Accel' },
  { key: 'a1_drift_accel', label: 'A1 Drift Accel' },
  { key: 't1_drift_accel', label: 'T1 Drift Accel' },
  { key: 'manual_handling', label: 'Manual Handling' },
  { key: 'auto_handling', label: 'Auto Handling' },
  { key: 'handling_reactivity', label: 'Handling Reactivity' },
  { key: 'manual_drift', label: 'Manual Drift' },
  { key: 'auto_drift', label: 'Auto Drift' },
  { key: 'drift_reactivity', label: 'Drift Reactivity' },
  { key: 'drift_angle', label: 'Drift Angle' },
  { key: 'drift_end_correction', label: 'Drift End Correction' },
  { key: 'mini_turbo', label: 'Mini-Turbo' },
  { key: 'wall_kcl_speed', label: 'MT Charge Time', limitlessOnly: true },
  { key: 'invisible_wall_kcl_speed', label: 'SMT Charge Time', limitlessOnly: true },
  { key: 'slippy_road', label: 'Slippy Road' },
  { key: 'light_off_road', label: 'Light Off-Road' },
  { key: 'medium_off_road', label: 'Medium Off-Road' },
  { key: 'heavy_off_road', label: 'Heavy Off-Road' },
  { key: 'slippy_off_road', label: 'Slippy Off-Road' }
]

function VehicleStatsPage() {
  return (
    <StatsTablePage
      title="Vehicle Stats"
      endpoint="/api/vehicle-table"
      columns={vehicleColumns}
      currentTable="vehicles"
    />
  )
}

export default VehicleStatsPage
