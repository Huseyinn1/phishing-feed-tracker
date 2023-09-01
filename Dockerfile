# Temel alınacak Docker imajı belirleniyor
FROM python:3.10.11-slim

# Uygulama klasörü oluşturuluyor
WORKDIR /app

# Poetry kütüphane dosyalarının kopyalanması ve yüklenmesi
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && poetry install --no-root

# Uygulama dosyalarının kopyalanması
COPY . .


