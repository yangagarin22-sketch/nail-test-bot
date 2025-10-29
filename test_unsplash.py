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
        print(f"🔑 Ключ API: {ACCESS_KEY[:10]}...")
        print("-" * 60)
        
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📡 HTTP Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            images = data.get('results', [])
            
            print(f"✅ УСПЕХ! Найдено изображений: {len(images)}")
            print("=" * 60)
            
            successful_count = 0
            for i, img in enumerate(images):
                try:
                    # Безопасное получение данных с проверкой на None
                    image_url = img.get('urls', {}).get('regular', 'Нет URL')
                    author = img.get('user', {}).get('name', 'Неизвестный автор')
                    description = img.get('description', 'Нет описания')
                    width = img.get('width', 'Неизвестно')
                    height = img.get('height', 'Неизвестно')
                    download_link = img.get('links', {}).get('download', 'Нет ссылки')
                    
                    # Если нет основного URL, пропускаем
                    if image_url == 'Нет URL':
                        print(f"\n⚠️  ФОТО #{i+1} - Пропущено (нет URL)")
                        continue
                    
                    successful_count += 1
                    print(f"\n🎨 ФОТО #{i+1}")
                    print(f"   👤 Автор: {author}")
                    print(f"   📝 Описание: {str(description)[:100]}...")
                    print(f"   🔗 Просмотр: {image_url}")
                    print(f"   📥 Скачать: {download_link}")
                    print(f"   📏 Размер: {width}x{height}")
                    
                except Exception as img_error:
                    print(f"\n⚠️  Ошибка обработки фото #{i+1}: {img_error}")
                    continue
                    
            return successful_count
            
        else:
            print(f"❌ ОШИБКА API: {response.text}")
            return 0
            
    except requests.exceptions.Timeout:
        print("💥 Таймаут соединения (>15 секунд)")
        return 0
    except requests.exceptions.ConnectionError:
        print("💥 Ошибка подключения к Unsplash API")
        return 0
    except Exception as e:
        print(f"💥 Неожиданная ошибка: {e}")
        return 0

if __name__ == "__main__":
    print("🚀 Запуск теста Unsplash API...")
    successful_images = test_unsplash_search()
    
    if successful_images > 0:
        print(f"\n🎉 ТЕСТ ПРОЙДЕН! Успешно обработано {successful_images} фото")
        print(f"🔗 Ссылки выше можно открывать в браузере для просмотра")
    else:
        print(f"\n😞 ТЕСТ НЕ ПРОШЕЛ. Фото не получены.")
