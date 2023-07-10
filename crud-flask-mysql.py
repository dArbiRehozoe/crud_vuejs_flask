from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# MySQL connection configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'projetvu'

# Create connection to the MySQL database
db = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create the 'location' table if it doesn't exist
# create_table_query = """
# CREATE TABLE IF NOT EXISTS locations (
#     id INT AUTO_INCREMENT PRIMARY KEY,
#     author VARCHAR(255),
#     title VARCHAR(255),
#     isbn INT
# )
# """
# cursor.execute(create_table_query)


# Route to get all location
@app.route('/location', methods=['GET'])
def get_location():
    select_query = "SELECT * FROM location"
    cursor.execute(select_query)
    location = cursor.fetchall()
    
    # Convert the result to a list of dictionaries
    location_list = []
    for loc in location:
        location_dict = {
            'numloc': loc[0],
            'nom_loc': loc[1],
            'design_voiture': loc[2],
            'Nombre_de_jours': loc[3],
            'taux_journalier': loc[4],
        }
        location_list.append(location_dict)
    
    return jsonify(location_list)


# Route to add a new location
@app.route('/add_location', methods=['POST'])
def add_location():
    location_data = request.get_json()
    nom_loc = location_data.get('nom_loc')
    design_voiture = location_data.get('design_voiture')
    Nombre_de_jours= location_data.get("Nombre_de_jours")
    taux_journalier= location_data.get("taux_journalier")


    insert_query = "INSERT INTO location (nom_loc,design_voiture,Nombre_de_jours,taux_journalier) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert_query, (nom_loc,design_voiture,Nombre_de_jours,taux_journalier))
    db.commit()
    
    return jsonify({'message': 'location added successfully'}), 201



# Route to update an existing location
@app.route('/update_location/<int:numloc>', methods=['PUT'])
def update_location(numloc):
    location_data = request.get_json()
    nom_loc = location_data.get('nom_loc')
    design_voiture = location_data.get('design_voiture')
    Nombre_de_jours= location_data.get("Nombre_de_jours")
    taux_journalier= location_data.get("taux_journalier")

    update_query = "UPDATE location SET nom_loc=%s ,design_voiture=%s ,Nombre_de_jours=%s,taux_journalier=%s WHERE numloc=%s"
    cursor.execute(update_query, (nom_loc,design_voiture,Nombre_de_jours,taux_journalier,numloc))
    db.commit()
    
    return jsonify({'message': 'Book updated successfully'})


# Route to delete a location
@app.route('/delete_location/<int:numloc>', methods=['DELETE'])
def delete_location(numloc):
    delete_query = "DELETE FROM location WHERE numloc=%s"
    cursor.execute(delete_query, numloc)
    db.commit()
    
    return jsonify({'message': 'Book deleted successfully'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

