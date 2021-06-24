from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # ფლასკ კლასის ობიექტი(აპლიკაცია).  _name_ არის წინასწარ შექმნილი ცვლადი,
# რომლის მნიშვნელობაა გამშვები ფაილის დასახელება.

app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite'
# შემოვიღოთ sqlalchemy კლასის ობიექტი, რომლითაც შემდეგ ვიმუშავებთ ბაზასთან
db = SQLAlchemy(app)


# კლასის შექმნა bazis
class Animes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"""Anime title:{self.title}; Rating: {self.rating}; Ranking: {self.ranking}"""


# b1 = Books.query.first() #erti selecti
# print(b1)


# yvelas select

# all_books = Books.query.all()
# print(all_books)
# for each in all_books:
#     print(each)

# gafiltruli select
# all_books = Animes.query.filter_by(author='აკაკი წერეთელი').all()
# print(all_books)
# for each in all_books:
#     print(each)


# db.create_all() # ეს ბრძანება გამოიყენება მაშინ, როცა ბაზა არ გვაქვს ჯერ. და შექმნის ამ ბაზას კლასის სტრუქტურით.
# # ხოლო თუ გვაქვს, არ შეიქმნება.

# insertebi
# b1 = Books(title='ლექსები', author='ილია', price=15)
# db.session.add(b1)
# db.session.commit()

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')  # მთავარი გვერდის html-ის დარენდერებული ვერსიის დაბრუნება



#davamato ro paroli rtuli unda iyosssss
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "" or password == "":
            flash("შეავსეთ ყველა ველი")
        else:
            session['username'] = username
            return redirect(url_for('user'))
        # url for ფუნქცია ააგებს იუზერზე იუერელს და მოახდენს რედაირექთს მასზე.
    else:
        return render_template('login.html')

    return render_template('login.html')


@app.route('/user')
def user():
    animes = ['Fullmetal Alchemist: Brotherhood', 'Death Note', 'Attack On Titan', 'Hunter X Hunter',
              'Samurai Champloo', 'Naruto', 'Kuroko\'s Basketball']
    return render_template('user.html', animes=animes)  # იუზერის html-ის დარენდერება.


# სახელისა და ასაკის რუთი
@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        rk = request.form['ranking']
        t = request.form['title']
        r = request.form['rating']
        if rk == "" or t == "" or r == "":
            flash("შეავსეთ ყველა ველი")
        elif not r.isnumeric():
            flash("ფასი უნდა იყოს რიცხვითი მონაცემი")
        else:
            b = Animes(ranking=rk, title=t, rating=float(r))
            db.session.add(b)
            db.session.commit()
            flash('მონაცემები დამატებულია')
    return render_template('animes.html')


# აპლიკაციის გაშვება run მეთოდით მოხდება მხოლოდ მაშინ, როცა ეს ფაილი იქნება მთავარი გამშვები ფაილი
if __name__ == "__main__":
    app.run(debug=True)
