import matplotlib.pyplot as plt
import io
import matplotlib.dates as mdates
from datetime import datetime
from typing import List, Dict

def generate_price_chart(article: int, title: str, history: List[Dict]) -> io.BytesIO:
    """Генерирует график изменения цены товара в формате PNG"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)

    dates = [datetime.strptime(item['recorded_at'], '%Y-%m-%d %H:%M:%S') for item in history]
    prices = [item['price'] for item in history]

    # Линия цены
    ax.plot(dates, prices, color='#38bdf8', marker='o', linewidth=2.5, markersize=6)
    ax.fill_between(dates, prices, color='#38bdf8', alpha=0.15)

    # Настройки стилей
    ax.set_title(f"История цены: {title[:30]}... (Арт: {article})", fontsize=12, pad=15, color='#f8fafc', fontweight='bold')
    ax.set_ylabel("Цена (₽)", fontsize=10, color='#94a3b8')
    ax.grid(True, linestyle='--', alpha=0.2, color='#ffffff')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m %H:%M'))
    fig.autofmt_xdate()

    plt.tight_layout()

    # Сохраняем в память
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', transparent=False)
    img_buf.seek(0)
    plt.close(fig)

    return img_buf
