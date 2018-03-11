from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_login import UserMixin


@login.user_loader()
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    '''
    User table.

    Contains basic user account information only.
    '''
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.nickname)


class Group(db.Model):
    """
    Group table

    Groups contain Contribs by Users, which are grouped into Songbooks. Users
    in the group have Roles, which are recorded in the Membership table.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)


class Membership(db.Model):
    """
    Membership table

    Associates Users who are members of a Group, and their Role in the Group..
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<Membership {user} {role} {group}>'.format({
            'user': self.user_id,
            'role': self.role_id,
            'group': self.group_id
        })


class Role(db.Model):
    """
    Role Table

    List of Group Roles, principally `Admin`, `Moderator`, `Default`
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))

    def __repr__(self):
        return '<Role {}'.format(self.name)


class Song(db.Model):
    """
    Song table

    Contains Song metadata only. Up-to-date versions of a song are stored in
    Body, and historical edits are stored in Edit
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Song {title} - {artist}>'.format({
            'title': self.title,
            'artist': self.artist
        })


class Body(db.Model):
    """
    Body table

    Contains raw text used to render a version of a song. The name should
    describe the version, and not repeat the song metadata. If empty, it will
    default to 'Default'

    Good names might be:
    - 'Beginner version'
    - '100% super-pedantic hard version'
    - 'Crazy jazz re-harm.'

    Bad names are things like:
    - 'Bad moon rising' -- This repeats the metadata
    - 'C Major Version' -- Use transposition tools instead of a new version
    - 'Artist So-and-so cover' -- Submit a new song with the covering artist
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    name = db.Column(db.String(50))
    body = db.Column(db.String(10000))
    revision = db.column(db.Integer())

    def __repr__(self):
        return '<Body>'


class Edit(db.Model):
    """
    Edit table

    Records all edits made to song Bodies with git-style diffs. Edits are
    submitted by a user, and approved by a mod.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mod_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body_id = db.Column(db.Integer, db.ForeignKey('body.id'))
    diff = db.column(db.String(10000))
    revision = db.column(db.Integer())

    def __repr__(self):
        return '<Edit {body_id} {version}'.format({
            'body_id': self.body_id,
            'timestamp': self.version
        })


class Contrib(db.Model):
    """
    Contrib table

    Records Songs contributed by Users to Groups, so other Group members can
    view, suggest edits, etc.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))


class Songbook(db.Model):
    """
    Songbook table

    Records Songbook metadata only. Songbook listings are in the Entries table.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    name = db.Column(db.String(50))
    revision = db.column(db.Integer())


class Entry(db.Model):
    """
    Entry table

    Records the songs added to a Songbook.
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    songbook_id = db.Column(db.Integer, db.ForeignKey('songbook.id'))
