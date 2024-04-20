# Python script that will apply the migrations up to head
import sys
import alembic.config
import os

here = os.path.dirname(os.path.abspath(__file__))

print(sys.argv[1:])

alembic_args = [
    "-c",
    os.path.join(here, "alembic.ini"),
    *sys.argv[1:],
    # 'upgrade', 'head'
]


def main():
    alembic.config.main(argv=alembic_args)
