import os
import sys

# Ensure the repository root is on sys.path so top-level packages (logic/) import correctly
parent_dir = os.path.dirname(os.path.dirname(__file__))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging

from logic import stats, simulation

app = FastAPI(title="Combo Compare API", version="1.0.0")

# Configure a simple module logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# Configure CORS origins from environment (comma-separated) with sensible defaults for local dev
allowed = os.environ.get('ALLOWED_ORIGINS')
if allowed:
    allow_list = [o.strip() for o in allowed.split(',') if o.strip()]
else:
    allow_list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# If a built frontend exists under ../frontend/dist, serve it as static files
repo_root = os.path.dirname(os.path.dirname(__file__))
frontend_dist = os.path.join(repo_root, 'frontend', 'dist')
if os.path.isdir(frontend_dist):
    app.mount('/', StaticFiles(directory=frontend_dist, html=True), name='frontend')


class StatsManager:
    """Loads and provides access to vanilla and limitless stats."""

    def __init__(self):
        self.vanilla: Optional[Dict[str, Any]] = None
        self.limitless: Optional[Dict[str, Any]] = None
        self._load()

    def _load(self) -> None:
        try:
            backend_dir = os.path.dirname(__file__)
            kart_path = os.path.join(backend_dir, 'kartParam.bin')
            driver_path = os.path.join(backend_dir, 'driverParam.bin')

            # Vanilla files must exist
            if not (os.path.exists(kart_path) and os.path.exists(driver_path)):
                logger.warning('Vanilla stats files not found in backend directory')
                self.vanilla = None
                self.limitless = None
                return

            vehicles = stats.parse_stats(kart_path)
            stats.set_names(vehicles, False)
            characters = stats.parse_stats(driver_path)
            stats.set_names(characters, True)

            self.vanilla = {'vehicles': vehicles, 'characters': characters}

            # Try loading limitless; fall back to vanilla when missing
            limitless_kart = os.path.join(backend_dir, 'limitless_kartParam.bin')
            limitless_driver = os.path.join(backend_dir, 'limitless_driverParam.bin')
            if os.path.exists(limitless_kart) and os.path.exists(limitless_driver):
                lv = stats.parse_stats(limitless_kart)
                stats.set_names(lv, False)
                lc = stats.parse_stats(limitless_driver)
                stats.set_names(lc, True)
                self.limitless = {'vehicles': lv, 'characters': lc}
            else:
                self.limitless = self.vanilla

            logger.info("Stats loaded: vanilla=%s limitless=%s", self.vanilla is not None, self.limitless is not None)
        except Exception as e:
            logger.exception('Error loading stats: %s', e)
            self.vanilla = None
            self.limitless = None

    def get_by_mode(self, mode: str) -> Optional[Dict[str, Any]]:
        return self.limitless if mode == 'limitless' else self.vanilla


_stats_manager: Optional[StatsManager] = None


def get_stats_manager() -> StatsManager:
    global _stats_manager
    if _stats_manager is None:
        _stats_manager = StatsManager()
    return _stats_manager


@app.on_event('startup')
def on_startup():
    # Ensure stats are loaded on startup
    get_stats_manager()


