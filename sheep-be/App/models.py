from flask_sqlalchemy import SQLAlchemy
from settings import db
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from passlib.hash import sha256_crypt


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    author = db.Column(db.String(20))
    pubdate = db.Column(db.DateTime)
    thumb = db.Column(db.String(30))


'''
CREATE TABLE news(
	id INT NOT NULL AUTO_INCREMENT,
	category INT NOT NULL DEFAULT 0,
	title VARCHAR(50) NOT NULL,
	content TEXT,
	author VARCHAR(20),
	thumb VARCHAR(30) DEFAULT NULL ,
	pubdate DATETIME,
	PRIMARY KEY(id)
)
'''


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(30), nullable=False)
    upass = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30))
    role = db.Column(db.Integer, server_default=db.FetchedValue())


'''
CREATE TABLE cms_adm (
    id   INT NOT NULL AUTO_INCREMENT,
    NAME        VARCHAR(30) NOT NULL,
    PASSWORD    VARCHAR(30) NOT NULL,
    gender    INT NOT NULL DEFAULT 0,
    email     VARCHAR(30) DEFAULT NULL,
    remark    VARCHAR(50) DEFAULT NULL,
    create_time datetime DEFAULT NULL,
    update_time datetime DEFAULT NULL,
    PRIMARY KEY(id)
);
'''


class CmsAdm(db.Model):
    __tablename__ = 'cms_adm'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    email = db.Column(db.String(30), server_default=db.FetchedValue())
    remark = db.Column(db.String(50), server_default=db.FetchedValue())
    create_time = db.Column(DateTime)
    update_time = db.Column(db.DateTime)

    def hash_password(self, password):
        """密码加密"""
        self.password = sha256_crypt.encrypt(password)

    def verify_password(self, password):
        """校验密码"""
        return sha256_crypt.verify(password, self.password)


class CmsCategory(db.Model):
    __tablename__ = 'cms_category'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    sort = db.Column(db.Integer, server_default=db.FetchedValue())
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue())


class CmsNav(db.Model):
    __tablename__ = 'cms_nav'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    icon = db.Column(db.String(40), nullable=False)
    path = db.Column(db.String(150), server_default=db.FetchedValue())
    level = db.Column(db.Integer, nullable=False)
    sort = db.Column(db.Integer, server_default=db.FetchedValue())
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    children = []


# https://www.jianshu.com/p/4e63bc531da5
class MenuDto():
    def __init__(self, id, name, path, icon, parent_id, children):
        super().__init__()
        self.id = id
        self.name = name
        self.path = path
        self.icon = icon
        self.parent_id = parent_id
        self.children = children

    def __str__(self):
        return '%s(id=%s,name=%s,path=%s,icon=%s,parent_id=%s)' % (
            self.__class__.__name__, self.id, self.name, self.path, self.icon, self.parent_id)

    __repr = __str__


class CmsArticle(db.Model):
    __tablename__ = 'cms_article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, nullable=False)
    category_name = db.Column(db.String(100), nullable=False)
    category_parent_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    thumbnail = db.Column(db.String(200), server_default=db.FetchedValue())
    content = db.Column(db.Text)
    sort = db.Column(db.Integer, server_default=db.FetchedValue())
    status = db.Column(db.Integer, server_default=db.FetchedValue())
    url = db.Column(db.String(150), server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, server_default=db.FetchedValue())
