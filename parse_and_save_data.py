from src import (
    User,
    Katalk,
    engine,
)
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

Session = sessionmaker(bind=engine)


def md5(input_):
    import hashlib
    return hashlib.md5(input_.encode()).hexdigest()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_logger():
    import logging
    logger = logging.getLogger(__file__)
    log_fn = 'kakao.log'
    hdlr = logging.FileHandler(log_fn)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


class KakaoTalk:
    hash_of_line = ''
    user_name = ''
    real_text = ''
    created_at = datetime.now()
    logger = get_logger()

    def save(self):
        s = Session()
        user = get_or_create(s, User, name=self.user_name)
        try:
            katalk = Katalk(
                unique_key=md5(self.hash_of_line),
                user=user,
                text=self.real_text,
                strlength=len(self.real_text),
                created_at=self.created_at,
            )
            s.add(katalk)
            s.commit()
        except IntegrityError:
            # 중복 저장 방지
            pass
        s.close()

    def analysis(self, fn, cnt, line):
        import re
        rule = re.compile(
            r'(?P<created_at>201\d년 (\d+)월 (\d+)일 오[전|후] (\d+):(\d+)), (?P<user_name>\w+) : (?P<real_text>.+)'
        )  # 한 말풍선에 여러 개행있으면 안됨
        try:
            dict_line = rule.match(line).groupdict()
        except AttributeError:
            self.logger.error('Analysis: {}:{}, "{}" parse error'.format(fn, cnt, line))
            return False
        self.hash_of_line = md5(line[:255])
        _created_at = dict_line['created_at']
        _created_at = _created_at.replace("오전", "am") if "오전" in _created_at else _created_at.replace("오후", "pm")
        self.created_at = datetime.strptime(_created_at, "%Y년 %m월 %d일 %p %I:%M")
        self.user_name = dict_line['user_name']
        self.real_text = dict_line['real_text']
        return True

    def read_kakaotalk_file(self, filename):
        import os
        filepath = os.path.join('chats', filename)
        with open(filepath, 'r', encoding='utf-8') as fp:
            for cnt, line in enumerate(fp):
                if self.analysis(filename, cnt, line) is True:
                    self.save()


if __name__ == "__main__":
    import sys
    import string

    sys.path.append('src')  # for alembic

    alphabets = string.ascii_lowercase
    print("GO!")
    k = KakaoTalk()
    for i in alphabets:
        try:
            k.read_kakaotalk_file("xa%s" % i)
        except FileNotFoundError:
            print("Done! ", i)
            break