# --- API endpoints ---
@app.get('/api/vehicles')
def api_vehicles(mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    vehicles = [{'id': v.id, 'name': v.name} for v in stats_data['vehicles']]
    vehicles.sort(key=lambda x: x['name'].lower())
    return {'vehicles': vehicles}


@app.get('/api/characters')
def api_characters(mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    characters = [{'id': c.id, 'name': c.name} for c in stats_data['characters']]
    characters.sort(key=lambda x: x['name'].lower())
    return {'characters': characters}


# Vehicle-only / Character-only basic stats (must appear before pair route)
@app.get('/api/basic-stats/vehicle/{vehicle_id}')
def api_basic_vehicle(vehicle_id: int, mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    try:
        vehicle = next(v for v in stats_data['vehicles'] if v.id == vehicle_id)
        v_stats = vehicle.get_basic_stats()
        norm = stats.normalise_stats(v_stats=v_stats, c_stats=stats.EMPTY_DICT(), vehicles=stats_data['vehicles'], characters=[])
        return {'stats': norm}
    except StopIteration:
        raise HTTPException(status_code=404, detail='Vehicle not found')


@app.get('/api/basic-stats/character/{character_id}')
def api_basic_character(character_id: int, mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    try:
        character = next(c for c in stats_data['characters'] if c.id == character_id)
        c_stats = character.get_basic_stats()
        norm = stats.normalise_stats(v_stats=stats.EMPTY_DICT(), c_stats=c_stats, vehicles=[], characters=stats_data['characters'])
        return {'stats': norm}
    except StopIteration:
        raise HTTPException(status_code=404, detail='Character not found')


# Pair basic stats
@app.get('/api/basic-stats/{vehicle_id}/{character_id}')
def api_basic_pair(vehicle_id: int, character_id: int, mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    try:
        vehicle = next(v for v in stats_data['vehicles'] if v.id == vehicle_id)
        character = next(c for c in stats_data['characters'] if c.id == character_id)
        v_stats = vehicle.get_basic_stats()
        c_stats = character.get_basic_stats()
        norm = stats.normalise_stats(v_stats=v_stats, c_stats=c_stats, vehicles=stats_data['vehicles'], characters=stats_data['characters'])
        return {'stats': norm}
    except StopIteration:
        raise HTTPException(status_code=404, detail='Vehicle or character not found')


# Vehicle-only / Character-only advanced stats
@app.get('/api/advanced-stats/vehicle/{vehicle_id}')
def api_advanced_vehicle(vehicle_id: int, mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    try:
        vehicle = next(v for v in stats_data['vehicles'] if v.id == vehicle_id)
        return {'stats': vehicle.get_advanced_stats()}
    except StopIteration:
        raise HTTPException(status_code=404, detail='Vehicle not found')


@app.get('/api/advanced-stats/character/{character_id}')
def api_advanced_character(character_id: int, mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    try:
        character = next(c for c in stats_data['characters'] if c.id == character_id)
        return {'stats': character.get_advanced_stats()}
    except StopIteration:
        raise HTTPException(status_code=404, detail='Character not found')


# Pair advanced stats
@app.get('/api/advanced-stats/{vehicle_id}/{character_id}')
def api_advanced_pair(vehicle_id: int, character_id: int, mode: str = 'vanilla'):
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=404, detail='Stats not loaded')
    try:
        vehicle = next(v for v in stats_data['vehicles'] if v.id == vehicle_id)
        character = next(c for c in stats_data['characters'] if c.id == character_id)
        v_dict = vehicle.get_advanced_stats()
        c_dict = character.get_advanced_stats()
        out = {}
        all_keys = set(v_dict.keys()) | set(c_dict.keys())
        for key in all_keys:
            v_val = v_dict.get(key)
            c_val = c_dict.get(key)
            if key in ('weight_class', 'num_tires', 'drift_type'):
                out[key] = v_val if v_val is not None else c_val
            else:
                if v_val is not None and c_val is not None:
                    out[key] = v_val + c_val
                else:
                    out[key] = v_val if v_val is not None else c_val
        return {'stats': out}
    except StopIteration:
        raise HTTPException(status_code=404, detail='Vehicle or character not found')


@app.post('/api/simulate')
def api_simulate(data: Dict[str, Any]):
    mode = data.get('mode', 'vanilla')
    stats_data = get_stats_manager().get_by_mode(mode)
    if not stats_data:
        raise HTTPException(status_code=500, detail='Stats not loaded')
    try:
        combo1 = data.get('combo1', None)
        combo2 = data.get('combo2', None)
        sim_type = data.get('sim_type', 'accel')
        time = data.get('time', 10.0)

        # Accept simulation with either combo1 or combo2 (or both). If the caller
        # only provided combo2, treat it as combo1 for the purposes of single-run.
        if not combo1 and combo2:
            combo1 = combo2
            combo2 = None

        if not combo1:
            raise HTTPException(status_code=400, detail='No combo provided')

        wheelie1 = bool(combo1.get('wheelie', False))
        ssmt1 = bool(combo1.get('ssmt', False))
        smt1 = bool(combo1.get('smt', False))

        # Look up combo1
        vehicle1 = next(v for v in stats_data['vehicles'] if v.id == combo1.get('vehicle_id'))
        character1 = next(c for c in stats_data['characters'] if c.id == combo1.get('character_id'))

        # Determine if combo2 provided and valid
        result2 = None
        vehicle2 = character2 = None
        if combo2 and combo2.get('vehicle_id') is not None and combo2.get('character_id') is not None:
            wheelie2 = bool(combo2.get('wheelie', False))
            ssmt2 = bool(combo2.get('ssmt', False))
            smt2 = bool(combo2.get('smt', False))
            vehicle2 = next(v for v in stats_data['vehicles'] if v.id == combo2.get('vehicle_id'))
            character2 = next(c for c in stats_data['characters'] if c.id == combo2.get('character_id'))

        # Run simulations
        if sim_type == 'accel':
            result1 = simulation.simulate_accel(vehicle1.get_basic_stats(), character1.get_basic_stats(), wheelie=wheelie1, ssmt=ssmt1, time=time)
            if vehicle2 is not None:
                result2 = simulation.simulate_accel(vehicle2.get_basic_stats(), character2.get_basic_stats(), wheelie=wheelie2, ssmt=ssmt2, time=time)
        else:
            # For mini-turbo simulation the SMT flag (short mini-turbo) comes from the 'smt' payload
            result1 = simulation.simulate_mini_turbo(vehicle1.get_basic_stats(), character1.get_basic_stats(), wheelie=wheelie1, SMT=smt1, time=time)
            if vehicle2 is not None:
                result2 = simulation.simulate_mini_turbo(vehicle2.get_basic_stats(), character2.get_basic_stats(), wheelie=wheelie2, SMT=smt2, time=time)

        # Convert distances from internal units (units per frame) to metres.
        # The simulation produces distances in 'units' (u) per frame.
        # By convention 216 u == 1 m, so divide by 216 to get metres.
        d1_m = (result1[2] / 216.0) if result1[2] is not None else result1[2]
        out = {
            'combo1': {
                'times': result1[0].tolist(),
                'speeds': result1[1].tolist(),
                'distances': d1_m.tolist(),
            }
        }
        if result2 is not None:
            _d2 = result2[2]
            d2_m = (_d2 / 216.0) if _d2 is not None else _d2
            out['combo2'] = {
                'times': result2[0].tolist(),
                'speeds': result2[1].tolist(),
                'distances': d2_m.tolist(),
            }
        else:
            out['combo2'] = None

        return out
    except StopIteration:
        detail_msg = 'Vehicle or character not found'
        raise HTTPException(status_code=404, detail=detail_msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/api/health')
def api_health():
    mgr = get_stats_manager()
    vanilla_loaded = mgr.vanilla is not None
    limitless_loaded = mgr.limitless is not None
    status = 'healthy' if (vanilla_loaded or limitless_loaded) else 'unhealthy'
    return {
        'status': status,
        'vanilla_loaded': vanilla_loaded,
        'limitless_loaded': limitless_loaded,
    }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

