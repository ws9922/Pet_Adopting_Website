from app import db
import time
def authenticate(UID:int, Input_PWD:str) -> bool:
    conn = db.connect()
    query = "Select* from Users where UID = {};".format(UID)
    result = conn.execute(query).fetchall()
    conn.close()
    print(result)
    password = result[0][1]
    if Input_PWD == password:
        return True
    return False

def get_user_id(UID:int) -> int:
    conn = db.connect()
    query = "Select UID from Users where UID = {};".format(UID)
    result = conn.execute(query).fetchall()
    conn.close()
    print(result[0][0])
    return result[0][0]

def signup_user(UID:int, Password:str):
    conn = db.connect()
    query = "Insert ignore Into Users(UID, passwd) values ({},{});".format(UID, Password)
    try:
        conn.execute(query)
    except:
        print(query+' execute error')
    conn.close()
    

def fetch_pet() -> dict:
    conn = db.connect()
    query_results = conn.execute("Select pet_id, pet_type, color, pet_condition, location from Pet natural join Shelter where (pet_condition='Normal' or pet_condition='Sick') limit 50;").fetchall()
    conn.close()
    pet_list = []
    for result in query_results:
        item = {
            "pet_id": result[0],
            "pet_type": result[1],
            "color": result[2],
            "pet_condition": result[3],
            "location": result[4]
        }
        pet_list.append(item)
    return pet_list

def fetch_top() -> dict:
    conn = db.connect()
    query_results = conn.execute("select pet_type, color, count(*) as num_pet from Pet natural join Shelter where location like '%%Austin%%' and pet_condition = 'Normal' group by pet_type, color order by num_pet desc limit 6;").fetchall()
    conn.close()
    pet_list = []
    for result in query_results:
        item = {
            "pet_type": result[0],
            "color": result[1],
            "number": result[2]
        }
        pet_list.append(item)
    return pet_list

def search_pet_(pet_id: str) -> dict:
    conn = db.connect()
    query = "select pet_type,user_num,heal_num from (select pet_type,count(distinct UID) as user_num from User_preference where color like '%%{}%%' group by pet_type) as u natural join (select pet_type,count(distinct pet_id) as heal_num from Pet where color like '%%{}%%' and pet_condition = 'Normal' group by pet_type) as p;".format(pet_id,pet_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    pet_list = []
    for result in query_results:
        item = {
            "pet_type": result[0],
            "num_user": result[1],
            "num_heal": result[2]
        }
        pet_list.append(item)
    return pet_list

def search_pet(pet_id: str) -> dict:
    conn = db.connect()
    query = "Select pet_id, pet_type, color, pet_condition, shelter_status, location from Pet natural join Shelter where ((color like '%%{}%%') and (pet_condition='Normal' or pet_condition='Sick')) limit 20;".format(pet_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    pet_list = []
    for result in query_results:
        item = {
            "pet_id": result[0],
            "pet_type": result[1],
            "color": result[2],
            "pet_condition": result[3],
            "status": result[4],
            "location": result[5]
        }
        pet_list.append(item)
    return pet_list


def remove_pet_by_id(pet_id: int) -> None:
    conn = db.connect()
    
    query = "Delete from Pet where pet_id={};".format(pet_id)
    try:
        conn.execute(query)
    except:
        print(query+' execute error')
    conn.close()

def update_condition_entry(pet_id: int, text: str) -> None:
    conn = db.connect()
    query = 'Update Pet set pet_condition = "{}" where pet_id = {};'.format(text, pet_id)
    print(query)
    conn.execute(query)
    conn.close()

def insert_new_pet(pet_id: str, pet_type: str, pet_color: str, pet_cond: str, pet_uid:str, pet_loc:str) -> None:
    conn = db.connect()
    query = 'Insert ignore Into Pet (pet_id, pet_type, color, pet_condition, intake_age, intake_time, shelter_id, UID) VALUES ({}, "{}", "{}", "{}", 0, "2000-1-1", "{}", {});'.format(pet_id, pet_type, pet_color, pet_cond, pet_loc, pet_uid)
    print(query)
    conn.execute(query)
    conn.close()

def insert_new_pre(pet_type: str, pet_color: str, pet_uid: str) -> None:
    conn = db.connect()
    query = 'delete from User_preference where (pet_type="{}" and color="{}") and (age=0 and UID={});'.format(pet_type, pet_color, pet_uid)
    print(query)
    conn.execute(query)
    query = 'Insert ignore Into User_preference (pet_type, color, age, UID) VALUES ("{}", "{}", 0, {});'.format(pet_type, pet_color, pet_uid)
    print(query)
    conn.execute(query)
    conn.close()


def match_pet(pet_id: str, fav:str):
    print(fav)
    conn = db.connect()
    query = "CALL smartMatch({},{});".format(fav,pet_id)
    pre_result = conn.execute(query).fetchall()
    conn.commit()
    query = "Select distinct p.pet_id, p.pet_type, p.color, p.pet_condition, s.shelter_status, s.location from (Pet as p natural join Shelter as s) left join Favors as f on f.pet_id=p.pet_id where f.UID={} or p.UID={} limit 30;".format(pet_id,pet_id)
    favor_result = conn.execute(query).fetchall()
    query = "Select distinct pet_id, pet_type, color, pet_condition, shelter_status, location from Pet natural join Shelter where ((pet_type,color) in (select pet_type,color from User_preference where UID={})) limit 30;".format(pet_id)
    match_result = conn.execute(query).fetchall()
    conn.close()

    pre = []
    for result in pre_result:
        item = {
            "pet_type": result[0],
            "color": result[1],
            "like_num": result[2],
            "heal_num": result[3],
            "rate": result[4]
        }
        pre.append(item)

    favor = []
    for result in favor_result:
        item = {
            "pet_id": result[0],
            "pet_type": result[1],
            "color": result[2],
            "pet_condition": result[3],
            "status": result[4],
            "location": result[5]
        }
        favor.append(item)

    match = []
    for result in match_result:
        item = {
            "pet_id": result[0],
            "pet_type": result[1],
            "color": result[2],
            "pet_condition": result[3],
            "status": result[4],
            "location": result[5]
        }
        match.append(item)

    return pre, favor, match
