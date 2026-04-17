import StatsTablePage from './stats-table-page.jsx'

const characterColumns = [
  { key: 'name', label: 'Character' },
  { key: 'weight_class', label: 'Weight Class' },
  { key: 'weight', label: 'Weight' },
  { key: 'speed', label: 'Speed' },
  { key: 'turn_speed', label: 'Turning Speed' },
  { key: 'a0_accel', label: 'A0 Accel' },
  { key: 'a1_accel', label: 'A1 Accel' },
  { key: 'a2_accel', label: 'A2 Accel' },
  { key: 'a3_accel', label: 'A3 Accel' },
  { key: 'handling', label: 'Handling' },
  { key: 'drift', label: 'Drift' },
  { key: 'mini_turbo', label: 'Mini Turbo' },
  { key: 'light_off_road', label: 'Light Off-Road' },
  { key: 'medium_off_road', label: 'Medium Off-Road' },
  { key: 'heavy_off_road', label: 'Heavy Off-Road' },
  { key: 'traction', label: 'Traction' }
]

function CharacterStatsPage() {
  return (
    <StatsTablePage
      title="Character Stats"
      endpoint="/api/character-table"
      columns={characterColumns}
      currentTable="characters"
    />
  )
}

export default CharacterStatsPage
