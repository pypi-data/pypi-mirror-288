Air Migrations
==

Библиотека обертка для алембика. Основная идея обертки, что можно напрямую указать в какую базу необходимо применить миграции, а так же в какую схему (Можно использовать -x чистого алембика)
Дополнительно возможно получить сырой sql, который будет применен в БД (алембик не предоставляет это в автоматическом режиме)
```shell
#Dev run
python -m air_migrations.cli DB_URL SCHEMA COMMAND

#User
migrate DB_URL SCHEMA COMMAND [REVISION]
#or 
python -m migrate DB_URL SCHEMA COMMAND
```
***Описание***

*Обязательные флаги*

1. DB_URL - url базы данных следующего вида login:password@localhost:5432/db
2. SCHEMA - указывается используемая схема (public)
3. COMMAND - доступны команды [upgrade, downgrade, revision]
4. REVISION - ревизия миграции (обычно base, head или уникальный номер). Обязателен только в случае использования COMMAND, которые равны [upgrade, downgrade]

*Необязательные флаги*

1. --autogenerate, -a - автогенерация ревизии миграции, используется если COMMAND равна "revision", иначе игнорируется
2. --message, -m - сообщение для генерации ревизии, используется если COMMAND равна "revision", иначе игнорируется
3. --sql-output, -s - папка для генерации сырого sql относительно ревизий, в момент генерации не применяется к базе данных, но требует подключения. Используется с COMMAND равным [upgrade, downgrade]
4. --config, -c - местоположение alembic.ini конфига, по-умолчанию в папке запуска

Примеры команд

User
```shell
migrate test:test@localhost:5432/test public upgrade head --sql ./
migrate test:test@localhost:5432/test public upgrade head
migrate test:test@localhost:5432/test public downgrade base --sql ./
migrate test:test@localhost:5432/test public downgrade base
migrate test:test@localhost:5432/test public upgrade head
```

Dev
```shell
python -m air_migrations.cli -с dev/alembic.ini test:test@localhost:5432/test public revision --autogenerate --message 'init'
python -m air_migrations.cli -с dev/alembic.ini test:test@localhost:5432/test public revision --message 'some revision'
python -m air_migrations.cli -с dev/alembic.ini test:test@localhost:5432/test public upgrade head --sql ./
python -m air_migrations.cli -с dev/alembic.ini test:test@localhost:5432/test public upgrade head
python -m air_migrations.cli -с dev/alembic.ini test:test@localhost:5432/test public downgrade base --sql ./
python -m air_migrations.cli -с dev/alembic.ini test:test@localhost:5432/test public downgrade base
python -m air_migrations.cli -с dev/alembic.ini test:test@localhost:5432/test public upgrade head
```


***Examples***

*Применение миграций из кода*

```python
#main.py
import os
import subprocess

URL: str = 'test:test@localhost:5432/test'
SCHEMA: str = os.getenv("POSTGRES_SCHEMA_NAME", 'public')

def upgrade_from_code() -> None:
    output = subprocess.run(["migrate", URL, SCHEMA, "upgrade", "head"], capture_output=True, text=True)
    print(output.stdout)


def downgrade_from_code() -> None:
    output = subprocess.run(["migrate", URL, SCHEMA, "downgrade", "base"], capture_output=True, text=True)
    print(output.stdout)
```

*Применение в тестах*

```python
#tests/conftest.py
import os
import subprocess

import pytest


URL: str = 'test:test@localhost:5432/test'
SCHEMA: str = os.getenv("POSTGRES_SCHEMA_NAME", 'public')

@pytest.fixture(autouse=True, scope="session")
def db_setup():
    subprocess.run(["migrate", URL, SCHEMA, "upgrade", "head"], capture_output=True, text=True)
    yield
    subprocess.run(["migrate", URL, SCHEMA, "downgrade", "base"], capture_output=True, text=True)
```


Пример реализации env.py (используется асинхронная версия)

```python
import asyncio
import os
from logging.config import fileConfig

from air_migrations import add_driver_to_url
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Here import your Base and models
from models import Base, Users

config = context.config
if not config.get_section_option("alembic", "sqlalchemy.url"):
    url = os.getenv("POSTGRES_DATABASE_URL", "")
    url = add_driver_to_url(url)
    config.set_main_option("sqlalchemy.url", url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
Base.metadata.schema = config.get_section_option("alembic", "schema")
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url_ = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url_,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=target_metadata.schema,
        echo=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=target_metadata.schema,
        include_schemas=True,
        echo=True,
    )

    with context.begin_transaction():
        if target_metadata.schema is not None:
            # Создание схемы если отсутствует
            context.execute(f"create schema if not exists {target_metadata.schema};")
            context.execute(f"set search_path to {target_metadata.schema}")
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool, echo=True
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```