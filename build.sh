#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
# 모든 static 파일(js, css 파일 등)을 수집해 한 폴더에 넣어줌
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
# 개발 환경에서 사용하는 DB와는 다른 별도의 DB이므로 migrate 필요
# Render가 알아서 migration 파일을 확인하고 새로운 DB에 적용함
python manage.py migrate

# Render의 Shell을 사용하지 않고 Superuser 만들기
if [[ $CREATE_SUPERUSER]];
then
    python manage.py createsuperuser --no-input
fi