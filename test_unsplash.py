import os
import requests
import json
from datetime import datetime

def test_unsplash_search():
    # Получаем ключ из переменных окружения
    ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    
    if not ACCESS_KEY:
        print("❌ Ошибка: UNSPLASH_ACCESS_KEY не установлен в переменных окружения")
        return None
    
    # Ваш запрос
    query = "white daisy gold flakes pastel gradient nails"
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=5"
    
    headers = {
        "Authorization": f"Client-ID {ACCESS_KEY}"
    }
    
    try:
        print("=" * 60)
        print(f"🔍 ТЕСТОВЫЙ ЗАПРОС К UNSPLASH API")
        print("=" * 60)
        print(f"📝 Поисковый запрос: {query}")
        print(f"🌍 Регион Render: Frankfurt (EU Central)")
        print(f"⏰ Время запуска: {datetime.now()}")
        print(f"🔑 Ключ API: {ACCESS_KEY[:10]}...")  # Показываем только начало ключа
        print("-" * 60)
        
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📡 HTTP Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            images = data.get('results', [])
            
            print(f"✅ УСПЕХ! Найдено изображений: {len(images)}")
            print("=" * 60)
            
            for i, img in enumerate(images):
                image_url = img['urls']['regular']
                author = img['user']['name']
                description = img.get('description', 'Нет описания')
                
                print(f"\n🎨 ФОТО #{i+1}")
                print(f"   👤 Автор: {author}")
                print(f"   📝 Описание: {description[:100]}...")
                print(f"   🔗 Просмотр: {image_url}")
                print(f"   📥 Скачать: {img['links']['download']}")
                print(f"   📏 Размер: {img['width']}x{img['height']}")
                
            return images
        else:
            print(f"❌ ОШИБКА API: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("💥 Таймаут соединения (>15 секунд)")
        return None
    except requests.exceptions.ConnectionError:
        print("💥 Ошибка подключения к Unsplash API")
        return None
    except Exception as e:
        print(f"💥 Неожиданная ошибка: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Запуск теста Unsplash API...")
    results = test_unsplash_search()
    
    if results:
        print(f"\n🎉 ТЕСТ ПРОЙДЕН! Получено {len(results)} фото")
    else:
        print(f"\n😞 ТЕСТ НЕ ПРОШЕЛ. Фото не получены.")