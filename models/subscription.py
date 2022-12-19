from flask import Flask, request, jsonify, session, Blueprint

subs = Blueprint('subs', __name__)


@subs.route('/subscription', methods=['GET', 'POST'])
def subscription():
    subscribe = request.form
    if subscribe == 'POST' and 'username' in request.form and 'current_plan' in request.form and 'plan_amount' in request.form and 'card_number' in request.form and 'created_at' in request.form:
        username = request.form[StringField('username')]
        current_plan = request.form[StringField('current_plan')]
        plan_amount = request.form[CurrencyCol('plan_amount')]
        card_number = request.form[Number('card_number')]
        created_at = request.form[StringField('created_at')]
        cur = DATABASE.connection.cursor(DATABASE.cursors.DictCursor)
        cur.execute("INSERT INTO subscriptions VALUES (%s,%s,%s,%s,%s,%s)",
                    (username, plan_amount,
                     card_number, created_at,
                     created_at))
        DATABASE.commit()
        flash('You have successfully subscribed!')
        token = jwt.encode({'subscriptions': username, 'exp': datetime.datetime.utcnow()})
        return jsonify({'token': token})
    return make_response('subscription failed', 401, {'www.Authenticate': 'Basic realm'})

