# FILE: src/neurotransanalytics/data_adapter/loaders/config_loader.py

import configparser


def load_config(path):
    """
    Загрузка legacy config_old.ini (Delphi-style).

    Особенности:
    - комментарии начинаются с //
    - файл может не содержать секций
    - допускает повторяющиеся ключи
    """

    raw_bytes = path.read_bytes()

    try:
        text = raw_bytes.decode("cp1251")
    except Exception:
        text = raw_bytes.decode("cp1251", errors="ignore")

    lines = []

    for line in text.splitlines():
        stripped = line.strip()

        # Delphi-комментарии
        if stripped.startswith("//"):
            continue

        lines.append(line)

    cleaned_text = "\n".join(lines)

    # Если нет секций — добавляем фиктивную
    if not cleaned_text.lstrip().startswith("["):
        cleaned_text = "[DEFAULT]\n" + cleaned_text

    # ВАЖНО: strict=False — разрешаем повторяющиеся ключи
    parser = configparser.ConfigParser(strict=False)
    parser.read_string(cleaned_text)

    return parser
