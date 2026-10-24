<!DOCTYPE html>
<html lang="en" class="h-full bg-[#070B12] text-slate-200">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ORBITWATCH // Satellite Telemetry & Orbit Tracking System</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Font Awesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <!-- Google Fonts: Orbitron & Inter -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@500;700;900&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            brand: {
              bg: '#070B12',
              card: '#0D1527',
              border: '#1E293B',
              borderGlow: '#00F0FF33',
              cyan: '#00F0FF',
              green: '#00FF88',
              amber: '#FF9F1C',
              red: '#FF4757',
              darkBlue: '#0B132B'
            }
          },
          fontFamily: {
            mono: ['Orbitron', 'monospace'],
            sans: ['Inter', 'sans-serif']
          }
        }
      }
    }
  </script>

  <style>
    /* Custom Grid Background Overlay */
    .bg-grid-pattern {
      background-size: 30px 30px;
      background-image: 
        linear-gradient(to right, rgba(0, 240, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
    }
    
    /* Custom Scrollbar Styling */
    ::-webkit-scrollbar {
      width: 5px;
      height: 5px;
    }
    ::-webkit-scrollbar-track {
      background: #070B12;
    }
    ::-webkit-scrollbar-thumb {
      background: #1E293B;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #00F0FF;
    }

    /* Pulse Glow Animations */
    @keyframes ping-slow {
      0% { transform: scale(1); opacity: 0.8; }
      100% { transform: scale(2.5); opacity: 0; }
    }
    .animate-ping-slow {
      animation: ping-slow 2s cubic-bezier(0, 0, 0.2, 1) infinite;
    }

    .glow-cyan {
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }
    .text-glow-cyan {
      text-shadow: 0 0 8px rgba(0, 240, 255, 0.6);
    }
  </style>
</head>
<body class="h-full flex flex-col font-sans bg-brand-bg bg-grid-pattern overflow-x-hidden select-none">

  <!-- TOP HEADER BAR -->
  <header class="h-16 border-b border-brand-border bg-brand-card/90 backdrop-blur px-4 flex items-center justify-between shrink-0 z-30">
    <div class="flex items-center space-x-3">
      <div class="p-2 bg-brand-cyan/10 rounded-lg border border-brand-cyan/30 text-brand-cyan">
        <i class="fa-solid fa-satellite fa-lg animate-pulse"></i>
      </div>
      <div>
        <h1 class="font-mono text-base md:text-lg font-black tracking-wider text-white flex items-center gap-2">
          ORBITWATCH <span class="text-brand-cyan text-xs font-normal border border-brand-cyan/40 px-2 py-0.5 rounded bg-brand-cyan/10">// TELEMETRY & TRACKING</span>
        </h1>
        <p class="text-[10px] text-slate-400 font-mono tracking-widest hidden sm:block">GLOBAL REAL-TIME SATELLITE OPERATIONS & ANOMALY DETECTION</p>
      </div>
    </div>

    <!-- MISSION STATS (Inspired by reference image summary bar) -->
    <div class="hidden lg:flex items-center space-x-8 font-mono text-sm">
      <div class="flex items-center space-x-2">
        <span class="relative flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-green opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-brand-green"></span>
        </span>
        <span id="stat-nominal" class="text-brand-green font-bold text-lg">145</span>
        <span class="text-slate-400 text-xs">NOMINAL</span>
      </div>

      <div class="flex items-center space-x-2">
        <span class="relative flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-amber opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-brand-amber"></span>
        </span>
        <span id="stat-advisory" class="text-brand-amber font-bold text-lg">18</span>
        <span class="text-slate-400 text-xs">ADVISORY</span>
      </div>

      <div class="flex items-center space-x-2">
        <span class="relative flex h-3 w-3">
          <span class="relative inline-flex rounded-full h-3 w-3 bg-brand-red"></span>
        </span>
        <span id="stat-offline" class="text-brand-red font-bold text-lg">19</span>
        <span class="text-slate-400 text-xs">OFFLINE / UNKNOWN</span>
      </div>
    </div>

    <!-- CLOCK & CONTROLS -->
    <div class="flex items-center space-x-4">
      <div class="text-right font-mono hidden md:block">
        <div id="clock-gmt" class="text-xs text-brand-cyan font-bold tracking-widest">00:00:00 UTC</div>
        <div id="clock-date" class="text-[10px] text-slate-400">2026-10-24</div>
      </div>
      
      <button id="btn-pause-stream" class="p-2 px-3 bg-brand-card hover:bg-slate-800 border border-brand-border rounded text-xs font-mono text-slate-300 hover:text-brand-cyan transition flex items-center gap-2">
        <i class="fa-solid fa-pause text-brand-cyan" id="pause-icon"></i>
        <span id="pause-text" class="hidden sm:inline">LIVE FEED</span>
      </button>

      <button id="btn-reset-view" class="p-2 bg-brand-card hover:bg-slate-800 border border-brand-border rounded text-xs text-slate-300 hover:text-brand-cyan transition" title="Reset Viewport">
        <i class="fa-solid fa-arrows-to-eye"></i>
      </button>
    </div>
  </header>

  <!-- MAIN DASHBOARD CONTENT GRID -->
  <div class="flex-1 flex flex-col lg:flex-row overflow-hidden p-3 gap-3">

    <!-- LEFT SIDE PANEL: SATELLITE ROSTER (Like image left panel) -->
    <aside class="w-full lg:w-80 bg-brand-card/90 border border-brand-border rounded-xl flex flex-col overflow-hidden shrink-0">
      <div class="p-3 border-b border-brand-border bg-slate-900/50 flex flex-col gap-2">
        <div class="flex justify-between items-center">
          <span class="font-mono text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
            <i class="fa-solid fa-layer-group text-brand-cyan"></i> Active Satellites
          </span>
          <span id="sat-count-badge" class="text-[10px] font-mono px-2 py-0.5 bg-brand-cyan/10 border border-brand-cyan/30 text-brand-cyan rounded">7 SATS</span>
        </div>

        <!-- Filter / Search Box -->
        <div class="relative">
          <input type="text" id="sat-search" placeholder="Search target or NORAD ID..." 
            class="w-full bg-slate-950 border border-slate-800 rounded px-8 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-brand-cyan font-mono transition">
          <i class="fa-solid fa-search absolute left-2.5 top-2 text-slate-500 text-xs"></i>
        </div>

        <!-- Status Filter Tabs -->
        <div class="flex gap-1 pt-1 text-[10px] font-mono">
          <button data-filter="ALL" class="filter-tab flex-1 py-1 bg-brand-cyan/20 border border-brand-cyan text-brand-cyan rounded text-center">ALL</button>
          <button data-filter="OK" class="filter-tab flex-1 py-1 bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 rounded text-center">OK</button>
          <button data-filter="ADVISORY" class="filter-tab flex-1 py-1 bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 rounded text-center">WARN</button>
          <button data-filter="OFFLINE" class="filter-tab flex-1 py-1 bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 rounded text-center">OFF</button>
        </div>
      </div>

      <!-- Satellite List -->
      <div id="satellite-list" class="flex-1 overflow-y-auto divide-y divide-slate-800/60 font-mono text-xs">
        <!-- JS-Generated Dynamic Satellites -->
      </div>

      <!-- Quick Summary Footer -->
      <div class="p-2 border-t border-brand-border bg-slate-950/60 text-[10px] font-mono text-slate-400 flex justify-between">
        <span>DOWNLINK STREAM: <span class="text-brand-green">ACTIVE</span></span>
        <span>LATENCY: <span class="text-brand-cyan">18ms</span></span>
      </div>
    </aside>

    <!-- CENTER & RIGHT MAIN WORKSPACE -->
    <main class="flex-1 flex flex-col gap-3 overflow-y-auto lg:overflow-hidden">
      
      <!-- TOP MAP & VISUALIZER ROW -->
      <div class="h-[360px] md:h-[440px] bg-brand-card/90 border border-brand-border rounded-xl flex flex-col relative overflow-hidden shrink-0">
        <!-- Map Header Toolbar -->
        <div class="p-2 px-4 bg-slate-950/80 border-b border-brand-border flex justify-between items-center z-10 font-mono text-xs">
          <div class="flex items-center gap-3">
            <span id="current-target-title" class="text-brand-cyan font-bold flex items-center gap-2">
              <i class="fa-solid fa-crosshairs text-brand-cyan animate-spin" style="animation-duration: 8s;"></i>
              TARGET: ISS (ZARYA) [NORAD #25544]
            </span>
            <span id="target-status-pill" class="text-[10px] px-2 py-0.5 rounded bg-brand-green/20 text-brand-green border border-brand-green/30">STATUS: NOMINAL</span>
          </div>

          <!-- Coordinate Readout -->
          <div class="hidden md:flex gap-4 text-[11px] text-slate-400">
            <div>LAT: <span id="map-lat" class="text-slate-200 font-mono">24.512° N</span></div>
            <div>LON: <span id="map-lon" class="text-slate-200 font-mono">81.332° W</span></div>
            <div>ALT: <span id="map-alt" class="text-slate-200 font-mono">418.4 km</span></div>
            <div>VEL: <span id="map-vel" class="text-brand-cyan font-mono">7.66 km/s</span></div>
          </div>
        </div>

        <!-- Canvas Map Layer -->
        <div class="relative flex-1 bg-[#050811] w-full h-full overflow-hidden">
          <canvas id="orbit-map-canvas" class="w-full h-full block cursor-crosshair"></canvas>
          
          <!-- Tactical Overlay Canvas Info Overlay -->
          <div class="absolute bottom-3 left-3 bg-slate-950/80 border border-brand-border/80 backdrop-blur rounded p-2 text-[10px] font-mono text-slate-400 flex flex-col gap-1 pointer-events-none">
            <div class="text-brand-cyan font-bold">GROUND TRACK SIMULATOR</div>
            <div>PROJECTION: EQUITECTANGULAR CYLINDRICAL</div>
            <div>COMM STATIONS: 6 LINKED</div>
          </div>

          <!-- Map Controls Overlay -->
          <div class="absolute top-3 right-3 flex flex-col gap-1 z-10">
            <button id="btn-zoom-in" class="p-2 bg-slate-950/90 hover:bg-slate-800 border border-brand-border rounded text-slate-300 text-xs w-8 h-8 flex items-center justify-center">
              <i class="fa-solid fa-plus"></i>
            </button>
            <button id="btn-zoom-out" class="p-2 bg-slate-950/90 hover:bg-slate-800 border border-brand-border rounded text-slate-300 text-xs w-8 h-8 flex items-center justify-center">
              <i class="fa-solid fa-minus"></i>
            </button>
            <button id="btn-toggle-footprint" class="p-2 bg-slate-950/90 hover:bg-slate-800 border border-brand-border rounded text-brand-cyan text-xs w-8 h-8 flex items-center justify-center" title="Toggle Horizon Footprint">
              <i class="fa-solid fa-wifi"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- BOTTOM TELEMETRY GAUGES & CHARTS SECTION -->
      <div class="flex-1 grid grid-cols-1 md:grid-cols-3 xl:grid-cols-4 gap-3 min-h-[300px]">

        <!-- GAUGES PANEL (Inspired by reference image 3 dials) -->
        <div class="bg-brand-card/90 border border-brand-border rounded-xl p-3 flex flex-col justify-between">
          <div class="font-mono text-xs font-bold text-slate-300 mb-2 flex justify-between items-center border-b border-brand-border/60 pb-2">
            <span><i class="fa-solid fa-gauge-high text-brand-cyan mr-1"></i> ANALOG TELEMETRY GAUGES</span>
            <span class="text-[10px] text-brand-green animate-pulse">● LIVE</span>
          </div>

          <div class="grid grid-cols-3 gap-2 flex-1 items-center">
            <!-- Gauge 1: Power / Voltage -->
            <div class="flex flex-col items-center">
              <div class="relative w-20 h-20 md:w-24 md:h-24">
                <canvas id="gauge-battery" class="w-full h-full"></canvas>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center pt-2">
                  <span id="gauge-bat-val" class="text-xs md:text-sm font-mono font-bold text-white">120.4</span>
                  <span class="text-[8px] text-slate-400 font-mono">VOLTS</span>
                </div>
              </div>
              <span class="text-[10px] font-mono text-slate-300 mt-1 text-center">Bus Voltage</span>
            </div>

            <!-- Gauge 2: Thermal Core -->
            <div class="flex flex-col items-center">
              <div class="relative w-20 h-20 md:w-24 md:h-24">
                <canvas id="gauge-temp" class="w-full h-full"></canvas>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center pt-2">
                  <span id="gauge-temp-val" class="text-xs md:text-sm font-mono font-bold text-brand-cyan">34.2</span>
                  <span class="text-[8px] text-slate-400 font-mono">°C TEMP</span>
                </div>
              </div>
              <span class="text-[10px] font-mono text-slate-300 mt-1 text-center">Core Thermal</span>
            </div>

            <!-- Gauge 3: Gyro Drift -->
            <div class="flex flex-col items-center">
              <div class="relative w-20 h-20 md:w-24 md:h-24">
                <canvas id="gauge-gyro" class="w-full h-full"></canvas>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center pt-2">
                  <span id="gauge-gyro-val" class="text-xs md:text-sm font-mono font-bold text-brand-amber">0.08</span>
                  <span class="text-[8px] text-slate-400 font-mono">DEG/S</span>
                </div>
              </div>
              <span class="text-[10px] font-mono text-slate-300 mt-1 text-center">Gyro Drift</span>
            </div>
          </div>

          <div class="mt-2 text-[10px] font-mono text-slate-400 bg-slate-950/60 p-1.5 rounded flex justify-between">
            <span>SOLAR BETA: <span class="text-brand-cyan">42.1°</span></span>
            <span>HEALTH: <span class="text-brand-green">98.4%</span></span>
          </div>
        </div>

        <!-- REAL-TIME TELEMETRY TIME-SERIES CHART -->
        <div class="bg-brand-card/90 border border-brand-border rounded-xl p-3 flex flex-col col-span-1 md:col-span-2">
          <div class="font-mono text-xs font-bold text-slate-300 mb-2 flex justify-between items-center border-b border-brand-border/60 pb-2">
            <span><i class="fa-solid fa-chart-line text-brand-cyan mr-1"></i> REAL-TIME TELEMETRY TIME-SERIES</span>
            <div class="flex gap-2">
              <button id="chart-toggle-snr" class="text-[10px] font-mono px-2 py-0.5 bg-brand-cyan/20 border border-brand-cyan text-brand-cyan rounded">SNR Signal</button>
              <button id="chart-toggle-power" class="text-[10px] font-mono px-2 py-0.5 bg-slate-900 border border-slate-800 text-slate-400 rounded">Power Generation</button>
            </div>
          </div>
          <div class="flex-1 relative min-h-[140px]">
            <canvas id="telemetry-chart" class="w-full h-full"></canvas>
          </div>
        </div>

        <!-- LIVE EVENT & ANOMALY LOG FEED -->
        <div class="bg-brand-card/90 border border-brand-border rounded-xl p-3 flex flex-col col-span-1 xl:col-span-1">
          <div class="font-mono text-xs font-bold text-slate-300 mb-2 flex justify-between items-center border-b border-brand-border/60 pb-2">
            <span><i class="fa-solid fa-terminal text-brand-cyan mr-1"></i> TELEMETRY LOG</span>
            <button id="btn-clear-logs" class="text-[10px] text-slate-400 hover:text-brand-cyan"><i class="fa-solid fa-trash"></i></button>
          </div>
          
          <div id="telemetry-log-stream" class="flex-1 overflow-y-auto space-y-1.5 font-mono text-[11px] pr-1">
            <!-- Dynamically populated event logs -->
          </div>
        </div>

      </div>

    </main>
  </div>

  <!-- SATELLITE DETAILS MODAL / DRAWER -->
  <div id="sat-modal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center hidden p-4">
    <div class="bg-brand-card border border-brand-cyan/40 rounded-xl w-full max-w-xl p-5 shadow-2xl relative glow-cyan">
      <button id="btn-close-modal" class="absolute top-4 right-4 text-slate-400 hover:text-white">
        <i class="fa-solid fa-xmark text-lg"></i>
      </button>

      <div class="flex items-center space-x-3 mb-4">
        <div class="p-3 bg-brand-cyan/10 border border-brand-cyan/30 rounded-lg text-brand-cyan">
          <i class="fa-solid fa-satellite fa-xl"></i>
        </div>
        <div>
          <h2 id="modal-title" class="font-mono text-lg font-bold text-white">ISS (ZARYA)</h2>
          <div class="text-xs font-mono text-slate-400" id="modal-norad">NORAD ID: 25544 | INT DESIGNATOR: 1998-067A</div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3 font-mono text-xs mb-4">
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-slate-400 block text-[10px]">ORBIT TYPE</span>
          <span id="modal-orbit" class="text-slate-200 font-bold">LEO (Low Earth Orbit)</span>
        </div>
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-slate-400 block text-[10px]">INCLINATION</span>
          <span id="modal-inc" class="text-brand-cyan font-bold">51.64°</span>
        </div>
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-slate-400 block text-[10px]">OPERATIONAL STATUS</span>
          <span id="modal-status" class="text-brand-green font-bold">NOMINAL - ACTIVE</span>
        </div>
        <div class="bg-slate-950 p-3 rounded border border-slate-800">
          <span class="text-slate-400 block text-[10px]">PERIOD</span>
          <span id="modal-period" class="text-slate-200 font-bold">92.68 Minutes</span>
        </div>
      </div>

      <div class="bg-slate-950/80 p-3 rounded border border-slate-800 mb-4 font-mono text-xs">
        <div class="text-brand-cyan text-[11px] font-bold mb-1">PAYLOAD DIAGNOSTICS & TELEMETRY SUMMARY</div>
        <p id="modal-desc" class="text-slate-300 text-[11px] leading-relaxed">
          Primary communications bus nominal. Solar array gimbal tracking sun angle at optimum efficiency. Zero anomaly detections in primary reaction wheels during last pass.
        </p>
      </div>

      <div class="flex justify-end gap-2 font-mono text-xs">
        <button id="btn-modal-close" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded">Close</button>
        <button id="btn-modal-track" class="px-4 py-2 bg-brand-cyan/20 hover:bg-brand-cyan/30 text-brand-cyan border border-brand-cyan/40 rounded font-bold">Track Target</button>
      </div>
    </div>
  </div>

  <!-- MAIN SCRIPT LOGIC -->
  <script>
    // --- SATELLITE FLEET DATA DATASET ---
    const satelliteFleet = [
      {
        id: "ISS-25544",
        name: "ISS (ZARYA)",
        norad: "25544",
        type: "LEO - Space Station",
        status: "OK", // OK, ADVISORY, OFFLINE
        lat: 24.512,
        lon: -81.332,
        alt: 418.4,
        vel: 7.66,
        inc: 51.64,
        battery: 124.5,
        temp: 32.4,
        gyro: 0.04,
        snr: 42,
        pathColor: "#00F0FF",
        desc: "International Space Station orbital laboratory. All environmental control systems, solar array gimbals, and high-gain antenna tracking operating normally."
      },
      {
        id: "HST-20580",
        name: "HUBBLE ST",
        norad: "20580",
        type: "LEO - Telescope",
        status: "OK",
        lat: -12.431,
        lon: 45.210,
        alt: 535.1,
        vel: 7.59,
        inc: 28.47,
        battery: 118.2,
        temp: 28.1,
        gyro: 0.02,
        snr: 38,
        pathColor: "#00FF88",
        desc: "Hubble Space Telescope performing deep field UV spectroscopy observations. Fine guidance sensors locked on target star cluster."
      },
      {
        id: "SENT-2B",
        name: "SENTINEL-1A",
        norad: "39634",
        type: "Sun-Sync Orbit",
        status: "ADVISORY",
        lat: 68.210,
        lon: 12.401,
        alt: 693.0,
        vel: 7.50,
        inc: 98.18,
        battery: 98.4,
        temp: 48.7, // High temp advisory
        gyro: 0.18,
        snr: 28,
        pathColor: "#FF9F1C",
        desc: "C-band Synthetic Aperture Radar satellite. Thermal sensor reading higher than expected core temperature during dark-orbit phase. Secondary cooling active."
      },
      {
        id: "LANDSAT-9",
        name: "LANDSAT 9",
        norad: "49260",
        type: "Sun-Sync Orbit",
        status: "OK",
        lat: -45.120,
        lon: -120.330,
        alt: 705.2,
        vel: 7.50,
        inc: 98.20,
        battery: 121.0,
        temp: 29.8,
        gyro: 0.03,
        snr: 45,
        pathColor: "#00F0FF",
        desc: "Earth observation imaging satellite capturing multispectral land cover data downlinks over South America pass."
      },
      {
        id: "NOAA-20",
        name: "NOAA-20 JPSS",
        norad: "43013",
        type: "Polar Orbit",
        status: "OK",
        lat: 52.330,
        lon: 104.220,
        alt: 824.6,
        vel: 7.42,
        inc: 98.70,
        battery: 122.8,
        temp: 31.0,
        gyro: 0.05,
        snr: 40,
        pathColor: "#00FF88",
        desc: "Polar-orbiting weather satellite transmitting VIIRS radiometer imagery & atmospheric sounding profiles."
      },
      {
        id: "STARLINK-3021",
        name: "STARLINK-3021",
        norad: "51240",
        type: "LEO Constellation",
        status: "OFFLINE",
        lat: -33.220,
        lon: 78.440,
        alt: 540.0,
        vel: 7.60,
        inc: 53.20,
        battery: 42.0,
        temp: 12.1,
        gyro: 1.45,
        snr: 0,
        pathColor: "#FF4757",
        desc: "Communication satellite in safe-hold mode following transient attitude control fault. Telemetry link degraded."
      },
      {
        id: "GOES-16",
        name: "GOES-16 (EAST)",
        norad: "41866",
        type: "Geostationary",
        status: "OK",
        lat: 0.080,
        lon: -75.200,
        alt: 35786.0,
        vel: 3.07,
        inc: 0.03,
        battery: 130.2,
        temp: 35.1,
        gyro: 0.01,
        snr: 48,
        pathColor: "#00F0FF",
        desc: "Geostationary weather satellite providing full-disk infrared & lightning mapper coverage over Western Hemisphere."
      }
    ];

    // --- APPLICATION STATE ---
    let selectedSat = satelliteFleet[0];
    let isStreamLive = true;
    let statusFilter = "ALL";
    let activeMetric = "SNR"; // SNR or POWER
    let zoomLevel = 1.0;
    let showFootprint = true;

    // --- CANVAS MAP INITIALIZATION ---
    const canvas = document.getElementById('orbit-map-canvas');
    const ctx = canvas.getContext('2d');

    function resizeCanvas() {
      const rect = canvas.parentElement.getBoundingClientRect();
      canvas.width = rect.width * window.devicePixelRatio || 1;
      canvas.height = rect.height * window.devicePixelRatio || 1;
      ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Map Coordinates Converter (Lat/Lon to Canvas X/Y)
    function geoToCanvas(lat, lon, width, height) {
      // Map longitude (-180 to 180) -> X (0 to width)
      // Map latitude (-90 to 90) -> Y (height to 0)
      const x = ((lon + 180) / 360) * width;
      const y = ((90 - lat) / 180) * height;
      return { x, y };
    }

    // Dynamic World Map Map Renderer
    function drawWorldMap() {
      const w = canvas.width / (window.devicePixelRatio || 1);
      const h = canvas.height / (window.devicePixelRatio || 1);

      ctx.clearRect(0, 0, w, h);

      // Deep Space / Map Background
      ctx.fillStyle = '#050811';
      ctx.fillRect(0, 0, w, h);

      // Draw Grid Lines (Latitude / Longitude)
      ctx.strokeStyle = '#00F0FF0F';
      ctx.lineWidth = 1;

      // Longitude lines
      for (let x = 0; x < w; x += w / 12) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
      }

      // Latitude lines
      for (let y = 0; y < h; y += h / 6) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }

      // Draw Simplified Stylized Continents (Vector Outlines)
      drawContinents(ctx, w, h);

      // Draw Ground Communications Stations
      drawGroundStations(ctx, w, h);

      // Draw Orbital Tracks & Satellites
      satelliteFleet.forEach(sat => {
        const isSelected = (sat.id === selectedSat.id);
        
        // Draw Orbit Path Trajectory Curve
        drawOrbitPath(ctx, sat, w, h, isSelected);

        // Draw Horizon Footprint (if enabled & selected)
        if (isSelected && showFootprint) {
          drawGroundFootprint(ctx, sat, w, h);
        }

        // Draw Satellite Marker
        drawSatelliteMarker(ctx, sat, w, h, isSelected);
      });
    }

    // Draw Stylized Cyber Continents
    function drawContinents(ctx, w, h) {
      ctx.fillStyle = '#0D1A30';
      ctx.strokeStyle = '#00F0FF26';
      ctx.lineWidth = 1;

      // Stylized simplified continent polys
      const continents = [
        // North America
        [[-160,60], [-100,65], [-60,45], [-80,25], [-105,20], [-120,35]],
        // South America
        [[-80,10], [-40,0], [-50,-35], [-70,-50], [-80,-20]],
        // Eurasia
        [[10,60], [80,70], [140,60], [120,20], [80,20], [40,35]],
        // Africa
        [[-15,32], [35,32], [45,10], [30,-30], [10,-35], [-10,5]],
        // Australia
        [[115,-15], [150,-15], [145,-38], [115,-35]]
      ];

      continents.forEach(poly => {
        ctx.beginPath();
        poly.forEach((pt, i) => {
          const pos = geoToCanvas(pt[1], pt[0], w, h);
          if (i === 0) ctx.moveTo(pos.x, pos.y);
          else ctx.lineTo(pos.x, pos.y);
        });
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
      });
    }

    // Ground Link Stations
    const groundStations = [
      { name: "Goldstone", lat: 35.42, lon: -116.88 },
      { name: "Madrid", lat: 40.41, lon: -3.70 },
      { name: "Canberra", lat: -35.30, lon: 149.13 },
      { name: "Svalbard", lat: 78.22, lon: 15.65 }
    ];

    function drawGroundStations(ctx, w, h) {
      groundStations.forEach(st => {
        const pt = geoToCanvas(st.lat, st.lon, w, h);
        ctx.fillStyle = '#00F0FF';
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 2.5, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#00F0FF44';
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 6, 0, Math.PI * 2);
        ctx.stroke();
      });
    }

    // Draw Dynamic Sine Wave Sine Orbital Path Projection
    function drawOrbitPath(ctx, sat, w, h, isSelected) {
      ctx.save();
      ctx.beginPath();
      
      const numSteps = 100;
      const amplitude = (sat.inc / 90) * (h / 2.2);
      const startPt = geoToCanvas(sat.lat, sat.lon, w, h);

      for (let i = -numSteps / 2; i <= numSteps / 2; i++) {
        const stepLon = sat.lon + (i * 3.6);
        const stepLat = sat.lat + Math.sin(i * 0.1) * (sat.inc * 0.8);

        const canvasPt = geoToCanvas(stepLat, stepLon, w, h);

        if (i === -numSteps / 2) {
          ctx.moveTo(canvasPt.x, canvasPt.y);
        } else {
          ctx.lineTo(canvasPt.x, canvasPt.y);
        }
      }

      ctx.strokeStyle = isSelected ? sat.pathColor : sat.pathColor + '33';
      ctx.lineWidth = isSelected ? 2 : 1;
      if (isSelected) {
        ctx.setLineDash([4, 3]);
      } else {
        ctx.setLineDash([]);
      }
      ctx.stroke();
      ctx.restore();
    }

    // Horizon Coverage Footprint Circle
    function drawGroundFootprint(ctx, sat, w, h) {
      const pt = geoToCanvas(sat.lat, sat.lon, w, h);
      const radius = (sat.alt / 400) * 30; // Radius based on altitude

      ctx.save();
      ctx.fillStyle = 'rgba(0, 240, 255, 0.08)';
      ctx.strokeStyle = 'rgba(0, 240, 255, 0.4)';
      ctx.lineWidth = 1;

      ctx.beginPath();
      ctx.arc(pt.x, pt.y, radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
      ctx.restore();
    }

    // Satellite Icon & Ping Pulse
    function drawSatelliteMarker(ctx, sat, w, h, isSelected) {
      const pt = geoToCanvas(sat.lat, sat.lon, w, h);

      let color = "#00FF88"; // OK
      if (sat.status === "ADVISORY") color = "#FF9F1C";
      if (sat.status === "OFFLINE") color = "#FF4757";

      ctx.save();

      // Selection Glow Pulsing Ring
      if (isSelected) {
        const pulseRadius = 12 + Math.sin(Date.now() / 200) * 4;
        ctx.strokeStyle = color;
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, pulseRadius, 0, Math.PI * 2);
        ctx.stroke();

        // Target Crosshair
        ctx.strokeStyle = '#00F0FF88';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(pt.x - 16, pt.y); ctx.lineTo(pt.x + 16, pt.y);
        ctx.moveTo(pt.x, pt.y - 16); ctx.lineTo(pt.x, pt.y + 16);
        ctx.stroke();
      }

      // Satellite Core Point
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, isSelected ? 5 : 3.5, 0, Math.PI * 2);
      ctx.fill();

      // Satellite Label
      ctx.font = '10px Orbitron, monospace';
      ctx.fillStyle = isSelected ? '#FFFFFF' : '#94A3B8';
      ctx.fillText(sat.name, pt.x + 8, pt.y + 3);

      ctx.restore();
    }

    // --- RENDER SATELLITE SIDEBAR ROSTER ---
    function renderSatelliteList() {
      const listContainer = document.getElementById('satellite-list');
      listContainer.innerHTML = '';

      const searchVal = document.getElementById('sat-search').value.toLowerCase();

      const filtered = satelliteFleet.filter(sat => {
        const matchesFilter = (statusFilter === 'ALL' || sat.status === statusFilter);
        const matchesSearch = sat.name.toLowerCase().includes(searchVal) || sat.norad.includes(searchVal);
        return matchesFilter && matchesSearch;
      });

      document.getElementById('sat-count-badge').textContent = `${filtered.length} SATS`;

      filtered.forEach(sat => {
        const isSelected = sat.id === selectedSat.id;
        
        let statusBadgeClass = "bg-brand-green/20 text-brand-green border-brand-green/30";
        if (sat.status === "ADVISORY") statusBadgeClass = "bg-brand-amber/20 text-brand-amber border-brand-amber/30";
        if (sat.status === "OFFLINE") statusBadgeClass = "bg-brand-red/20 text-brand-red border-brand-red/30";

        const item = document.createElement('div');
        item.className = `p-2.5 px-3 cursor-pointer transition border-l-2 flex items-center justify-between ${
          isSelected 
            ? 'bg-brand-cyan/10 border-brand-cyan text-white font-bold' 
            : 'border-transparent text-slate-400 hover:bg-slate-900/80 hover:text-slate-200'
        }`;

        item.innerHTML = `
          <div class="flex items-center space-x-2.5">
            <i class="fa-solid fa-satellite text-xs ${isSelected ? 'text-brand-cyan' : 'text-slate-500'}"></i>
            <div>
              <div class="text-xs tracking-wide">${sat.name}</div>
              <div class="text-[10px] text-slate-500 font-normal">NORAD: ${sat.norad} • ${sat.type}</div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end">
            <span class="text-[9px] px-1.5 py-0.5 rounded border ${statusBadgeClass}">${sat.status}</span>
            <span class="text-[9px] text-slate-500 mt-1">${sat.alt} km</span>
          </div>
        `;

        item.onclick = () => {
          selectedSat = sat;
          updateDashboard();
          renderSatelliteList();
        };

        listContainer.appendChild(item);
      });
    }

    // --- CANVAS ANALOG GAUGES (3 Circular Dials like reference image) ---
    function drawGauge(canvasId, value, min, max, unit, warningThresh, dangerThresh, strokeColor) {
      const c = document.getElementById(canvasId);
      if (!c) return;
      const gctx = c.getContext('2d');
      const dpr = window.devicePixelRatio || 1;
      
      c.width = c.clientWidth * dpr;
      c.height = c.clientHeight * dpr;
      gctx.scale(dpr, dpr);

      const w = c.clientWidth;
      const h = c.clientHeight;
      const cx = w / 2;
      const cy = h / 2 + 5;
      const radius = Math.min(w, h) / 2 - 8;

      gctx.clearRect(0, 0, w, h);

      // Arc background track
      const startAngle = 0.8 * Math.PI;
      const endAngle = 2.2 * Math.PI;

      gctx.lineWidth = 6;
      gctx.strokeStyle = '#1E293B';
      gctx.beginPath();
      gctx.arc(cx, cy, radius, startAngle, endAngle);
      gctx.stroke();

      // Arc active value fill
      const pct = Math.min(Math.max((value - min) / (max - min), 0), 1);
      const valAngle = startAngle + (endAngle - startAngle) * pct;

      gctx.lineWidth = 6;
      gctx.strokeStyle = strokeColor;
      gctx.beginPath();
      gctx.arc(cx, cy, radius, startAngle, valAngle);
      gctx.stroke();

      // Tick marks
      for (let i = 0; i <= 10; i++) {
        const ang = startAngle + (endAngle - startAngle) * (i / 10);
        const innerR = radius - 8;
        const outerR = radius - 4;
        
        gctx.strokeStyle = '#475569';
        gctx.lineWidth = i % 5 === 0 ? 1.5 : 1;
        gctx.beginPath();
        gctx.moveTo(cx + Math.cos(ang) * innerR, cy + Math.sin(ang) * innerR);
        gctx.lineTo(cx + Math.cos(ang) * outerR, cy + Math.sin(ang) * outerR);
        gctx.stroke();
      }
    }

    function updateGauges() {
      // Battery / Voltage
      drawGauge('gauge-battery', selectedSat.battery, 0, 150, 'V', 100, 140, '#00FF88');
      document.getElementById('gauge-bat-val').textContent = selectedSat.battery.toFixed(1);

      // Temperature
      const tempColor = selectedSat.temp > 45 ? '#FF9F1C' : '#00F0FF';
      drawGauge('gauge-temp', selectedSat.temp, -20, 80, '°C', 40, 60, tempColor);
      document.getElementById('gauge-temp-val').textContent = selectedSat.temp.toFixed(1);

      // Gyro Drift
      const gyroColor = selectedSat.gyro > 0.5 ? '#FF4757' : '#FF9F1C';
      drawGauge('gauge-gyro', selectedSat.gyro, 0, 2.0, 'deg/s', 0.5, 1.2, gyroColor);
      document.getElementById('gauge-gyro-val').textContent = selectedSat.gyro.toFixed(2);
    }

    // --- CHART.JS TELEMETRY CHART INITIALIZATION ---
    let telemetryChart;
    const chartTimeLabels = [];
    const chartDataPoints = [];

    function initChart() {
      const ctxChart = document.getElementById('telemetry-chart').getContext('2d');
      
      // Pre-fill initial historical dummy points
      const now = new Date();
      for (let i = 15; i >= 0; i--) {
        const t = new Date(now.getTime() - i * 3000);
        chartTimeLabels.push(t.toLocaleTimeString('en-US', { hour12: false, minute:'2-digit', second:'2-digit' }));
        chartDataPoints.push(selectedSat.snr + (Math.random() * 4 - 2));
      }

      telemetryChart = new Chart(ctxChart, {
        type: 'line',
        data: {
          labels: chartTimeLabels,
          datasets: [{
            label: 'Downlink Signal (SNR dB)',
            data: chartDataPoints,
            borderColor: '#00F0FF',
            backgroundColor: 'rgba(0, 240, 255, 0.08)',
            borderWidth: 2,
            fill: true,
            tension: 0.3,
            pointRadius: 2,
            pointBackgroundColor: '#00F0FF'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            x: {
              grid: { color: 'rgba(30, 41, 59, 0.5)' },
              ticks: { color: '#64748B', font: { family: 'Orbitron', size: 9 } }
            },
            y: {
              grid: { color: 'rgba(30, 41, 59, 0.5)' },
              ticks: { color: '#64748B', font: { family: 'Orbitron', size: 9 } }
            }
          }
        }
      });
    }

    function pushTelemetryChartPoint(value) {
      if (!telemetryChart) return;

      const timeStr = new Date().toLocaleTimeString('en-US', { hour12: false, minute:'2-digit', second:'2-digit' });
      chartTimeLabels.push(timeStr);
      chartDataPoints.push(value);

      if (chartTimeLabels.length > 20) {
        chartTimeLabels.shift();
        chartDataPoints.shift();
      }

      telemetryChart.update('none'); // Update without full animation for performance
    }

    // --- LIVE EVENT & TELEMETRY LOG STREAM ---
    function addLogEntry(satName, msg, type = "INFO") {
      const stream = document.getElementById('telemetry-log-stream');
      const entry = document.createElement('div');
      
      const timeStr = new Date().toLocaleTimeString('en-US', { hour12: false, minute:'2-digit', second:'2-digit' });

      let badgeColor = "text-brand-cyan bg-brand-cyan/10 border-brand-cyan/20";
      if (type === "WARN") badgeColor = "text-brand-amber bg-brand-amber/10 border-brand-amber/20";
      if (type === "ALERT") badgeColor = "text-brand-red bg-brand-red/10 border-brand-red/20";

      entry.className = "p-1.5 bg-slate-950/60 rounded border border-slate-800/80 flex items-start space-x-2";
      entry.innerHTML = `
        <span class="text-[9px] text-slate-500 shrink-0 font-mono">${timeStr}</span>
        <span class="text-[9px] px-1 py-0.2 rounded border ${badgeColor} font-bold shrink-0">${type}</span>
        <span class="text-slate-300 truncate"><strong class="text-slate-100">${satName}:</strong> ${msg}</span>
      `;

      stream.prepend(entry);

      if (stream.children.length > 25) {
        stream.removeChild(stream.lastChild);
      }
    }

    // --- UPDATE ENTIRE DASHBOARD UI FOR SELECTED SATELLITE ---
    function updateDashboard() {
      // Header details
      document.getElementById('current-target-title').innerHTML = `
        <i class="fa-solid fa-crosshairs text-brand-cyan animate-spin" style="animation-duration: 8s;"></i>
        TARGET: ${selectedSat.name} [NORAD #${selectedSat.norad}]
      `;

      const pill = document.getElementById('target-status-pill');
      pill.textContent = `STATUS: ${selectedSat.status}`;
      if (selectedSat.status === "OK") pill.className = "text-[10px] px-2 py-0.5 rounded bg-brand-green/20 text-brand-green border border-brand-green/30";
      if (selectedSat.status === "ADVISORY") pill.className = "text-[10px] px-2 py-0.5 rounded bg-brand-amber/20 text-brand-amber border border-brand-amber/30";
      if (selectedSat.status === "OFFLINE") pill.className = "text-[10px] px-2 py-0.5 rounded bg-brand-red/20 text-brand-red border border-brand-red/30";

      // Coordinate readouts
      document.getElementById('map-lat').textContent = `${selectedSat.lat.toFixed(3)}° ${selectedSat.lat >= 0 ? 'N' : 'S'}`;
      document.getElementById('map-lon').textContent = `${Math.abs(selectedSat.lon).toFixed(3)}° ${selectedSat.lon >= 0 ? 'E' : 'W'}`;
      document.getElementById('map-alt').textContent = `${selectedSat.alt.toFixed(1)} km`;
      document.getElementById('map-vel').textContent = `${selectedSat.vel.toFixed(2)} km/s`;

      // Update Gauges
      updateGauges();

      // Update Modal Content
      document.getElementById('modal-title').textContent = selectedSat.name;
      document.getElementById('modal-norad').textContent = `NORAD ID: ${selectedSat.norad} | TYPE: ${selectedSat.type}`;
      document.getElementById('modal-orbit').textContent = selectedSat.type;
      document.getElementById('modal-inc').textContent = `${selectedSat.inc}°`;
      document.getElementById('modal-status').textContent = selectedSat.status;
      document.getElementById('modal-desc').textContent = selectedSat.desc;
    }

    // --- REAL-TIME SIMULATION TICKER LOOP ---
    function simulationStep() {
      if (!isStreamLive) return;

      // Update GMT Clock
      const now = new Date();
      document.getElementById('clock-gmt').textContent = now.toISOString().substring(11, 19) + " UTC";
      document.getElementById('clock-date').textContent = now.toISOString().substring(0, 10);

      // Orbital Physics Motion Simulation for Satellites
      satelliteFleet.forEach(sat => {
        // Move satellites gradually along longitude
        sat.lon += (sat.vel / 100);
        if (sat.lon > 180) sat.lon = -180;

        // Slight telemetry jitter for realistic live feel
        if (sat.status !== "OFFLINE") {
          sat.battery = Math.min(135, Math.max(90, sat.battery + (Math.random() - 0.5) * 0.4));
          sat.temp = Math.min(60, Math.max(15, sat.temp + (Math.random() - 0.5) * 0.2));
          sat.gyro = Math.max(0.01, sat.gyro + (Math.random() - 0.5) * 0.01);
          sat.snr = Math.min(50, Math.max(10, sat.snr + (Math.random() - 0.5) * 1.5));
        }
      });

      // Update Selected Sat Telemetry Chart Data
      const chartVal = activeMetric === 'SNR' ? selectedSat.snr : selectedSat.battery;
      pushTelemetryChartPoint(chartVal);

      // Random Event Stream Generator
      if (Math.random() < 0.25) {
        const randomSat = satelliteFleet[Math.floor(Math.random() * satelliteFleet.length)];
        const events = [
          { msg: "Downlink telemetry frame sync locked", type: "INFO" },
          { msg: "Solar array tracking angle adjusted +0.4°", type: "INFO" },
          { msg: "Pass over Madrid Ground Station initiated", type: "INFO" },
          { msg: "Transient thermal spike logged in sensor array", type: "WARN" },
          { msg: "Automated reaction wheel desaturation complete", type: "INFO" }
        ];
        const evt = events[Math.floor(Math.random() * events.length)];
        addLogEntry(randomSat.name, evt.msg, evt.type);
      }

      // Re-render UI & Map Canvas
      updateDashboard();
      drawWorldMap();
    }

    // --- INTERACTIVE EVENT LISTENERS & FILTERING ---
    document.querySelectorAll('.filter-tab').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.filter-tab').forEach(b => {
          b.className = "filter-tab flex-1 py-1 bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 rounded text-center";
        });
        e.target.className = "filter-tab flex-1 py-1 bg-brand-cyan/20 border border-brand-cyan text-brand-cyan rounded text-center";
        statusFilter = e.target.getAttribute('data-filter');
        renderSatelliteList();
      });
    });

    document.getElementById('sat-search').addEventListener('input', renderSatelliteList);

    // Live Stream Pause / Play Toggle
    const pauseBtn = document.getElementById('btn-pause-stream');
    pauseBtn.addEventListener('click', () => {
      isStreamLive = !isStreamLive;
      const icon = document.getElementById('pause-icon');
      const text = document.getElementById('pause-text');

      if (isStreamLive) {
        icon.className = "fa-solid fa-pause text-brand-cyan";
        text.textContent = "LIVE FEED";
        pauseBtn.classList.remove('border-brand-red');
      } else {
        icon.className = "fa-solid fa-play text-brand-amber";
        text.textContent = "PAUSED";
        pauseBtn.classList.add('border-brand-amber');
      }
    });

    // Clear Logs
    document.getElementById('btn-clear-logs').addEventListener('click', () => {
      document.getElementById('telemetry-log-stream').innerHTML = '';
    });

    // Chart Metric Toggles
    const btnSnr = document.getElementById('chart-toggle-snr');
    const btnPower = document.getElementById('chart-toggle-power');

    btnSnr.addEventListener('click', () => {
      activeMetric = 'SNR';
      btnSnr.className = "text-[10px] font-mono px-2 py-0.5 bg-brand-cyan/20 border border-brand-cyan text-brand-cyan rounded";
      btnPower.className = "text-[10px] font-mono px-2 py-0.5 bg-slate-900 border border-slate-800 text-slate-400 rounded";
      telemetryChart.data.datasets[0].label = 'Downlink Signal (SNR dB)';
      telemetryChart.data.datasets[0].borderColor = '#00F0FF';
      telemetryChart.data.datasets[0].backgroundColor = 'rgba(0, 240, 255, 0.08)';
    });

    btnPower.addEventListener('click', () => {
      activeMetric = 'POWER';
      btnPower.className = "text-[10px] font-mono px-2 py-0.5 bg-brand-cyan/20 border border-brand-cyan text-brand-cyan rounded";
      btnSnr.className = "text-[10px] font-mono px-2 py-0.5 bg-slate-900 border border-slate-800 text-slate-400 rounded";
      telemetryChart.data.datasets[0].label = 'Bus Voltage (V)';
      telemetryChart.data.datasets[0].borderColor = '#00FF88';
      telemetryChart.data.datasets[0].backgroundColor = 'rgba(0, 255, 136, 0.08)';
    });

    // Satellite Canvas Selection Click Event
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const clickY = e.clientY - rect.top;

      const w = canvas.width / (window.devicePixelRatio || 1);
      const h = canvas.height / (window.devicePixelRatio || 1);

      // Check if user clicked near any satellite point
      satelliteFleet.forEach(sat => {
        const pt = geoToCanvas(sat.lat, sat.lon, w, h);
        const dist = Math.hypot(clickX - pt.x, clickY - pt.y);
        if (dist < 18) {
          selectedSat = sat;
          updateDashboard();
          renderSatelliteList();
          openModal();
        }
      });
    });

    // Modal Details Controls
    const modal = document.getElementById('sat-modal');
    function openModal() { modal.classList.remove('hidden'); }
    function closeModal() { modal.classList.add('hidden'); }

    document.getElementById('btn-close-modal').addEventListener('click', closeModal);
    document.getElementById('btn-modal-close').addEventListener('click', closeModal);
    document.getElementById('btn-modal-track').addEventListener('click', () => {
      closeModal();
      updateDashboard();
    });

    document.getElementById('btn-toggle-footprint').addEventListener('click', () => {
      showFootprint = !showFootprint;
      drawWorldMap();
    });

    // Reset View Button
    document.getElementById('btn-reset-view').addEventListener('click', () => {
      selectedSat = satelliteFleet[0];
      updateDashboard();
      renderSatelliteList();
    });

    // --- INIT APP ON WINDOW LOAD ---
    window.onload = function() {
      renderSatelliteList();
      initChart();
      updateDashboard();
      drawWorldMap();

      // Start ticker loop
      setInterval(simulationStep, 1000);

      // Initial Log Messages
      addLogEntry("SYSTEM", "OrbitWatch Telemetry Engine initialized.", "INFO");
      addLogEntry("ISS (ZARYA)", "Telemetry stream connected via Madrid Station.", "INFO");
      addLogEntry("STARLINK-3021", "Attitude anomaly detected. Beacon active.", "ALERT");
    };
  </script>
</body>
</html>
