# kakaotalk-visualization

## Using
- Python
- SQLAlchemy
- alembic
- jupyter

## TODO
- [많음](https://github.com/nerogit/kakaotalk-visualization/issues)

## How to run
1. [split](http://stackoverflow.com/questions/3066948/how-to-file-split-at-a-line-number)
이용해서 파일을 작은 단위로 split(디버깅효율과 io 시간 단축위해) 후 chats 디렉토리에 복사
1. `mkvirtualenv -p python3` katalk-visualization
1. `pip install -r requirements.txt`
1. `cd src; alembic upgrade head`
1. `python run.py`
