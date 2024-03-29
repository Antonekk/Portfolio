#Antoni Strasz


from __future__ import annotations
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, ForeignKey,String, Boolean,create_engine
from sqlalchemy.orm import relationship, mapped_column,Mapped,sessionmaker
from sqlalchemy.orm import validates
import datetime
import re
import argparse
from typing import List
from flask import Flask, request, jsonify
from DatabaseFunc import Znajomy,Wypozyczenie,Ksiazka,dodaj_znajomego,inicjalizuj



app = Flask(__name__)

base = declarative_base()



session = inicjalizuj()


#Operacje CRUD dla Tabeli Znajomych

# Endpoint do pobierania wszystkich użytkowników
@app.route('/api/users', methods=['GET'])
def get_all_users():
    znajomi = session.query(Znajomy)
    return jsonify(json_list = [ znajomy.serialize() for znajomy in znajomi.all()])


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = session.query(Znajomy).filter_by(id=user_id).first()
    if user is not None :
        return jsonify(user.serialize())
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/api/users', methods=['POST'])
def add_user():
    new_user = request.json
    print(new_user)
    znajomy_id = dodaj_znajomego(session,new_user['imie'],new_user['nazwisko'],new_user['email'])
    if znajomy_id:
        return jsonify({'Success': 'Friend succesfully added'})
    else:
        return jsonify({'error': 'Cant add user'}), 404


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_data = request.json
    user = session.query(Znajomy).filter_by(id=user_id).first()
    if user is not None:
        user.imie = updated_data["imie"]
        user.nazwisko = updated_data["nazwisko"]
        user.email = updated_data["email"]
        session.commit
        return jsonify({'Success': 'Succesfully updated'})
    else:
        return jsonify({'error': 'User not found'}), 404



@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = session.query(Znajomy).filter_by(id=user_id)
    if user.first() is not None:
        user.delete()
        session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404



