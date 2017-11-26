from app import app
from app import db
import views,models
#app.run(debug = True)

from posts.blueprint import posts

app.register_blueprint(posts, url_prefix='/articles')

if __name__ == '__main__':
    app.run()

