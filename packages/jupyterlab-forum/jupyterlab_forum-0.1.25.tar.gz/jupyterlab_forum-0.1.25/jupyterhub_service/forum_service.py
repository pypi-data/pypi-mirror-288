import logging
import argparse
import json
import os
from urllib.parse import urlparse
import sqlite3
from tornado import escape
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, authenticated

from jupyterhub.services.auth import HubAuthenticated


class ForumRequestHandler(HubAuthenticated, RequestHandler):


    def initialize(self):

      self.db_path = '/opt/forum-database/forumbase.db'
      self.ensure_db_exists()

    def ensure_db_exists(self):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        # Check if the database exists
        if not os.path.exists(self.db_path):
            # Create a new database and tables
            self.create_database()
    def create_database(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Create Themes table
        cursor.execute('''
            CREATE TABLE Themes (
                ThemeID INTEGER PRIMARY KEY AUTOINCREMENT,
                Title TEXT NOT NULL,
                Author TEXT NOT NULL,
                CreationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                Status TEXT NOT NULL,
                Description TEXT,
                Sticky BOOLEAN DEFAULT FALSE,
                Commentable BOOLEAN DEFAULT FALSE
            )
        ''')

        # Create Replies table
        cursor.execute('''
            CREATE TABLE Replies (
                ReplyID INTEGER PRIMARY KEY AUTOINCREMENT,
                Author TEXT NOT NULL,
                Content TEXT NOT NULL,
                CreationTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ThemeID INTEGER,
                FOREIGN KEY(ThemeID) REFERENCES Themes(ThemeID)
            )
        ''')

        connection.commit()
        connection.close()

    def _read_forum_overview(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Get all themes from the Themes table
            cursor.execute("SELECT ThemeID, Title, Author, CreationTime, Status,Sticky,Commentable FROM Themes")
            themes = cursor.fetchall()

            # Get all replies for each theme from the Replies table
            overview = []
            for theme in themes:
                overview.append({
                    'ThemeID': theme[0],
                    'Title': theme[1],
                    'Author': theme[2],
                    'CreationTime': theme[3],
                    'Status': theme[4],
                    'Sticky': theme[5],
                    'Commentable': theme[6],
                })

            return overview

    def write_to_json(self, doc):
        """Write dictionary document as JSON"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(escape.utf8(json.dumps(doc)))
    @authenticated
    def get(self):
      logging.info("Authenticated user: %s", self.current_user)
      overview = self._read_forum_overview()
      overview_dict = {'themes': overview}

      self.write_to_json(overview_dict)

    @authenticated
    def post(self):
      try:
          theme_id = int(json.loads(self.request.body)['ThemeID'])
      except (json.JSONDecodeError, KeyError, ValueError):
          self.set_status(400, "Invalid ThemeID")
          return

      with sqlite3.connect(self.db_path) as conn:
          cursor = conn.cursor()

          # Fetch theme details
          cursor.execute("SELECT * FROM Themes WHERE ThemeID = ?", (theme_id,))
          theme = cursor.fetchone()

          if not theme:
              self.set_status(404, "Theme not found")
              return

          # Fetch replies for the theme
          cursor.execute("SELECT * FROM Replies WHERE ThemeID = ?", (theme_id,))
          replies = cursor.fetchall()

          replies = [
              {
                  'Author': reply[1],
                  'Content': reply[2],
                  'CreationTime': reply[3]
              } for reply in replies
          ]

          # Construct response data
          theme_details = {
              'Title': theme[1],
              'Author': theme[2],
              'CreationTime': theme[3],
              'Status': theme[4],
              'Description': theme[5],
              'Sticky': theme[6],
              'Commentable': theme[7],
              'Replies': replies
          }

          self.write_to_json(theme_details)


class CreateThemeHandler(HubAuthenticated, RequestHandler):


    def initialize(self):
      self.db_path = '/opt/forum-database/forumbase.db'


    def write_to_json(self, doc):
        """Write dictionary document as JSON"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(escape.utf8(json.dumps(doc)))


    @authenticated
    def post(self):

      try:
          newtheme = json.loads(self.request.body)
      except (json.JSONDecodeError, KeyError, ValueError):
          self.set_status(400, "Invalid new Theme")
          return

      with sqlite3.connect(self.db_path) as conn:
          cursor = conn.cursor()

          # Fetch theme details
          cursor.execute('''
              INSERT INTO Themes (Title, Author, Status, Description, Sticky, Commentable)
              VALUES (?, ?, ?, ?, ?, ?)
          ''', (newtheme["Title"], newtheme["Author"], newtheme["Status"], newtheme["Description"], newtheme["Sticky"],>

          if not newtheme:
              self.set_status(404, "Theme not found")
              return
          last_row_id = cursor.lastrowid

          # Retrieve the last inserted row
          cursor.execute(f"SELECT * FROM Themes WHERE rowid = ?", (last_row_id,))
          last_row = cursor.fetchone()


          # Construct response data
          theme_details = {
              'ThemeID': last_row[0],
          }

          self.write_to_json(theme_details)


class ReplyHandler(HubAuthenticated, RequestHandler):

    def initialize(self):
      self.db_path = '/opt/forum-database/forumbase.db'

    def write_to_json(self, doc):
        """Write dictionary document as JSON"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(escape.utf8(json.dumps(doc)))
    @authenticated
    def post(self):
      try:
          newreply = json.loads(self.request.body)
      except (json.JSONDecodeError, KeyError, ValueError):
          self.set_status(400, "Invalid new Theme")
          return

      with sqlite3.connect(self.db_path) as conn:
          cursor = conn.cursor()

          # Fetch theme details
          cursor.execute('''
              INSERT INTO Replies (ThemeID, Content, Author)
              VALUES (?, ?, ?)
          ''', (newreply["ThemeID"], newreply["Content"], newreply["Author"]))

          if not newreply:
              self.set_status(404, "Theme not found")
              return

          self.write_to_json({"message": "Reply updated successfully", "Authenticated user":self.current_user})

class DeleteThemeHandler(HubAuthenticated, RequestHandler):

    def initialize(self):
      self.db_path = '/opt/forum-database/forumbase.db'
    def write_to_json(self, doc):

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(escape.utf8(json.dumps(doc)))
    @authenticated
    def delete(self):
        try:
            request_data = json.loads(self.request.body)
            theme_id = request_data.get("ThemeID")
            if not theme_id:
                self.set_status(400, "ThemeID is required")
                return

        except (json.JSONDecodeError, KeyError, ValueError):
            self.set_status(400, "Invalid request")
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Themes WHERE ThemeID = ?', (theme_id,))
            conn.commit()

        self.write_to_json({"message": "Theme deleted successfully"})

class ToggleStatusHandler(HubAuthenticated, RequestHandler):

    def initialize(self):
        self.db_path = '/opt/forum-database/forumbase.db'

    def write_to_json(self, doc):
        """Write dictionary document as JSON"""
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(escape.utf8(json.dumps(doc)))
    @authenticated
    def patch(self):
        try:
            request_data = json.loads(self.request.body)
            theme_id = request_data.get("ThemeID")
            new_status = request_data.get("Status")
            if not theme_id or not new_status:
                self.set_status(400, "ThemeID and Status are required")
                return

        except (json.JSONDecodeError, KeyError, ValueError):
            self.set_status(400, "Invalid request")
            return

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE Themes SET Status = ? WHERE ThemeID = ?', (new_status, theme_id))
            conn.commit()

        self.write_to_json({"message": "Theme status updated successfully"})

def main():
    args = parse_arguments()
    application = create_application(**vars(args))
    application.listen(args.port)
    IOLoop.current().start()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-prefix",
        "-a",
        default=[os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/"),
                 os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/") + "createtheme",
                 os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/") + "replytheme",
                 os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/") + "deletetheme",
                 os.environ.get("JUPYTERHUB_SERVICE_PREFIX", "/") + "togglestatus"],
        help="application API prefix",
    )
    parser.add_argument(
        "--port", "-p", default=8010, help="port for API to listen on", type=int
    )
    return parser.parse_args()

handler_list = [
                ForumRequestHandler,
                CreateThemeHandler,
                ReplyHandler,
                DeleteThemeHandler,
                ToggleStatusHandler
               ]

def create_application(api_prefix=["/","/test"], handler=handler_list, **kwargs):

    return Application([(i,j) for i ,j in zip(api_prefix, handler)])


if __name__ == "__main__":
    main()
