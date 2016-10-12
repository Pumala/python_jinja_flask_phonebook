from flask import Flask, render_template, request, redirect
import pg

db = pg.DB(dbname='phonebook_app2')
app = Flask('MyApp')

@app.route('/')
def render_home():
    return redirect('/new_entry')
    # return '<h1>Welcome to the Phonebook!</h1>'

@app.route('/print_all_entries')
def print_all():
    query = db.query('select * from phonebook')

    return render_template(
        'all_entries.html',
        title='Entries',
        contact_list = query.namedresult()
    )

@app.route('/update_entry')
def update_entry():
    id = request.args.get('id')
    # print "Id: %s" % id
    query = db.query("select * from phonebook where id = '%s'" % id)
    # query = db.query("select * from phonebook where id = '%s'" % id).namedresult()
    print "Query: %r" % query

    return render_template(
        'update.html',
        contact_list = query.namedresult()
    )

@app.route('/submit_updated_entry', methods=['POST'])
def submit_update():
    contact_id = request.form.get('id')
    name = request.form.get('name')
    cell_number = request.form.get('cell_number')
    email = request.form.get('email')
    action = request.form.get('action')
    print "ACTION: %r" % action
    if action == 'update':
        db.update(
            'phonebook', {
                'id': contact_id,
                'name': name,
                'cell_number': cell_number,
                'email': email
            }
        )
    else:
        print "Hi!!"
        db.delete('phonebook', {'id': contact_id})
    return redirect('/print_all_entries')

@app.route('/submit_new_entry', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    cell_number = request.form.get('cell_number')
    email = request.form.get('email')
    db.insert(
        'phonebook',
        name=name,
        cell_number=cell_number,
        email=email
    )
    return redirect('/new_entry')

@app.route('/new_entry')
def projects():
    query = db.query('select * from phonebook')

    return render_template(
        'index.html',
        title='Entries',
        contact_list = query.namedresult()
    )

if __name__ == '__main__':
    app.run(debug=True)
