import unittest
import re
import app as mainModule
from flask_mail import Message
from datetime import datetime
from forms import AddNoteForm
from app import Notes, mail, db, app
from flask import render_template
from dotenv import load_dotenv

app.testing = True

class EndPointsCase(unittest.TestCase):
  def setUp(self):
    self.app = app
    self.app.config['UPLOAD_FOLDER'] = 'storage'
    self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    self.app_context = self.app.app_context()
    self.app_context.push()
    self.client = app.test_client()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_landing_page(self):
    response = self.client.get('/', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  def test_add_note_page(self):
    response = self.client.get('/add', follow_redirects=True)
    self.assertEqual(response.status_code, 200)

  def test_submit_new_note(self):
    form = {
      'subjectTitle': 'Testing',
      'subjectName': 'Software Engineering',
      'chapterName': 'Unittest',
      'link': 'https://example.com',
      'semester': 5
    }
    response = self.client.post('/add', data=form,
               content_type='multipart/form-data')
    self.assertEqual(response.status_code, 302)

  def test_notes_view(self):
    note = Notes(
      subjectName='Software Engineering',
      subjectTitle='Testing',
      chapterName='Unittest',
      semester=5,
      link ='https://example.com'
    )
    db.session.add(note)
    db.session.commit()

    form = {
      'semester': 5,
      'email': 'test@example.com',
      'name': 'Test'
    }
    response = self.client.post('/notes', data=form,
                content_type='multipart/form-data')
    self.assertEqual(response.status_code, 200)

  # def test_download_and_send(self):
  #   n = Notes(
  #     subjectName='Software Engineering',
  #     subjectTitle='Testing',
  #     chapterName='Unittest',
  #     semester=5,
  #     link ='https://example.com'
  #   )
  #   db.session.add(n)
  #   db.session.commit()


class NotesModelCase(unittest.TestCase):
  def setUp(self):
    self.app = app
    self.app.config['UPLOAD_FOLDER'] = 'storage'
    self.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    self.app_context = self.app.app_context()
    self.app_context.push()
    self.client = app.test_client()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_db_model(self):
    n = Notes(      
      subjectName='Software Engineering',
      subjectTitle='Testing',
      chapterName='Unittest',
      semester=6,
      link ='https://example.com'
    )
    db.session.add(n)
    db.session.commit()

    note = Notes.query.get(1)
    self.assertEqual(note,n)


if __name__ == '__main__':
    unittest.main(verbosity=2)