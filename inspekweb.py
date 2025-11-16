#!/usr/bin/env python3
"""
inspekweb.py - Versi dengan perilaku pengguna dan fingerprint palsu yang diperluas
Usage:
    python3 inspekweb.py <url> <jumlah> <delay_seconds>

Contoh:
    python3 inspekweb.py https://example.com 3 10
"""
import sys
import asyncio
import json
import random
import time
from pathlib import Path
from playwright.async_api import async_playwright

# -----------------------
# Konfigurasi Sederhana & Data Palsu
# -----------------------

# PENTING: Untuk Fake IP (Proxy), isi list proxies ini.
proxies = [
    # "http://proxy1.example:8080",
    # "http://proxy2.example:8080",
    # ... Tambahkan hingga 30 proxy hidup di sini
]

# Output file
OUTFILE = Path("results.json")

# 1. Random user agents (30+ yang lebih beragam)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 15_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.7 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 9S) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/115.0.1901.188",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; CrOS x86_64 15329.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
]

VIEWPORTS = [
    {"width": 360, "height": 800},
    {"width": 375, "height": 812},
    {"width": 393, "height": 851},
    {"width": 412, "height": 915},
    {"width": 1280, "height": 720},
    {"width": 1920, "height": 1080},
    {"width": 1440, "height": 900},
]

# Data Fake Connection/ISP
CONNECTION_TYPES = ["wifi", "cellular", "4g", "3g"]
EFFECTIVE_TYPES = ["4g", "3g", "2g"]

# Data Fake WebGL (GPU)
FAKE_WEBGL_RENDERERS = [
    "ANGLE (NVIDIA GeForce RTX 3060)",
    "ANGLE (NVIDIA GeForce RTX 4090)",
    "ANGLE (NVIDIA GeForce RTX 5090)",
    "Google SwiftShader",
    "AMD Radeon Graphics",
    "Intel(R) UHD Graphics 620",
    "Apple A12 Bionic GPU",
]

# Data Fake Hardware (Spesifikasi Baru)
FAKE_CPU_CORES = 9000000000000
FAKE_RAM_GB = 9999999999999999999.0 # Dalam GB

# -----------------------
# Utils
# -----------------------
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def choose_proxy(i):
    if not proxies:
        return None
    return proxies[i % len(proxies)]

