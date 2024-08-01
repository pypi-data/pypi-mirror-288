from sqlman import MySQL

cfg = {
    'username': 'admin',
    'password': 'admin@1',
    'db': 'test'
}
db = MySQL(**cfg)
# db.gen_test_table('aaa')
aaa = db["aaa"]

# print(aaa.insert_data(data={"name": "CLOS"}))
# print(aaa.delete(name="CLOS"))
# print(aaa.update(new={"name": "CLOS-2"}, name="CLOS"))
print(aaa.query(name="CLOS"))

print(aaa.exe_sql("select * from aaa where name='CLOS'", query_all=False))



