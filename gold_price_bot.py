import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://kimkhanhviethung.vn/tra-cuu-gia-vang.html'

def get_gold_price():
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        message = f"🔔 **GIÁ VÀNG KIM KHÁNH VIỆT HÙNG**\nCập nhật lúc: {datetime.now().strftime('%H:%M %d/%m/%Y')}\n\n"
        
        table_div = soup.find('div', class_='table_goldprice')
        if not table_div:
            return "⚠️ Không tìm thấy bảng giá trên website."

        table = table_div.find('table')
        rows = table.find_all('tr')
        found_data = False
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                name = cols[0].text.strip().lower()
                if '999.9' in name or '9999' in name or '98' in name:
                    gold_type = cols[0].text.strip()
                    buy_price = cols[1].text.strip()
                    sell_price = cols[2].text.strip()
                    
                    message += f"🔹 **{gold_type}**:\n"
                    message += f"   - Mua vào: {buy_price}\n"
                    message += f"   - Bán ra: {sell_price}\n\n"
                    found_data = True

        return message if found_data else "⚠️ Không tìm thấy dữ liệu."
            
    except Exception as e:
        return f"❌ Lỗi khi lấy dữ liệu: {e}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID, 
        'text': text,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=payload)

if __name__ == '__main__':
    price_info = get_gold_price()
    send_telegram_message(price_info)