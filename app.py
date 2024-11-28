from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '284jejsj83sps!83eels'
app.config['MYSQL_DB'] = 'ОСББ'

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page not found"}), 404

@app.route('/owners', methods=['GET'])
def get_owners():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM owners')
    owners = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('owners.html', owners=owners)

@app.route('/owners/add', methods=['POST', 'GET'])
def add_owner():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO owners (name, last_name, phone_number, email) 
            VALUES (%s, %s, %s, %s)
        ''', (name, last_name, phone_number, email))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_owners'))
    return render_template('create_owner.html')

@app.route('/owners/<int:owner_id>/edit', methods=['GET', 'POST'])
def update_owner(owner_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE owners 
            SET name = %s, last_name = %s, phone_number = %s, email = %s 
            WHERE idowners = %s
        ''', (name, last_name, phone_number, email, owner_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_owners'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM owners WHERE idowners = %s', (owner_id,))
    owner = cursor.fetchone()
    cursor.close()
    conn.close()
    if not owner:
        return jsonify({"error": "Owner not found"}), 404
    return render_template('edit_owner.html', owner=owner)

@app.route('/owners/<int:owner_id>/delete', methods=['POST'])
def delete_owner(owner_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM owners WHERE idowners = %s', (owner_id,))
    owner = cursor.fetchone()
    if not owner:
        return jsonify({"error": "Owner not found"}), 404
    cursor.execute('DELETE FROM owners WHERE idowners = %s', (owner_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_owners'))

@app.route('/apartments', methods=['GET'])
def get_apartments():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM apartments')
    apartments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('apartments.html', apartments=apartments)

@app.route('/apartments/create', methods=['GET', 'POST'])
def create_apartment():
    if request.method == 'POST':
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500
        apartment_number = request.form['apartment_number']
        idowners = request.form['idowners']
        floor = request.form['floor']
        area = request.form['area']
        status = request.form['status']
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO apartments (apartment_number, idowners, floor, area, status) 
                VALUES (%s, %s, %s, %s, %s)
            ''', (apartment_number, idowners, floor, area, status))
            conn.commit()
        except mysql.connector.errors.IntegrityError as e:
            return jsonify({"error": "Apartment number already exists"}), 409
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('get_apartments'))
    return render_template('create_apartment.html')

@app.route('/apartments/<int:apartment_id>/edit', methods=['GET', 'POST'])
def update_apartment(apartment_id):
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    if request.method == 'POST':
        apartment_number = request.form.get('apartment_number')
        floor = request.form.get('floor')
        area = request.form.get('area')
        status = request.form.get('status')
        idowners = request.form.get('idowners')
        cursor = conn.cursor()
        cursor.execute('''
                UPDATE apartments 
                SET apartment_number = %s, floor = %s, area = %s, status = %s, idowners = %s
                WHERE idapartments = %s
            ''', (apartment_number, floor, area, status, idowners, apartment_id))
        conn.commit()
        if cursor.rowcount == 0:
            return "Apartment not found", 404
        cursor.close()
        conn.close()
        return redirect(url_for('get_apartments'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM apartments WHERE idapartments = %s', (apartment_id,))
    apartment = cursor.fetchone()
    if apartment is None:
        cursor.close()
        conn.close()
        return "Apartment not found", 404
    cursor.close()
    conn.close()
    return render_template('edit_apartment.html', apartment=apartment)

@app.route('/apartments/<int:apartment_id>/delete', methods=['POST'])
def delete_apartment(apartment_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM apartments WHERE idapartments = %s', (apartment_id,))
    apartment = cursor.fetchone()
    if not apartment:
        return jsonify({"error": "Apartment not found"}), 404
    cursor.execute('DELETE FROM apartments WHERE idapartments = %s', (apartment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_apartments'))

@app.route('/payments', methods=['GET'])
def get_payments():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM payments')
    payments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('payments.html', payments=payments)
@app.route('/payments/create', methods=['GET', 'POST'])
def add_payment():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        idapartments = request.form.get('idapartments')
        payment_type = request.form.get('payment_type')
        sum = request.form.get('sum')
        date = request.form.get('date')
        status = request.form.get('status')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments (idapartments, payment_type, sum, date, status)
            VALUES (%s, %s, %s, %s, %s)
        ''', (idapartments, payment_type, sum, date, status))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_payments'))
    return render_template('create_payment.html')
@app.route('/payments/<int:payment_id>/edit', methods=['GET', 'POST'])
def update_payment(payment_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        payment_type = request.form.get('payment_type')
        sum = request.form.get('sum')
        date = request.form.get('date')
        status = request.form.get('status')
        idapartments = request.form.get('idapartments')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE payments 
            SET payment_type = %s, sum = %s, date = %s, status = %s, idapartments = %s 
            WHERE idpayments = %s
        ''', (payment_type, sum, date, status, idapartments, payment_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_payments'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM payments WHERE idpayments = %s', (payment_id,))
    payment = cursor.fetchone()
    cursor.close()
    conn.close()
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return render_template('edit_payment.html', payment=payment)

@app.route('/payments/<int:payment_id>/delete', methods=['POST'])
def delete_payment(payment_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('DELETE FROM payments WHERE idpayments = %s', (payment_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_payments'))

@app.route('/advertisements', methods=['GET'])
def get_advertisements():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT idAdvertisement, theme, ad_text, date_of_publication, idowners FROM advertisement')
    advertisements = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('advertisements.html', advertisements=advertisements)

@app.route('/advertisements/add', methods=['GET', 'POST'])
def add_advertisement():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        theme = request.form.get('theme')
        ad_text = request.form.get('ad_text')
        date_of_publication = request.form.get('date_of_publication')
        idowners = request.form.get('idowners')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO advertisement (theme, ad_text, date_of_publication, idowners)
            VALUES (%s, %s, %s, %s)
        ''', (theme, ad_text, date_of_publication, idowners))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_advertisements'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM owners')
    owners = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_advertisement.html', owners=owners)

@app.route('/advertisements/<int:ad_id>/edit', methods=['GET', 'POST'])
def update_advertisement(ad_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        theme = request.form.get('theme')
        ad_text = request.form.get('ad_text')
        date_of_publication = request.form.get('date_of_publication')
        idowners = request.form.get('idowners')
        cursor = conn.cursor()
        cursor.execute('''UPDATE advertisement 
                          SET theme = %s, ad_text = %s, date_of_publication = %s, idowners = %s 
                          WHERE idAdvertisement = %s''',
                       (theme, ad_text, date_of_publication, idowners, ad_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_advertisements'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM advertisement WHERE idAdvertisement = %s', (ad_id,))
    advertisement = cursor.fetchone()
    cursor.close()
    conn.close()
    if not advertisement:
        return jsonify({"error": "Advertisement not found"}), 404
    return render_template('edit_advertisement.html', advertisement=advertisement)

@app.route('/advertisements/<int:ad_id>/delete', methods=['POST'])
def delete_advertisement(ad_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('DELETE FROM advertisement WHERE idAdvertisement = %s', (ad_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_advertisements'))

@app.route('/directors', methods=['GET'])
def get_directors():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM acab_director')
    directors = cursor.fetchall()
    cursor.execute('SELECT * FROM owners')
    owners = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('directors.html', directors=directors, owners=owners)

@app.route('/directors/add', methods=['POST', 'GET'])
def add_director():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        took_office = request.form.get('took_office')
        idowners = request.form.get('idowners')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO acab_director (took_office, idowners) 
            VALUES (%s, %s)
        ''', (took_office, idowners))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_directors'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT idowners, name, last_name FROM owners')
    owners = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('create_director.html', owners=owners)

@app.route('/directors/<int:director_id>/edit', methods=['GET', 'POST'])
def update_director(director_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        took_office = request.form.get('took_office')
        idowners = request.form.get('idowners')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE acab_director 
            SET took_office = %s, idowners = %s 
            WHERE idacab_director = %s
        ''', (took_office, idowners, director_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_directors'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM acab_director WHERE idacab_director = %s', (director_id,))
    director = cursor.fetchone()
    cursor.close()
    conn.close()
    if not director:
        return jsonify({"error": "Director not found"}), 404
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT idowners, name, last_name FROM owners')
    owners = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('edit_director.html', director=director, owners=owners)

@app.route('/directors/<int:director_id>/delete', methods=['POST'])
def delete_director(director_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM acab_director WHERE idacab_director = %s', (director_id,))
    director = cursor.fetchone()
    if not director:
        return jsonify({"error": "Director not found"}), 404
    cursor.execute('DELETE FROM acab_director WHERE idacab_director = %s', (director_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_directors'))

@app.route('/meetings', methods=['GET'])
def get_meetings():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT idmeetings_of_the_ACAB, date_start, purpose_of_the_meeting FROM meetings_of_the_acab')
    meetings = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('meetings_of_the_ACAB.html', meetings=meetings)

@app.route('/meetings/add', methods=['GET', 'POST'])
def add_meeting():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        date_start = request.form.get('date_start')
        purpose_of_the_meeting = request.form.get('purpose_of_the_meeting')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO meetings_of_the_acab (date_start, purpose_of_the_meeting)
            VALUES (%s, %s)
        ''', (date_start, purpose_of_the_meeting))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_meetings'))
    return render_template('add_meeting.html')

@app.route('/meetings/<int:meeting_id>/edit', methods=['GET', 'POST'])
def update_meeting(meeting_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        date_start = request.form.get('date_start')
        purpose_of_the_meeting = request.form.get('purpose_of_the_meeting')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE meetings_of_the_ACAB 
            SET date_start = %s, purpose_of_the_meeting = %s
            WHERE idmeetings_of_the_ACAB = %s
        ''', (date_start, purpose_of_the_meeting, meeting_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_meetings'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM meetings_of_the_ACAB WHERE idmeetings_of_the_ACAB = %s', (meeting_id,))
    meeting = cursor.fetchone()
    cursor.close()
    conn.close()
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    return render_template('edit_meeting.html', meeting=meeting)

@app.route('/meetings/<int:meeting_id>/delete', methods=['POST'])
def delete_meeting(meeting_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('DELETE FROM meetings_of_the_acab WHERE idmeetings_of_the_ACAB = %s', (meeting_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_meetings'))

@app.route('/service_providers', methods=['GET'])
def get_service_providers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM service_providers')
    providers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('service_providers.html', providers=providers)

@app.route('/service_providers/add', methods=['GET', 'POST'])
def add_service_provider():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        service_providerscol = request.form.get('service_providerscol')
        phone_number = request.form.get('phone_number')
        services = request.form.get('services')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO service_providers (service_providerscol, phone_number, services)
            VALUES (%s, %s, %s)
        ''', (service_providerscol, phone_number, services))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_service_providers'))
    return render_template('add_service_provider.html')

@app.route('/service_providers/<int:provider_id>/edit', methods=['GET', 'POST'])
def update_service_provider(provider_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        service_providerscol = request.form.get('service_providerscol')
        phone_number = request.form.get('phone_number')
        services = request.form.get('services')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE service_providers 
            SET service_providerscol = %s, phone_number = %s, services = %s 
            WHERE idservice_providers = %s
        ''', (service_providerscol, phone_number, services, provider_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_service_providers'))
    cursor = conn.cursor(dictionary=True)  # Додаємо dictionary=True тут
    cursor.execute('SELECT * FROM service_providers WHERE idservice_providers = %s', (provider_id,))
    provider = cursor.fetchone()
    cursor.close()
    conn.close()
    if not provider:
        return jsonify({"error": "Service provider not found"}), 404
    return render_template('edit_service_provider.html', provider=provider)

@app.route('/service_providers/<int:provider_id>/delete', methods=['POST'])
def delete_service_provider(provider_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('DELETE FROM service_providers WHERE idservice_providers = %s', (provider_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_service_providers'))

@app.route('/special_services', methods=['GET'])
def get_special_services():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM special_services_and_repairs')
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('special_services_and_repairs.html', services=services)

@app.route('/special_services/add', methods=['GET', 'POST'])
def add_special_service():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        services_type = request.form.get('services_type')
        date_start = request.form.get('date_start')
        end_date = request.form.get('end_date')
        price = request.form.get('price')
        idservice_providers = request.form.get('idservice_providers')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO special_services_and_repairs (services_type, date_start, end_date, price, idservice_providers)
            VALUES (%s, %s, %s, %s, %s)
        ''', (services_type, date_start, end_date, price, idservice_providers))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_special_services'))
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM service_providers')
    providers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_special_service.html', providers=providers)

@app.route('/special_services/<int:service_id>/edit', methods=['GET', 'POST'])
def update_special_service(service_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    if request.method == 'POST':
        services_type = request.form.get('services_type')
        date_start = request.form.get('date_start')
        end_date = request.form.get('end_date')
        price = request.form.get('price')
        idservice_providers = request.form.get('idservice_providers')
        cursor = conn.cursor()
        cursor.execute(''' 
            UPDATE special_services_and_repairs 
            SET services_type = %s, date_start = %s, end_date = %s, price = %s, idservice_providers = %s 
            WHERE idspecial_services_and_repairs = %s
        ''', (services_type, date_start, end_date, price, idservice_providers, service_id))  # Використання service_id тут
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('get_special_services'))
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM special_services_and_repairs WHERE idspecial_services_and_repairs = %s', (service_id,))
    service = cursor.fetchone()
    cursor.close()
    conn.close()
    if not service:
        return jsonify({"error": "Service not found"}), 404
    return render_template('edit_special_service.html', special_service=service)  # Передайте service тут

@app.route('/special_services/<int:service_id>/delete', methods=['POST'])
def delete_special_service(service_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()
    cursor.execute('DELETE FROM special_services_and_repairs WHERE idspecial_services_and_repairs = %s', (service_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('get_special_services'))

if __name__ == '__main__':
    app.run(debug=True)