# -----------------------
# Core: single visit
# -----------------------
async def run_visit(playwright, url, idx, delay, proxy=None):
    browser_args = ["--no-sandbox", "--disable-setuid-sandbox"]
    
    # Mode Headless diaktifkan
    launch_opts = {"headless": True, "args": browser_args} 
    
    if proxy:
        launch_opts["proxy"] = {"server": proxy}

    browser = await playwright.chromium.launch(**launch_opts)
    ua = random.choice(USER_AGENTS)
    viewport = random.choice(VIEWPORTS)
    
    # Data Palsu yang akan diinjeksikan
    fake_battery_level = round(random.uniform(0.01, 1.00), 2)
    fake_charging = random.choice([True, False])
    fake_connection_type = random.choice(CONNECTION_TYPES)
    fake_effective_type = random.choice(EFFECTIVE_TYPES)
    fake_downlink = round(random.uniform(0.5, 10.0), 1)
    fake_rtt = random.choice([50, 100, 150, 200])
    fake_webgl_renderer = random.choice(FAKE_WEBGL_RENDERERS)

    # Context harus dibuat dulu sebelum init_script
    context = await browser.new_context(user_agent=ua, viewport=viewport)
    
    # ----------------------------------------------------
    # 🛠️ INJEKSI DATA FAKE (SPOOFING)
    # ----------------------------------------------------
    
    # 1. Fake Baterai
    await context.add_init_script(f"""
        const batteryLevel = {fake_battery_level};
        const batteryCharging = {fake_charging};
        
        if (navigator.getBattery === undefined) {{
            navigator.getBattery = () => Promise.resolve({{
                level: batteryLevel,
                charging: batteryCharging,
                chargingTime: Infinity,
                dischargingTime: Infinity
            }});
        }}
    """)
    
    # 2. Fake Koneksi/ISP
    await context.add_init_script(f"""
        const connectionType = '{fake_connection_type}';
        const effectiveType = '{fake_effective_type}';
        const downlink = {fake_downlink};
        const rtt = {fake_rtt};
        
        Object.defineProperty(navigator, 'connection', {{
            get: () => ({{
                type: connectionType,
                effectiveType: effectiveType,
                downlink: downlink,
                rtt: rtt,
                saveData: false
            }})
        }});
    """)

    # 3. Fake WebGL Renderer (GPU)
    await context.add_init_script(f"""
        const fakeRenderer = '{fake_webgl_renderer}';

        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {{
            if (parameter === 37446) {{ // UNMASKED_RENDERER_WEBGL
                return fakeRenderer;
            }}
            if (parameter === 37445) {{ // UNMASKED_VENDOR_WEBGL
                return 'Google Inc.';
            }}
            return getParameter.apply(this, arguments);
        }};
    """)

    # 4. Fake Plugins/MimeTypes
    await context.add_init_script("""
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format'},
                {name: 'Chromium PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai', description: 'Portable Document Format'}
            ],
        });
        Object.defineProperty(navigator, 'mimeTypes', {
            get: () => [
                {type: 'application/pdf', suffixes: 'pdf', description: 'Portable Document Format'}
            ],
        });
    """)
    
    # 5. FAKE HARDWARE (CPU Cores & RAM)
    await context.add_init_script(f"""
        const fakeCores = {FAKE_CPU_CORES};
        const fakeRAM = {FAKE_RAM_GB};

        // Spoof navigator.hardwareConcurrency (CPU Cores)
        Object.defineProperty(navigator, 'hardwareConcurrency', {{
            get: () => fakeCores
        }});

        // Spoof navigator.deviceMemory (RAM, dalam GB)
        Object.defineProperty(navigator, 'deviceMemory', {{
            get: () => fakeRAM
        }});
    """)

    page = await context.new_page()

    result = {"visit": idx, "timestamp": now(), "url": url, "proxy": proxy or None, "userAgent": ua, "viewport": viewport}
    # Simpan data yang diinjeksikan untuk logging
    result["fake_data_injected"] = {
        "cpu_cores": FAKE_CPU_CORES,
        "ram_gb": FAKE_RAM_GB,
        "battery": fake_battery_level, 
        "charging": fake_charging, 
        "connection_type": fake_connection_type,
        "webgl_renderer": fake_webgl_renderer
    }

    try:
        print(f"[{idx}] 🌐 Mengunjungi {url} (UA: {ua.split(')')[0]}...)")
        print(f"[{idx}] ⚙️ Hardware Palsu: CPU={FAKE_CPU_CORES} Core, RAM={int(FAKE_RAM_GB)} GB")
        print(f"[{idx}] 🔋 Baterai Palsu: {int(fake_battery_level*100)}% ({'Charging' if fake_charging else 'Not Charging'})")
        print(f"[{idx}] 📶 Koneksi Palsu: {fake_connection_type}/{fake_effective_type}")
        print(f"[{idx}] 🖼️ GPU Palsu: {fake_webgl_renderer}")
        
        await page.goto(url, timeout=30000)
        
        # ------------------------------------------------
        # 🤖 Simulasi Perilaku Manusia (Scroll & Hover)
        # ------------------------------------------------
        
        random_wait_on_load = random.uniform(2.0, 5.0) 
        await page.wait_for_timeout(int(random_wait_on_load * 1000))
        
        scroll_count = random.randint(1, 3)
        total_scroll_time = 0
        for _ in range(scroll_count):
            scroll_distance = random.randint(500, 2000)
            scroll_duration = random.uniform(1.0, 3.0)
            await page.mouse.wheel(0, scroll_distance)
            await page.wait_for_timeout(int(scroll_duration * 1000))
            total_scroll_time += scroll_duration
            
        print(f"[{idx}] 🔄 Selesai scroll dalam {total_scroll_time:.2f}s.")
        
        try:
            elements = await page.locator('a[href], button').all()
            if elements:
                random_element = random.choice(elements)
                await random_element.scroll_into_view_if_needed()
                box = await random_element.bounding_box()
                if box:
                    x = box['x'] + box['width'] * random.uniform(0.1, 0.9)
                    y = box['y'] + box['height'] * random.uniform(0.1, 0.9)
                    await page.mouse.move(x, y)
                    await page.wait_for_timeout(random.randint(500, 1500))
                    print(f"[{idx}] 🖱️ Melakukan gerakan mouse (hover) pada elemen.")
            
        except Exception:
            pass
            
        final_wait = random.uniform(1.0, 4.0)
        await page.wait_for_timeout(int(final_wait * 1000))
        
        # ------------------------------------------------
        # 📝 Pengambilan Data (Fingerprinting)
        # ------------------------------------------------

        info = await page.evaluate("""async () => {
            const out = {};
            try {
                // Data standar (sebagian besar akan mengambil nilai palsu)
                out.userAgent = navigator.userAgent || null;
                out.platform = navigator.platform || null;
                out.language = navigator.language || null;
                out.languages = navigator.languages || null;
                out.onLine = navigator.onLine;
                out.vendor = navigator.vendor || null;
                // Hardware palsu akan diambil dari sini
                out.hardwareConcurrency = navigator.hardwareConcurrency || null;
                out.deviceMemory = navigator.deviceMemory || null;
                out.maxTouchPoints = navigator.maxTouchPoints || null;
                out.screen = { width: screen.width, height: screen.height, colorDepth: screen.colorDepth, pixelDepth: screen.pixelDepth, availWidth: screen.availWidth, availHeight: screen.availHeight };
                out.windowSize = { innerWidth: window.innerWidth, innerHeight: window.innerHeight, outerWidth: window.outerWidth, outerHeight: window.outerHeight };
                out.referrer = document.referrer || null;
                out.location = { href: location.href, origin: location.origin };
                // connection (sudah dipalsukan)
                try {
                    const c = navigator.connection || {};
                    out.connection = { type: c.type || null, downlink: c.downlink || null, rtt: c.rtt || null, effectiveType: c.effectiveType || null, saveData: c.saveData || null};
                } catch(e) { out.connection = null; }
                // battery (sudah dipalsukan)
                try {
                    if (navigator.getBattery) {
                        const b = await navigator.getBattery();
                        out.battery = { level: b.level, charging: b.charging, chargingTime: b.chargingTime, dischargingTime: b.dischargingTime };
                    } else out.battery = null;
                } catch(e){ out.battery = null; }
                // plugins/mime types (sudah dipalsukan)
                try { out.plugins = navigator.plugins ? Array.from(navigator.plugins).map(p => ({name:p.name, filename:p.filename, description:p.description})) : null } catch(e){ out.plugins = null }
                try { out.mimeTypes = navigator.mimeTypes ? Array.from(navigator.mimeTypes).map(m => ({type: m.type, description: m.description})) : null } catch(e){ out.mimeTypes = null }
                // WebGL renderer (sudah dipalsukan)
                try {
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                    out.webglRenderer = gl ? gl.getParameter(gl.RENDERER) : null;
                } catch(e) { out.webglRenderer = "error"; }
            } catch (err) {
                out._error = String(err);
            }
            return out;
        }""")
        result["data"] = info

        try:
            content = await page.content()
            result["content_snippet"] = content[:20000]
        except:
            result["content_snippet"] = None

        print(f"[{idx}] ✅ done - {now()}")
    except Exception as e:
        result["error"] = str(e)
        print(f"[{idx}] ❌ error - {e}")
    finally:
        try:
            await context.close()
        except: pass
        try:
            await browser.close()
        except: pass

    await asyncio.sleep(delay)
    return result

