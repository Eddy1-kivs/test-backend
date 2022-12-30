from flask import Flask, request, jsonify, session, Blueprint

pay = Blueprint('pay', __name__)


class CurrencyCol:
    @staticmethod
    def td_format(content):
        amount = float(content.replace(',', ''))
        locale.setlocale(locale.LC_NUMERIC, 'nl_NL')
        val = locale.format_string('%.2f', float(amount), 1, 1).replace(' ', '.')
        return f'$ {val}'


class Number:
    def verify(self):
        number_string = self.replace("-", "")
        list_number = [int(n) for n in number_string]

        if not list_number[0] == 4:
            return False

        if not list_number[3] - list_number[4] == 1:
            return False

        if not sum(list_number) % 4 == 0:
            return False

        if not int(number_string[0:2]) + int(number_string[6:8]) == 100:
            return False

        return True


@pay.route('/PaymentMethod', methods=['GET', 'POST'])
def add_payment():
    add = request.form
    if add == 'POST' and 'username' in request.form and 'card_number' in request.form and 'card_holder_name' in request.form and 'expiration_date' in request.form and 'cvv' in request.form:
        username = request.form[StringField('username')]
        card_number = request.form[Number('card_number')]
        card_holder_name = request.form[StringField('card_holder_name')]
        expiration_date = request.form[StringField('expiration_date')]
        cvv = request.form[StringField('cvv', validators.length(min=3, max=3))]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        cur.execute("INSERT INTO payments VALUES ( %s,%s,%s,%s,%s,%s)",
                    (username,
                     card_number,
                     card_holder_name,
                     expiration_date,
                     cvv))
        db.commit()
        flash('You have successfully added payment!')
        token = jwt.encode({'payments': username, 'exp': datetime.datetime.utcnow()})
        return jsonify({'token': token})
    return make_response('add payment failed', 401, {'www.Authenticate': 'Basic realm'})

