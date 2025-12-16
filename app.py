from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import get_db_connection

app = Flask(__name__)
app.secret_key = "sy"


@app.get("/")
def index():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return render_template(
        "index.html",
        title="Flask booksㅤ",
        books=books
    )


@app.get("/about/<int:id>/")
def get_about(id):
    conn = get_db_connection()
    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (id,)).fetchone()
    conn.close()

    if not book:
        return "Книгу не знайдено", 404

    return render_template(
        "about.html",
        book=book,
        title=book["title"]
    )


@app.get("/cart/")
def cart():
    cart_ids = session.get("cart", [])

    if not cart_ids:
        return render_template("cart.html", books=[], total=0)

    placeholders = ",".join("?" * len(cart_ids))

    conn = get_db_connection()
    books = conn.execute(f"SELECT * FROM books WHERE id IN ({placeholders})", cart_ids).fetchall()
    conn.close()

    total = sum(book["price"] for book in books)

    return render_template(
        "cart.html",books=books, total=total, title="Flask books")


@app.get("/add_to_cart/<int:id>/")
def add_to_cart(id):
    cart = session.get("cart", [])
    if id not in cart:
        cart.append(id)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.get("/remove_from_cart/<int:id>/")
def remove_from_cart(id):
    cart = session.get("cart", [])
    if id in cart:
        cart.remove(id)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.get("/add/")
def add_book_form():
    return render_template("add.html", title="Flask booksㅤ")


@app.get("/info/")
def info():
    return render_template('info.html', title="Flask booksㅤ")


@app.post("/add/")
def add_book_submit():
    title = request.form["title"]
    description = request.form["description"]
    picture = request.form["picture"]
    price = request.form["price"]
    rate = request.form["rate"]
    country = request.form["country"]

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO books (title, description, picture, price, rate, country)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, picture, price, rate, country))
    conn.commit()
    conn.close()

    flash("Книгу додано")
    return redirect(url_for("index"))


@app.get("/edit/<int:id>/")
def edit_book_form(id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    conn.close()

    if not book:
        flash("Книга не знайдена")
        return redirect(url_for("index"))

    return render_template("edit.html", book=book, title="Flask booksㅤ")


@app.post("/edit/<int:id>/")
def edit_book_submit(id):
    conn = get_db_connection()
    conn.execute("""
        UPDATE books
        SET title=?, description=?, picture=?, price=?, rate=?, country=?
        WHERE id=?
    """, (
        request.form["title"],
        request.form["description"],
        request.form["picture"],
        request.form["price"],
        request.form["rate"],
        request.form["country"],
        id
    ))
    conn.commit()
    conn.close()
    flash("Книгу оновлено")
    return redirect(url_for("view_book", id=id))


@app.get("/delete/<int:id>/")
def delete_book_confirm(id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("delete.html", book=book)


@app.post("/delete/<int:id>/")
def delete_book(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Книгу видалено")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(port=9110, debug=True)
