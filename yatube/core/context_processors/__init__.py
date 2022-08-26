from datetime import datetime

def year():
    year = datetime.now().year
    """Добавляет переменную с текущим годом."""
    return {'year': year}