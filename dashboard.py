import streamlit as st
import streamlit.components.v1 as components

# Configure full-width layout
st.set_page_config(
    page_title="OrbitWatch | Telemetry & Tracking",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit chrome elements
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0rem !important; max-width: 100% !important;}
        body {background-color: #030712;}
        iframe {border: none !important; width: 100% !important;}
    </style>
""", unsafe_allow_html=True)

# Complete 3D Orbital Command Center HTML Content
HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OrbitWatch | Telemetry & Tracking</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        .font-mono { font-family: 'Share Tech Mono', monospace; }
        body { background-color: #030712; color: #94a3b8; margin: 0; padding: 8px; overflow-x: hidden; }
        .panel { background: rgba(11, 19, 38, 0.85); border: 1px solid #1e293b; border-radius: 8px; }
        .panel-glow { box-shadow: 0 0 15px rgba(6, 182, 212, 0.08); border: 1px solid #0f3759; }
        .grid-bg {
            background-image: linear-gradient(to right, rgba(15, 23, 42, 0.5) 1px, transparent 1px),
                              linear-gradient(to bottom, rgba(15, 23, 42, 0.5) 1px, transparent 1px);
            background-size: 24px 24px;
        }
        .sat-card { transition: all 0.2s ease; cursor: pointer; }
        .sat-card:hover, .sat-card.active { background: rgba(15, 23, 42, 0.9); border-color: #0284c7; }
        .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
    </style>
</head>
<body class="grid-bg flex flex-col gap-2">

    <header class="panel panel-glow px-4 py-2 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-3">
            <div class="p-2 bg-cyan-950/80 border border-cyan-500/40 rounded-lg text-cyan-400">
                <svg class="w-5 h-5 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path></svg>
            </div>
            <div>
                <div class="flex items-center gap-2">
                    <h1 class="font-bold font-mono text-cyan-400 tracking-wider text-base">ORBITWATCH</h1>
                    <span class="text-[10px] font-mono px-1.5 py-0.5 rounded border border-cyan-800 bg-cyan-950 text-cyan-300">// 3D ORBITAL COMMAND</span>
                </div>
                <p class="text-[11px] text-slate-400">GLOBAL REAL-TIME SATELLITE OPERATIONS & ANOMALY DETECTION</p>
            </div>
        </div>

        <div class="flex items-center gap-5">
            <div class="flex items-center gap-4 text-xs font-mono">
                <div class="flex items-center gap-1.5"><span class="status-dot bg-emerald-400"></span><span class="text-emerald-400 font-bold">145</span><span class="text-slate-400">NOMINAL</span></div>
                <div class="flex items-center gap-1.5"><span class="status-dot bg-amber-400"></span><span class="text-amber-400 font-bold">18</span><span class="text-slate-400">ADVISORY</span></div>
                <div class="flex items-center gap-1.5"><span class="status-dot bg-rose-500"></span><span class="text-rose-400 font-bold">19</span><span class="text-slate-400">OFFLINE</span></div>
            </div>

            <div class="h-6 w-px bg-slate-800"></div>

            <div class="text-right font-mono text-xs">
                <div id="utc-clock" class="text-cyan-300 font-bold text-xs">--:--:-- UTC</div>
                <div class="text-slate-500 text-[9px]" id="utc-date">2026-10-24</div>
            </div>

            <button onclick="toggleStream()" id="pause-btn" class="px-2.5 py-1 rounded bg-cyan-950 border border-cyan-700 text-cyan-300 font-mono text-[11px] hover:bg-cyan-900 transition flex items-center gap-1">
                <span>⏸</span> <span>LIVE FEED</span>
            </button>
        </div>
    </header>

    <div class="grid grid-cols-12 gap-2">
        <aside class="col-span-3 panel panel-glow p-2.5 flex flex-col gap-2.5" style="height: 610px;">
            <div class="flex items-center justify-between border-b border-slate-800 pb-1.5">
                <div class="flex items-center gap-1.5">
                    <svg class="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                    <span class="font-mono text-xs font-bold text-slate-200 uppercase tracking-wider">Active Satellites</span>
                </div>
                <span class="text-[10px] font-mono bg-slate-800 text-cyan-400 px-1.5 py-0.5 rounded">7 SATS</span>
            </div>

            <input type="text" id="sat-search" onkeyup="filterSats()" placeholder="Search target or NORAD ID..." class="w-full bg-slate-950 border border-slate-800 rounded px-2 py-1 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono">

            <div class="grid grid-cols-4 gap-1 text-[10px] font-mono">
                <button onclick="setFilter('ALL')" class="py-1 bg-cyan-950 text-cyan-400 border border-cyan-800 rounded text-center">ALL</button>
                <button onclick="setFilter('OK')" class="py-1 bg-slate-900 text-slate-400 border border-slate-800 rounded text-center hover:text-emerald-400">OK</button>
                <button onclick="setFilter('WARN')" class="py-1 bg-slate-900 text-slate-400 border border-slate-800 rounded text-center hover:text-amber-400">WARN</button>
                <button onclick="setFilter('OFF')" class="py-1 bg-slate-900 text-slate-400 border border-slate-800 rounded text-center hover:text-rose-400">OFF</button>
            </div>

            <div id="sat-list" class="flex-1 overflow-y-auto space-y-1 pr-1" style="max-height: 440px;"></div>

            <div class="border-t border-slate-800 pt-1.5 flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span>DOWNLINK: <span class="text-emerald-400">ACTIVE</span></span>
                <span>LATENCY: <span id="latency-val" class="text-cyan-400">18ms</span></span>
            </div>
        </aside>

        <main class="col-span-9 flex flex-col gap-2">
            <div class="panel panel-glow relative overflow-hidden flex flex-col" style="height: 415px;">
                <div class="absolute top-2.5 left-2.5 z-10 bg-slate-950/90 border border-slate-800 rounded px-2.5 py-1 flex items-center gap-3 text-[11px] font-mono">
                    <span class="text-cyan-400 font-bold flex items-center gap-1.5">
                        <span class="status-dot bg-cyan-400 animate-ping"></span>
                        TARGET: <span id="target-name">ISS (ZARYA) NORAD #25544</span>
                    </span>
                    <span class="text-slate-600">|</span>
                    <span class="text-slate-300">STATUS: <span id="target-status" class="text-emerald-400 font-bold">OK</span></span>
                    <span class="text-slate-600">|</span>
                    <span class="text-slate-300">ALT: <span id="target-alt" class="text-slate-200">418.4 km</span></span>
                    <span class="text-slate-300">VEL: <span id="target-vel" class="text-slate-200">7.66 km/s</span></span>
                </div>

                <canvas id="globeCanvas" width="980" height="415" class="w-full h-full block bg-[#020617] cursor-grab"></canvas>

                <div class="absolute bottom-2.5 left-2.5 z-10 bg-slate-950/80 border border-slate-800/80 rounded p-1.5 font-mono text-[9px] text-slate-400 pointer-events-none">
                    <div class="text-cyan-400 font-bold">3D ORBITAL ENGINE // REAL-TIME INCLINATION SIMULATOR</div>
                    <div>DRAG TO ROTATE GLOBE VIEW</div>
                </div>
            </div>

            <div class="grid grid-cols-12 gap-2" style="height: 185px;">
                <div class="col-span-5 panel panel-glow p-2 flex flex-col justify-between">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-1">
                        <span class="font-mono text-[11px] font-bold text-slate-200 uppercase flex items-center gap-1.5">
                            <span class="status-dot bg-cyan-400"></span> ANALOG GAUGES
                        </span>
                        <span class="text-[9px] font-mono text-emerald-400">● LIVE</span>
                    </div>

                    <div class="grid grid-cols-3 gap-1 text-center my-auto">
                        <div class="flex flex-col items-center">
                            <div class="relative w-14 h-14">
                                <canvas id="gaugePower" width="56" height="56"></canvas>
                                <div class="absolute inset-0 flex flex-col items-center justify-center">
                                    <span id="gauge-power-val" class="font-mono font-bold text-xs text-slate-100">4.2</span>
                                    <span class="text-[7px] text-slate-500 font-mono">kW</span>
                                </div>
                            </div>
                            <span class="text-[9px] font-mono text-slate-400 mt-0.5">POWER</span>
                        </div>

                        <div class="flex flex-col items-center">
                            <div class="relative w-14 h-14">
                                <canvas id="gaugeTemp" width="56" height="56"></canvas>
                                <div class="absolute inset-0 flex flex-col items-center justify-center">
                                    <span id="gauge-temp-val" class="font-mono font-bold text-xs text-slate-100">24</span>
                                    <span class="text-[7px] text-slate-500 font-mono">°C</span>
                                </div>
                            </div>
                            <span class="text-[9px] font-mono text-slate-400 mt-0.5">TEMP</span>
                        </div>

                        <div class="flex flex-col items-center">
                            <div class="relative w-14 h-14">
                                <canvas id="gaugeBat" width="56" height="56"></canvas>
                                <div class="absolute inset-0 flex flex-col items-center justify-center">
                                    <span id="gauge-bat-val" class="font-mono font-bold text-xs text-slate-100">92</span>
                                    <span class="text-[7px] text-slate-500 font-mono">%</span>
                                </div>
                            </div>
                            <span class="text-[9px] font-mono text-slate-400 mt-0.5">BATTERY</span>
                        </div>
                    </div>
                </div>

                <div class="col-span-7 panel panel-glow p-2 flex flex-col">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-1">
                        <span class="font-mono text-[11px] font-bold text-slate-200 uppercase flex items-center gap-1.5">
                            REAL-TIME TELEMETRY TIME-SERIES
                        </span>
                        <div class="flex gap-1">
                            <button onclick="switchChart('snr')" id="btn-snr" class="px-2 py-0.5 text-[9px] font-mono bg-cyan-950 border border-cyan-800 text-cyan-300 rounded">SNR</button>
                            <button onclick="switchChart('alt')" id="btn-alt" class="px-2 py-0.5 text-[9px] font-mono bg-slate-900 border border-slate-800 text-slate-400 rounded">ALT</button>
                        </div>
                    </div>
                    <div class="flex-1 min-h-0 pt-1 relative" style="height: 125px;">
                        <canvas id="telemetryChart"></canvas>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        const satData = [
            { id: 'ISS (ZARYA)', norad: '25544', status: 'OK', type: 'Space Station', alt: 418.4, inc: 51.6, speed: 7.66, color: '#34d399', angle: 0 },
            { id: 'HUBBLE ST', norad: '20580', status: 'OK', type: 'Telescope', alt: 535.1, inc: 28.5, speed: 7.50, color: '#38bdf8', angle: 1.2 },
            { id: 'SENTINEL-1A', norad: '39634', status: 'WARN', type: 'Sun-Sync', alt: 693.0, inc: 98.1, speed: 7.35, color: '#fbbf24', angle: 2.5 },
            { id: 'LANDSAT 9', norad: '49260', status: 'OK', type: 'Sun-Sync', alt: 705.2, inc: 98.2, speed: 7.34, color: '#34d399', angle: 3.8 },
            { id: 'NOAA-20 JPSS', norad: '43013', status: 'OK', type: 'Polar', alt: 824.6, inc: 98.7, speed: 7.42, color: '#34d399', angle: 4.5 },
            { id: 'STARLINK-3021', norad: '51240', status: 'OFF', type: 'LEO Const', alt: 540.0, inc: 53.0, speed: 7.55, color: '#f43f5e', angle: 5.2 },
            { id: 'GOES-16 (EAST)', norad: '41866', status: 'OK', type: 'Geostationary', alt: 35786.0, inc: 0.0, speed: 3.07, color: '#38bdf8', angle: 0.5 }
        ];

        let selectedSat = satData[0];
        let isStreaming = true;
        let activeFilter = 'ALL';

        function updateClock() {
            const now = new Date();
            document.getElementById('utc-clock').innerText = now.toISOString().substr(11, 8) + ' UTC';
            document.getElementById('utc-date').innerText = now.toISOString().substr(0, 10);
        }
        setInterval(updateClock, 1000);
        updateClock();

        function renderSatList() {
            const container = document.getElementById('sat-list');
            const search = document.getElementById('sat-search').value.toLowerCase();
            container.innerHTML = '';

            satData.filter(s => {
                const matchSearch = s.id.toLowerCase().includes(search) || s.norad.includes(search);
                const matchFilter = activeFilter === 'ALL' || 
                                   (activeFilter === 'OK' && s.status === 'OK') ||
                                   (activeFilter === 'WARN' && s.status === 'WARN') ||
                                   (activeFilter === 'OFF' && s.status === 'OFF');
                return matchSearch && matchFilter;
            }).forEach(s => {
                const badgeColor = s.status === 'OK' ? 'bg-emerald-950 text-emerald-400 border-emerald-800' :
                                 s.status === 'WARN' ? 'bg-amber-950 text-amber-400 border-amber-800' :
                                 'bg-rose-950 text-rose-400 border-rose-800';
                
                const card = document.createElement('div');
                card.className = `sat-card panel p-2 flex items-center justify-between border ${s.id === selectedSat.id ? 'active' : ''}`;
                card.onclick = () => selectSat(s);
                card.innerHTML = `
                    <div>
                        <div class="font-mono text-xs font-bold text-slate-100">${s.id}</div>
                        <div class="text-[9px] text-slate-500 font-mono">NORAD: ${s.norad} · ${s.type}</div>
                    </div>
                    <div class="text-right">
                        <span class="text-[8px] font-mono px-1.5 py-0.5 rounded border ${badgeColor}">${s.status === 'WARN' ? 'ADVISORY' : s.status === 'OFF' ? 'OFFLINE' : 'OK'}</span>
                        <div class="text-[9px] text-slate-400 font-mono mt-1">${s.alt} km</div>
                    </div>
                `;
                container.appendChild(card);
            });
        }

        function selectSat(s) {
            selectedSat = s;
            document.getElementById('target-name').innerText = `${s.id} NORAD #${s.norad}`;
            document.getElementById('target-status').innerText = s.status === 'WARN' ? 'ADVISORY' : s.status === 'OFF' ? 'OFFLINE' : 'OK';
            document.getElementById('target-status').className = s.status === 'OK' ? 'text-emerald-400 font-bold' : s.status === 'WARN' ? 'text-amber-400 font-bold' : 'text-rose-500 font-bold';
            document.getElementById('target-alt').innerText = `${s.alt} km`;
            document.getElementById('target-vel').innerText = `${s.speed} km/s`;
            renderSatList();
        }

        function setFilter(f) { activeFilter = f; renderSatList(); }
        function filterSats() { renderSatList(); }
        renderSatList();

        const canvas = document.getElementById('globeCanvas');
        const ctx = canvas.getContext('2d');
        let globeRotation = 0;
        let isDragging = false;
        let lastMouseX = 0;

        canvas.addEventListener('mousedown', e => { isDragging = true; lastMouseX = e.clientX; });
        window.addEventListener('mouseup', () => { isDragging = false; });
        canvas.addEventListener('mousemove', e => {
            if(!isDragging) return;
            const delta = e.clientX - lastMouseX;
            globeRotation += delta * 0.008;
            lastMouseX = e.clientX;
        });

        function draw3DGlobe() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const cx = canvas.width / 2;
            const cy = canvas.height / 2;
            const radius = 110;

            ctx.fillStyle = '#0f172a';
            for(let i=0; i<40; i++) {
                let sx = (i * 93) % canvas.width;
                let sy = (i * 47) % canvas.height;
                ctx.fillRect(sx, sy, 1.5, 1.5);
            }

            let gradient = ctx.createRadialGradient(cx, cy, radius * 0.9, cx, cy, radius * 1.3);
            gradient.addColorStop(0, 'rgba(6, 182, 212, 0.25)');
            gradient.addColorStop(1, 'rgba(3, 7, 18, 0)');
            ctx.fillStyle = gradient;
            ctx.beginPath(); ctx.arc(cx, cy, radius * 1.3, 0, Math.PI * 2); ctx.fill();

            ctx.fillStyle = '#081c36';
            ctx.beginPath(); ctx.arc(cx, cy, radius, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#0284c7'; ctx.lineWidth = 1.5; ctx.stroke();

            ctx.strokeStyle = 'rgba(56, 189, 248, 0.25)';
            ctx.lineWidth = 0.75;
            for(let i = -2; i <= 2; i++) {
                let latOffset = i * 35;
                ctx.beginPath();
                ctx.ellipse(cx, cy + latOffset, radius * Math.cos(latOffset/radius), radius * 0.2, 0, 0, Math.PI * 2);
                ctx.stroke();
            }
            for(let i = 0; i < 6; i++) {
                let angle = globeRotation + (i * Math.PI / 3);
                ctx.beginPath();
                ctx.ellipse(cx + Math.sin(angle)*radius*0.3, cy, radius * Math.abs(Math.cos(angle)), radius, 0, 0, Math.PI * 2);
                ctx.stroke();
            }

            satData.forEach(s => {
                s.angle += 0.012 * (8.0 / Math.sqrt(s.alt));
                
                let incRad = s.inc * (Math.PI / 180);
                let orbitRadius = radius + (s.alt > 10000 ? 55 : 35);
                
                let x3d = orbitRadius * Math.cos(s.angle);
                let y3d = orbitRadius * Math.sin(s.angle) * Math.cos(incRad);
                let z3d = orbitRadius * Math.sin(s.angle) * Math.sin(incRad);

                let rotX = x3d * Math.cos(globeRotation) - z3d * Math.sin(globeRotation);
                let rotZ = x3d * Math.sin(globeRotation) + z3d * Math.cos(globeRotation);

                let screenX = cx + rotX;
                let screenY = cy + y3d;

                ctx.beginPath();
                ctx.strokeStyle = s.id === selectedSat.id ? 'rgba(56, 189, 248, 0.8)' : 'rgba(30, 58, 138, 0.4)';
                ctx.lineWidth = s.id === selectedSat.id ? 1.5 : 0.75;
                
                for(let a = 0; a < Math.PI * 2; a += 0.1) {
                    let tx = orbitRadius * Math.cos(a);
                    let ty = orbitRadius * Math.sin(a) * Math.cos(incRad);
                    let tz = orbitRadius * Math.sin(a) * Math.sin(incRad);
                    let trx = tx * Math.cos(globeRotation) - tz * Math.sin(globeRotation);
                    let trz = tx * Math.sin(globeRotation) + tz * Math.cos(globeRotation);
                    
                    let px = cx + trx;
                    let py = cy + ty;
                    if(a === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
                }
                ctx.stroke();

                let isFront = rotZ > -20;
                if(isFront || s.id === selectedSat.id) {
                    if(s.id === selectedSat.id) {
                        ctx.beginPath();
                        ctx.arc(screenX, screenY, 14, 0, Math.PI * 2);
                        ctx.strokeStyle = '#38bdf8';
                        ctx.lineWidth = 1.5;
                        ctx.stroke();
                    }

                    ctx.beginPath();
                    ctx.arc(screenX, screenY, 4, 0, Math.PI * 2);
                    ctx.fillStyle = s.color;
                    ctx.fill();

                    ctx.fillStyle = '#cbd5e1';
                    ctx.font = '10px Share Tech Mono';
                    ctx.fillText(s.id, screenX + 8, screenY + 3);
                }
            });

            if (isStreaming) globeRotation += 0.003;
            requestAnimationFrame(draw3DGlobe);
        }
        draw3DGlobe();

        function drawGauge(canvasId, val, max, color) {
            const gCanvas = document.getElementById(canvasId);
            if(!gCanvas) return;
            const gCtx = gCanvas.getContext('2d');
            const cx = 28, cy = 28, radius = 21;
            gCtx.clearRect(0, 0, 56, 56);

            gCtx.beginPath();
            gCtx.arc(cx, cy, radius, 0.75 * Math.PI, 2.25 * Math.PI);
            gCtx.strokeStyle = '#1e293b';
            gCtx.lineWidth = 5;
            gCtx.lineCap = 'round';
            gCtx.stroke();

            const pct = Math.min(val / max, 1);
            const endAngle = 0.75 * Math.PI + (pct * 1.5 * Math.PI);
            gCtx.beginPath();
            gCtx.arc(cx, cy, radius, 0.75 * Math.PI, endAngle);
            gCtx.strokeStyle = color;
            gCtx.lineWidth = 5;
            gCtx.lineCap = 'round';
            gCtx.stroke();
        }

        drawGauge('gaugePower', 4.2, 5.0, '#38bdf8');
        drawGauge('gaugeTemp', 24.5, 50.0, '#34d399');
        drawGauge('gaugeBat', 92, 100.0, '#818cf8');

        const chartCtx = document.getElementById('telemetryChart').getContext('2d');
        const telemetryChart = new Chart(chartCtx, {
            type: 'line',
            data: {
                labels: Array.from({length: 20}, (_, i) => `${i}s ago`).reverse(),
                datasets: [{
                    label: 'SNR Signal (dB)',
                    data: [15.2, 15.4, 15.1, 15.8, 16.0, 15.9, 16.2, 16.5, 16.1, 15.8, 15.7, 16.3, 16.4, 16.8, 17.0, 16.9, 17.2, 17.1, 17.4, 17.5],
                    borderColor: '#38bdf8',
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { color: '#0f172a' }, ticks: { color: '#64748b', font: { size: 9, family: 'Share Tech Mono' } } },
                    y: { grid: { color: '#0f172a' }, ticks: { color: '#64748b', font: { size: 9, family: 'Share Tech Mono' } } }
                }
            }
        });

        setInterval(() => {
            if(!isStreaming) return;
            const pow = (4.0 + Math.random() * 0.4).toFixed(1);
            const temp = Math.round(23 + Math.random() * 3);
            document.getElementById('gauge-power-val').innerText = pow;
            document.getElementById('gauge-temp-val').innerText = temp;
            drawGauge('gaugePower', pow, 5.0, '#38bdf8');
            drawGauge('gaugeTemp', temp, 50.0, '#34d399');

            const lastData = telemetryChart.data.datasets[0].data;
            lastData.shift();
            lastData.push(+(15.5 + Math.random() * 2.2).toFixed(1));
            telemetryChart.update('none');
            document.getElementById('latency-val').innerText = `${Math.floor(14 + Math.random() * 8)}ms`;
        }, 1500);

        function toggleStream() {
            isStreaming = !isStreaming;
            document.getElementById('pause-btn').innerHTML = isStreaming ? '<span>⏸</span> <span>LIVE FEED</span>' : '<span>▶</span> <span>PAUSED</span>';
        }

        function switchChart(type) {
            if(type === 'snr') {
                telemetryChart.data.datasets[0].label = 'SNR Signal (dB)';
                telemetryChart.data.datasets[0].borderColor = '#38bdf8';
                document.getElementById('btn-snr').className = 'px-2 py-0.5 text-[9px] font-mono bg-cyan-950 border border-cyan-800 text-cyan-300 rounded';
                document.getElementById('btn-alt').className = 'px-2 py-0.5 text-[9px] font-mono bg-slate-900 border border-slate-800 text-slate-400 rounded';
            } else {
                telemetryChart.data.datasets[0].label = 'Altitude (km)';
                telemetryChart.data.datasets[0].borderColor = '#a855f7';
                document.getElementById('btn-alt').className = 'px-2 py-0.5 text-[9px] font-mono bg-purple-950 border border-purple-800 text-purple-300 rounded';
                document.getElementById('btn-snr').className = 'px-2 py-0.5 text-[9px] font-mono bg-slate-900 border border-slate-800 text-slate-400 rounded';
            }
            telemetryChart.update();
        }
    </script>
</body>
</html>
'''

# Render inside Streamlit component iframe
components.html(HTML_CONTENT, height=660, scrolling=False)
