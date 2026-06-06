import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from datetime import datetime
import streamlit.components.v1 as components

# ini berfungsi agar halaman streamlit rapi ke bawah (centered)
st.set_page_config(
    page_title="SADAM - Monitoring Merapi",
    layout="centered"
)

# Mengambil data dari MAGMA (kita mengambil data realtime dari website magma.esdm.go.id)
def ambil_data_merapi():
    url = "https://magma.esdm.go.id/v1/gunung-api/laporan"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'lxml')

        cards = soup.find_all(['div', 'article'], class_=['card', 'card-body', 'col-md-6'])

        for card in cards:
            card_text = card.get_text()
            if "Merapi" in card_text:
                status_tag = card.find('span', class_='badge')
                status = status_tag.text.strip() if status_tag else "Data Tidak Ditemukan"

                visual = "Teramati asap kawah utama berwarna putih dengan intensitas tipis hingga tebal."
                p_tags = card.find_all('p')
                for p in p_tags:
                    if "visual" in p.text.lower() or "asap" in p.text.lower():
                        visual = p.text.strip()
                        break

                return {
                    "status": status,
                    "visual": visual,
                    "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                }

        return {
            "status": "Data Tidak Ditemukan",
            "visual": "Gagal sinkronisasi dengan website MAGMA. Silakan cek koneksi atau struktur web.",
            "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }

    except Exception as e:
        return {
            "status": "Error Koneksi",
            "visual": f"Terjadi kesalahan teknis: {str(e)}",
            "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        
# Import data yang sudah diambil dari magma.esdm.go.id
data = ambil_data_merapi()

# Set up data youtube live gunung merapi
video_id = "8X7gHBhD1Tw"
youtube_url = f"https://www.youtube.com/watch?v={video_id}"
thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

# Membuat Peta Folium Lokasi Gunung Merapi
m = folium.Map(location=[-7.54, 110.44], zoom_start=12, scrollWheelZoom=False)
folium.Marker(
    [-7.54, 110.44],
    popup="Gunung Merapi",
    icon=folium.Icon(color='red', icon='fire')
).add_to(m)

# Mengonversi peta ke HTML string
map_html = m._repr_html_()

# Dashbord Layout (HTML + CSS)
dashboard_html = f"""
<div style="background-color:#f0f2f6; padding:30px; border-radius:15px; font-family:sans-serif; max-width:800px; margin:auto; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">

    <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color:white; padding:25px; border-radius:12px; margin-bottom:20px; text-align:center;">
        <h1 style="margin:0; font-size:28px; letter-spacing:1px; font-weight:bold;">🌋 SADAM</h1>
        <p style="margin:5px 0 0; opacity:0.9; font-weight:300;">Monitoring Merapi Real-Time • PVMBG (MAGMA Indonesia)</p>
    </div>

    <div style="background-color:#ffffff; padding:20px; border-radius:10px; margin-bottom:20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
        <h4 style="margin:0 0 10px 0; color:#1e3a8a; font-weight:bold; display:flex; align-items:center;">
            <span style="margin-right:14px;">⛰️</span> Mengenal Gunung Merapi
        </h4>
        <p style="font-size:14px; color:#334155; line-height:1.6; margin:0; text-align:justify;">
            Gunung Merapi adalah salah satu gunung api paling aktif di dunia yang terletak di perbatasan Provinsi Jawa Tengah dan Daerah Istimewa Yogyakarta. Secara geologis, Merapi merupakan gunung api bertipe <b>stratovulkano</b> yang dikenal dengan karakteristik letusan efusif maupun eksplosif, serta seringnya terbentuk kubah lava yang berpotensi menghasilkan awan panas (wedhus gembel). Pemantauan secara real-time sangat krusial mengingat letaknya yang berdekatan dengan kawasan padat penduduk.
        </p>
    </div>

    <table style="width:100%; background-color:white; border-collapse: separate; border-spacing: 0; border-radius:10px; overflow:hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
        <thead>
            <tr style="background-color:#e2e8f0; color:#1e3a8a;">
                <th style="padding:15px; border-bottom:2px solid #cbd5e1; text-align:left; font-size:14px; font-weight:bold;">WAKTU UPDATE</th>
                <th style="padding:15px; border-bottom:2px solid #cbd5e1; text-align:center; font-size:14px; font-weight:bold;">STATUS AKTIVITAS</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style="padding:20px; color:#475569; font-size:16px;">{data['waktu']}</td>
                <td style="padding:20px; text-align:center;">
                    <span style="background-color:#dbeafe; color:#1e40af; padding:8px 16px; border-radius:20px; font-weight:bold; font-size:14px; border: 1px solid #bfdbfe;">
                        {data['status']}
                    </span>
                </td>
            </tr>
        </tbody>
    </table>

    <div style="margin-top:20px; background-color:#ffffff; padding:20px; border-left:5px solid #3b82f6; border-radius:8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
        <h4 style="margin:0 0 10px 0; color:#1e3a8a; display:flex; align-items:center; font-weight:bold;">
            <span style="margin-right:10px;">🔍</span> Keterangan Visual
        </h4>
        <p style="font-size:15px; color:#334155; line-height:1.6; margin:0;">{data['visual']}</p>
    </div>

    <div style="margin-top:25px;">
        <h4 style="color:#1e3a8a; font-size:18px; margin-bottom:12px; display:flex; align-items:center; font-weight:bold;">
            <span style="margin-right:10px;">🛡️</span> Protokol Mitigasi & Keselamatan
        </h4>
        <table style="width:100%; background-color:white; border-collapse: separate; border-spacing: 0; border-radius:12px; overflow:hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">
            <thead>
                <tr style="background-color:#1e3a8a; color:white;">
                    <th style="padding:12px; text-align:left; font-size:13px; width:30%; font-weight:bold;">TINGKAT RISIKO</th>
                    <th style="padding:12px; text-align:left; font-size:13px; font-weight:bold;">TINDAKAN REKOMENDASI</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color:#fff5f5;">
                    <td style="padding:12px; border-bottom:1px solid #fecaca; font-weight:bold; color:#c53030;">AWAS (Level IV)</td>
                    <td style="padding:12px; border-bottom:1px solid #fecaca; color:#742a2a; font-size:13px;">Erupsi sedang berlangsung atau akan segera terjadi dengan potensi bahaya besar. Evakuasi wajib dilakukan di zona terdampak dan seluruh aktivitas di area rawan dihentikan.</td>
                </tr>
                <tr style="background-color:#fffaf0;">
                    <td style="padding:12px; border-bottom:1px solid #feebc8; font-weight:bold; color:#c05621;">SIAGA (Level III)</td>
                    <td style="padding:12px; border-bottom:1px solid #feebc8; color:#7b341e; font-size:13px;">Aktivitas gunungapi meningkat signifikan dan berpotensi terjadi erupsi. Evakuasi sebagian wilayah rawan dapat mulai dilakukan. Masyarakat harus mengikuti arahan resmi dan menjauhi kawasan berbahaya.</td>
                </tr>
                <tr style="background-color:#f0fff4;">
                    <td style="padding:12px; border-bottom:1px solid #c6f6d5; font-weight:bold; color:#2f855a;">WASPADA (Level II)</td>
                    <td style="padding:12px; border-bottom:1px solid #c6f6d5; color:#22543d; font-size:13px;">Terjadi peningkatan aktivitas vulkanik di atas kondisi normal, seperti gempa vulkanik, kenaikan suhu, atau emisi gas. Masyarakat diminta meningkatkan kewaspadaan dan membatasi aktivitas di zona rawan.</td>
                </tr>
                <tr>
                    <td style="padding:12px; font-weight:bold; color:#4a5568;">NORMAL (Level I)</td>
                    <td style="padding:12px; color:#4a5568; font-size:13px;">Aktivitas gunungapi berada pada kondisi dasar/normal. Belum ada tanda peningkatan aktivitas vulkanik yang signifikan. Masyarakat tetap waspada dan tidak mendekati area kawah tertentu.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <div style="margin-top:25px;">
        <h4 style="color:#1e3a8a; font-size:18px; margin-bottom:12px; display:flex; align-items:center; font-weight:bold;">
            <span style="margin-right:10px;">📺</span> CCTV Live Merapi (BPPTKG)
        </h4>
        <a href="{youtube_url}" target="_blank" style="text-decoration:none;">
            <div style="position:relative; background-color:white; padding:10px; border-radius:12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; overflow:hidden;">
                <div style="position:relative; border-radius:8px; overflow:hidden; display:block;">
                    <img src="{thumbnail_url}" style="width:100%; display:block; filter: brightness(0.9);">
                    <div style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); background:rgba(30, 58, 138, 0.8); border-radius:50%; width:60px; height:60px; display:flex; align-items:center; justify-content:center; box-shadow: 0 0 20px rgba(0,0,0,0.3);">
                        <div style="width: 0; height: 0; border-top: 12px solid transparent; border-left: 20px solid white; border-bottom: 12px solid transparent; margin-left: 5px;"></div>
                    </div>
                </div>
                <div style="padding:12px; text-align:center; color:#1e3a8a; font-weight:bold; font-size:13px; letter-spacing:0.5px;">
                    KLIK UNTUK PANTAU LIVE VISUAL
                </div>
            </div>
        </a>
    </div>

    <div style="margin-top:25px;">
        <h4 style="color:#1e3a8a; font-size:18px; margin-bottom:12px; display:flex; align-items:center; font-weight:bold;">
            <span style="margin-right:10px;">🗺️</span> Letak Gunung Merapi
        </h4>
        <div style="background-color:white; padding:10px; border-radius:12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; overflow:hidden;">
            <div style="border-radius:8px; overflow:hidden;">
                {map_html}
            </div>
            <div style="padding:12px; text-align:center; color:#475569; font-size:12px; font-style:italic;">
                Gunakan scroll untuk zoom in/out pada area kawah dan pemukiman sekitar.
            </div>
        </div>
    </div>

    <div style="margin-top:25px; text-align:center; font-size:11px; color:#94a3b8; border-top: 1px solid #e2e8f0; padding-top:15px;">
        SADAM Project • Sumber Data: PVMBG & BPPTKG
    </div>

</div>
"""

# Render kode HTML asli ke dalam aplikasi Streamlit
components.html(dashboard_html, height=1700, scrolling=True)
