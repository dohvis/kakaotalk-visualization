from src import (
    User,
    Katalk,
    engine,
)
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError, IntegrityError
Session = sessionmaker(bind=engine)

s = Session()

def md5(input_):
    import hashlib
    return hashlib.md5(input_.encode()).hexdigest()

def error_handler(f, e, line):
    with open('error.txt', 'a', encoding='utf8') as fp:
        content = "{file} {error}: {line}"
        fp.write(content.format(file=f, error=e, line=line))

def read_kakaotalk_file(filename):
    import os
    filepath = os.path.join('chats', filename)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as fp:
        for line in fp:
            try:
                anal(line)
            except Exception as e:
                print("!!! ERRROR !!!!")

                error_handler(filename, e, line)

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def anal(line):
    # print(line, '!!')
    s = Session()
    try:
        splited = line.split(",")
    except ValueError:
        # 채팅방 초대메세지 등등
        return False
    created_at, text = splited[0], splited[1]
    # created_at, text = line.split(",") 이렇게하면 본문에있는 , 까지 짤려서

    
    if "오전" in created_at:
        created_at = created_at.replace("오전", "am")
    else:
        created_at = created_at.replace("오후", "pm")
    created_at = datetime.strptime(created_at, "%Y년 %m월 %d일 %p %I:%M")

    end_name = text.find(" :")
    if end_name < 0:
        # ~~님이 ~~를 초대했습니다 or ~~님이 나갔습니다.
        return False
    name = text[1:end_name]
    user = get_or_create(s, User, name=name)
    real_text = text[end_name+3:]
    
    try:
        katalk = Katalk(
            unique_key=md5(line[:255]),
            user=user,
            text=real_text,
            strlength=len(real_text),
            created_at=created_at,
        )
        s.add(katalk)
        s.commit()
    except (InvalidRequestError, IntegrityError):
        pass
    s.close()

if __name__ == "__main__":
    import sys
    import logging
    logging.disable(level=logging.INFO)
    sys.path.append('src')
    f = open("error.txt", "w")
    f.close()
    import string
    alphabets = string.ascii_lowercase
    print("GO!")
    for i in alphabets:
        try:
            read_kakaotalk_file("xa%s" % i)
        except FileNotFoundError:
            print("Done! ", i)
            break

