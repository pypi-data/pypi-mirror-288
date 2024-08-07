import argparse
from enum import StrEnum
from typing import Optional
from pathlib import Path
import contextlib
import asyncio

from alembic.config import Config
from alembic.script import ScriptDirectory, Script
from alembic import command
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncConnection
from sqlalchemy.engine import Connection
from alembic.runtime.migration import MigrationContext

from .utils import add_driver_to_url


class ActionEnum(StrEnum):
    UPGRADE = "upgrade"
    DOWNGRADE = "downgrade"
    REVISION = "revision"

    @classmethod
    def to_list(cls) -> list[str]:
        return [action for action in cls]


class SQLGenerator:
    __slots__ = (
        "_alembic_cfg",
        "_output_path",
        "_engine",
    )

    def __init__(self, alembic_cfg: Config, output_dir: Optional[str] = None) -> None:
        self._alembic_cfg: Config = alembic_cfg
        self._output_path: Path = Path(output_dir)
        self._output_path.mkdir(parents=True, exist_ok=True)
        self._engine: AsyncEngine = create_async_engine(alembic_cfg.get_main_option("sqlalchemy.url"), echo=True)

    @staticmethod
    async def get_current_revision(conn: AsyncConnection) -> Optional[str]:
        """Get the current revision from the database."""

        def sync_get_current_revision(connection: Connection):
            context = MigrationContext.configure(connection)
            return context.get_current_revision()

        return await conn.run_sync(sync_get_current_revision)

    @staticmethod
    def _determine_revisions(
        script_: ScriptDirectory, action: ActionEnum, target_rev: str, current_rev: str
    ) -> list[Script]:
        """Determine the list of revisions to apply based on the action."""
        if action is ActionEnum.UPGRADE:
            return [rev for rev in script_.iterate_revisions(target_rev, current_rev)]
        elif action is ActionEnum.DOWNGRADE:
            return [rev for rev in script_.iterate_revisions(current_rev, target_rev)]
        raise ValueError(f"Invalid action: {action}")

    @staticmethod
    def _determine_alembic_command(action: ActionEnum) -> callable:
        """Map the action to the corresponding Alembic command."""
        if action is ActionEnum.UPGRADE:
            return command.upgrade
        elif action is ActionEnum.DOWNGRADE:
            return command.downgrade
        raise ValueError(f"Invalid action: {action}")

    async def generate_sql_files(self, conn: AsyncConnection, revisions: list[Script], action: ActionEnum) -> None:
        """Generate SQL files for each revision."""
        alembic_command: callable = self._determine_alembic_command(action)

        for rev in reversed(revisions):
            down_revision: str = rev.down_revision or "base"
            rev_id: str = rev.revision
            file_name: str = f"{Path(rev.path).stem}.sql"
            file_name = f"{'up' if action is ActionEnum.UPGRADE else 'down'}_{file_name}"
            file_path: Path = self._output_path / file_name
            if file_path.exists():
                raise FileExistsError(f"The file {file_path} already exist")
            revision_step = f"{down_revision}:{rev_id}" if action is ActionEnum.UPGRADE else f"{rev_id}:{down_revision}"

            with open(file_path, "w") as file:
                with contextlib.redirect_stdout(file):
                    await conn.run_sync(lambda sync_conn: alembic_command(self._alembic_cfg, revision_step, sql=True))
            print(f"Generated SQL for revision {rev_id} in {file_path}")

    async def generate_sql(self, action: ActionEnum, revision: str = "head") -> None:
        """Generate SQL files for each unapplied migration up to the target revision asynchronously."""
        async with self._engine.connect() as conn:
            current_rev: Optional[str] = await self.get_current_revision(conn)
            script_ = ScriptDirectory.from_config(self._alembic_cfg)
            revisions: list[Script] = self._determine_revisions(script_, action, revision, current_rev)
            await self.generate_sql_files(conn, revisions, action)


def main():
    parser = argparse.ArgumentParser(description="Database migration tool")
    parser.add_argument(
        "--config", "-c", help="Alternate config file", type=str, default="./alembic.ini", required=False
    )
    parser.add_argument("url", help="Database URL", type=str, metavar="login:password@localhost:5432/db")
    parser.add_argument("schema", help="Target schema", type=str, metavar="public")
    parser.add_argument("command", choices=ActionEnum.to_list(), help="Alembic command", metavar=ActionEnum.REVISION)
    parser.add_argument(
        "revision",
        nargs="?" if parser.parse_known_args()[0].command == ActionEnum.REVISION else "+",
        type=str,
        default="head",
        help="Revision to apply or target for SQL generation",
        metavar="head",
    )
    parser.add_argument("--autogenerate", "-a", action="store_true", help="Alembic action for autogenerate revision")
    parser.add_argument("--message", "-m", required=False, type=str, help="Revision message", metavar="init")
    parser.add_argument("--sql-output", "-s", type=str, required=False, help="Path for alembic action SQL generation")

    args = parser.parse_args()

    alembic_cfg = Config(Path(args.config))
    alembic_cfg.set_main_option("sqlalchemy.url", add_driver_to_url(args.url))
    alembic_cfg.set_main_option("schema", args.schema)

    if args.command == ActionEnum.REVISION:
        command.revision(alembic_cfg, message=args.message, autogenerate=args.autogenerate)
    elif args.sql_output:
        generator = SQLGenerator(alembic_cfg, args.sql_output)
        asyncio.run(generator.generate_sql(ActionEnum(args.command), args.revision))
    elif args.command == ActionEnum.UPGRADE:
        command.upgrade(alembic_cfg, args.revision[0])
    elif args.command == ActionEnum.DOWNGRADE:
        command.downgrade(alembic_cfg, args.revision[0])


if __name__ == "__main__":
    main()
