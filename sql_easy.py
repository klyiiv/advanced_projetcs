db = input()
global_init(db)
db_sess = create_session()
users = db_sess.query(User).filter(User.address == "module_1", User.age < 21)
for i in users:
    i.address = "module_3"
db_sess.commit()
