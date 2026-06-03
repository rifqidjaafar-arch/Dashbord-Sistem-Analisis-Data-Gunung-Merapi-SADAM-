import streamlit as st
from streamlit_folium import st_folium

import requests
from bs4 import BeautifulSoup
import pandas as pd
import folium
from datetime import datetime

# =========================
# KONFIGURASI HALAMAN
# =========================

st.set_page_config(
    page_title="SADAM - Monitoring Merapi",
    page_icon="🌋",
    layout="wide"
)

# =========================
# FUNGSI AMBIL DATA
# =========================

def ambil_data_merapi():

    url = "https://magma.esdm.go.id/v1/gunung-api/laporan"

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:

        res = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            res.text,
            "lxml"
        )

        cards = soup.find_all(
            ["div", "article"],
            class_=["card", "card-body", "col-md-6"]
        )

        for card in cards:

            card_text = card.get_text()

            if "Merapi" in card_text:

                status_tag = card.find(
                    "span",
                    class_="badge"
                )

                status = (
                    status_tag.text.strip()
                    if status_tag
                    else "Data Tidak Ditemukan"
                )

                visual = (
                    "Teramati asap kawah utama "
                    "berwarna putih dengan "
                    "intensitas tipis hingga tebal."
                )

                p_tags = card.find_all("p")

                for p in p_tags:

                    if (
                        "visual" in p.text.lower()
                        or
                        "asap" in p.text.lower()
                    ):
                        visual = p.text.strip()
                        break

                return {
                    "status": status,
                    "visual": visual,
                    "waktu": datetime.now().strftime(
                        "%d-%m-%Y %H:%M:%S"
                    )
                }

        return {
            "status": "Data Tidak Ditemukan",
            "visual": "Gagal sinkronisasi dengan MAGMA.",
            "waktu": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }

    except Exception as e:

        return {
            "status": "Error Koneksi",
            "visual": str(e),
            "waktu": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )
        }


# =========================
# AMBIL DATA
# =========================

data = ambil_data_merapi()

# =========================
# HEADER
# =========================

st.title("🌋 SADAM")
st.caption(
    "Sistem Analisis Data Gunung Merapi • Monitoring Real-Time"
)

# =========================
# DESKRIPSI MERAPI
# =========================

st.markdown("## Mengenal Gunung Merapi")

st.write(
    """
Gunung Merapi merupakan salah satu gunung api paling aktif di dunia
yang berada di perbatasan Jawa Tengah dan Daerah Istimewa Yogyakarta.

Secara geologis, Merapi merupakan gunung api stratovulkanik yang
memiliki karakter erupsi efusif maupun eksplosif serta sering
membentuk kubah lava yang dapat menghasilkan awan panas guguran.
"""
)

# =========================
# STATUS AKTIVITAS
# =========================

st.markdown("## Status Aktivitas")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Status Gunungapi",
        data["status"]
    )

with col2:
    st.metric(
        "Waktu Update",
        data["waktu"]
    )

# =========================
# KETERANGAN VISUAL
# =========================

st.markdown("## Keterangan Visual")

st.info(data["visual"])

# =========================
# TABEL MITIGASI
# =========================

st.markdown("## Protokol Mitigasi dan Keselamatan")

df_mitigasi = pd.DataFrame(
    {
        "Level": [
            "Level IV (AWAS)",
            "Level III (SIAGA)",
            "Level II (WASPADA)",
            "Level I (NORMAL)"
        ],
        "Keterangan": [
            "Erupsi sedang berlangsung atau segera terjadi. Evakuasi wajib dilakukan.",
            "Aktivitas meningkat signifikan. Persiapan evakuasi dan pembatasan aktivitas.",
            "Aktivitas di atas normal. Tingkatkan kewaspadaan.",
            "Aktivitas normal. Pemantauan rutin tetap dilakukan."
        ]
    }
)

st.dataframe(
    df_mitigasi,
    use_container_width=True,
    hide_index=True
)

# =========================
# CCTV
# =========================

st.markdown("## CCTV Live Merapi")

video_id = "8X7gHBhD1Tw"

st.image(
    f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
    use_container_width=True
)

st.link_button(
    "Buka CCTV Live Merapi",
    f"https://www.youtube.com/watch?v={video_id}"
)

# =========================
# PETA
# =========================

st.markdown("## Peta Lokasi Gunung Merapi")

m = folium.Map(
    location=[-7.54, 110.44],
    zoom_start=12
)

folium.Marker(
    [-7.54, 110.44],
    popup="Gunung Merapi",
    icon=folium.Icon(
        color="red",
        icon="info-sign"
    )
).add_to(m)

st_folium(
    m,
    width=1200,
    height=500
)

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "SADAM Project • Sumber Data: PVMBG, MAGMA Indonesia, BPPTKG"
)
