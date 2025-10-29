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
    
    # Оптимизированный запрос на английском
    query = "pastel gradient nails white daisies gold flakes nail art closeup professional manicure"
    
    # Параметры для лучшего поиска
    url = f"https://api.unsplash.com/search/photos?query={query}&per_page=10&order_by=popularity"
    
    headers = {
        "Authorization": f"Client-ID {ACCESS_KEY}"
    }
    
    try:
        print("=" * 70)
        print(f"🔍 ТОЧНЫЙ ПОИСК ДЛЯ МАНИКЮРНЫХ СТАТЕЙ")
        print("=" * 70)
        print(f"📝 Оригинальный запрос: Нежное градиентное покрытие в пастельных тонах с белыми ромашками и золотыми вкраплениями")
        print(f"🌐 Поисковый запрос: {query}")
        print(f"🌍 Регион Render: Frankfurt (EU Central)")
        print(f"⏰ Время запуска: {datetime.now()}")
        print(f"🔑 Ключ API: {ACCESS_KEY[:10]}...")
        print("-" * 70)
        
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"📡 HTTP Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            images = data.get('results', [])
            
            print(f"✅ Найдено изображений: {len(images)}")
            print("=" * 70)
            
            # Фильтруем и сортируем по популярности
            filtered_images = []
            for img in images:
                likes = img.get('likes', 0)
                downloads = img.get('downloads', 0)
                # Отбираем только популярные фото
                if likes > 10 or downloads > 50:
                    filtered_images.append(img)
            
            # Сортируем по лайкам (популярности)
            filtered_images.sort(key=lambda x: x.get('likes', 0), reverse=True)
            
            # Берем топ-5
            top_images = filtered_images[:5]
            
            print(f"🎯 Отобрано лучших фото: {len(top_images)}")
            print("=" * 70)
            
            successful_count = 0
            for i, img in enumerate(top_images):
                try:
                    # Безопасное получение данных
                    image_url = img.get('urls', {}).get('regular', 'Нет URL')
                    author = img.get('user', {}).get('name', 'Неизвестный автор')
                    username = img.get('user', {}).get('username', '')
                    description = img.get('description', 'Нет описания')
                    alt_description = img.get('alt_description', 'Нет описания')
                    width = img.get('width', 'Неизвестно')
                    height = img.get('height', 'Неизвестно')
                    downloads = img.get('downloads', 0)
                    likes = img.get('likes', 0)
                    views = img.get('views', 0)
                    
                    if image_url == 'Нет URL':
                        print(f"\n⚠️  ФОТО #{i+1} - Пропущено (нет URL)")
                        continue
                    
                    successful_count += 1
                    print(f"\n🏆 ФОТО #{i+1} (Рейтинг: {likes}❤️)")
                    print(f"   👤 Автор: {author} (@{username})")
                    print(f"   📝 Описание: {description or alt_description}")
                    print(f"   📊 Статистика: {likes} лайков, {downloads} загрузок, {views} просмотров")
                    print(f"   🔗 Просмотр: {image_url}")
                    print(f"   📥 Скачать: https://unsplash.com/photos/{img.get('id', '')}/download")
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
    print("🚀 Запуск улучшенного поиска для маникюрных статей...")
    successful_images = test_unsplash_search()
    
    if successful_images > 0:
        print(f"\n🎉 ПОИСК УСПЕШЕН! Найдено {successful_images} качественных фото")
        print(f"📸 Фото отсортированы по популярности (лайкам)")
        print(f"🔗 Ссылки выше можно открывать в браузере")
    else:
        print(f"\n😞 Фото не найдены. Попробуйте изменить поисковый запрос.")