# -----------------------
# Main
# -----------------------
async def main(url, jumlah, delay):
    results = []
    print(f"⚙️ Memulai inspeksi ke: {url}")
    print(f"• Visits: {jumlah}")
    print(f"• Delay tiap visit: {delay}s")
    if proxies:
        print(f"• **Menggunakan {len(proxies)} Proxy (Fake IP) yang bergantian**")
    else:
        print(f"• **PERINGATAN: Tidak ada Proxy/Fake IP yang digunakan. IP kamu akan terdeteksi sama!**")

    async with async_playwright() as p:
        for i in range(1, jumlah + 1):
            proxy = choose_proxy(i-1)
            r = await run_visit(p, url, i, delay, proxy=proxy)
            results.append(r)
            
            if "error" in r:
                print(f"  → Visit {i}: ERROR: {r['error']}")
            else:
                cpu = r.get("fake_data_injected", {}).get("cpu_cores")
                ram = r.get("fake_data_injected", {}).get("ram_gb")
                renderer = r.get("fake_data_injected", {}).get("webgl_renderer")
                print(f"  → Visit {i}: UA='{r.get('userAgent')[:60]}...' CPU={cpu} RAM={int(ram)}GB GPU='{renderer}'")

    OUTFILE.write_text(json.dumps({"meta": {"url": url, "visits": jumlah, "delay": delay, "timestamp": now()}, "results": results}, indent=2, ensure_ascii=False))
    print(f"\n✅ Selesai. Hasil disimpan di {OUTFILE.resolve()}")

# -----------------------
# CLI
# -----------------------
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 inspekweb.py <url> <jumlah> <delay_seconds>")
        sys.exit(1)
    url = sys.argv[1]
    try:
        jumlah = int(sys.argv[2])
        delay = float(sys.argv[3])
    except:
        print("Jumlah harus integer, delay harus number (detik).")
        sys.exit(1)
    asyncio.run(main(url, jumlah, delay))