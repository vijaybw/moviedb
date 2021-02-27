import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import hashlib
#from werkzeug import generate_password_hash, check_password_hash

@app.route('/add', methods=['POST'])
def add_user():
    try:
        _json = request.json
        _username = _json['username']
        _firstname = _json['firstname']
        _lastname = _json['lastname']
        _email = _json['email']
        _gender = _json['gender']
        _age = _json['age']
        _password = _json['password']
        # validate the received values
        if _username and _email and _password and request.method == 'POST':

            args = [_username, _firstname, _lastname, _email, _gender, _age, _password]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_CreateUser', args)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/users')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM tbl_users")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user')
def user():
    try:
        username = request.args.get('username')
        userpassword = request.args.get('userpassword')
        args = [username, userpassword]
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.callproc("sp_LoginUser", args)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/userfollowing/<string:username>')
def user_following(username):
    try:
        args = [username]
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.callproc('sp_GetUserFollowing', args)
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/userfollowers/<string:username>')
def user_followers(username):
    try:
        args = [username]
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.callproc('sp_GetUserFollowers', args)
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/followuser', methods=['POST'])
def follow_user():
    try:
        _json = request.json
        _username = _json['username']
        _followername = _json['followername']
        # validate the received values
        if _username and _followername and request.method == 'POST':
            args = [_username, _followername]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_FollowUser', args)
            conn.commit()
            resp = jsonify('User followed successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/unfollowuser', methods=['POST'])
def unfollow_user():
    try:
        _json = request.json
        _username = _json['username']
        _followername = _json['followername']
        # validate the received values
        if _username and _followername and request.method == 'POST':
            args = [_username, _followername]
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_UnfollowUser', args)
            conn.commit()
            resp = jsonify('User unfollowed successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/delete/<string:username>')
def delete_user(username):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tbl_users WHERE user_name=%s", (username,))
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run()