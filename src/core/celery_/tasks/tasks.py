from time import sleep
import os

from PIL import Image

from core.celery_.celery_conf import celery_app




@celery_app.task
def background_task():
    print('Начал выполнение повторной задачи')
    sleep(3)
    print('Закончил выполнение повторной задачи')
    
    
@celery_app.task
def saving_photo(file_path: str):
    print('Начал выполнение задачи')
    sizes = [i for i in range(100, 3000, 10)]
    output_folder = "static/images/changed"

    # Открываем изображение
    img = Image.open(file_path)

    # Получаем имя файла и его расширение
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)

    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize((size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS)

        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"

        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)

        # Сохраняем изображение
        img_resized.save(output_path)

    print(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")