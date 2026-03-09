import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import os

# --- LẤY THÔNG TIN TỪ BIẾN MÔI TRƯỜNG (GITHUB SECRETS) ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
URL = 'https://kimkhanhviethung.vn/tra-cuu-gia-vang.html'

def get_gold_price():
    try:
        # Tải trang web
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Chuyển đổi sang múi giờ Việt Nam (UTC+7)
        vn_time = datetime.now(timezone.utc) + timedelta(hours=7)
        message = f"🔔 **GIÁ VÀNG KIM KHÁNH VIỆT HÙNG**\nCập nhật lúc: {vn_time.strftime('%H:%M %d/%m/%Y')}\n\n"
        
        # Tìm div chứa bảng giá vàng
        table_div = soup.find('div', class_='table_goldprice')
        if not table_div:
            return "⚠️ Không tìm thấy bảng giá trên website."

        table = table_div.find('table')
        rows = table.find_all('tr')
        found_data = False
        
        for row in rows:
            cols = row.find_all('td')
            # Kiểm tra xem hàng này có đủ cột dữ liệu không
            if len(cols) >= 3:
                name = cols[0].text.strip().lower()
                
                # Lọc đúng loại vàng 999.9, 9999 và 98
                if '999.9' in name or '9999' in name or '98' in name:
                    gold_type = cols[0].text.strip()
                    buy_price = cols[1].text.strip()
                    sell_price = cols[2].text.strip()
                    
                    message += f"🔹 **{gold_type}**:\n"
                    message += f"   - Mua vào: {buy_price}\n"
                    message += f"   - Bán ra: {sell_price}\n\n"
                    found_data = True

        if found_data:
            return message
        else:
            return "⚠️ Không tìm thấy dữ liệu vàng 999.9 và 98 trong bảng."
            
    except Exception as e:
        return f"❌ Lỗi khi lấy dữ liệu: {e}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID, 
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Lỗi gửi tin nhắn: {response.text}")
    else:
        print("Đã gửi tin nhắn thành công!")

# --- CHẠY CHƯƠNG TRÌNH KHI GITHUB ACTIONS KÍCH HOẠT ---
if __name__ == '__main__':
    print("Đang lấy dữ liệu và gửi thông báo...")
    price_info = get_gold_price()
    send_telegram_message(price_info)
