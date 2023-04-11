import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="clothes"
)

if __name__ == '__main__':
    a = 0
    b = 0
    mycursor = mydb.cursor()
    while a == 0:
        username = input("username：")
        password = input("password：")
        mycursor.execute("SELECT password FROM users where username = %s", (username,))
        result_pass = mycursor.fetchone()
        password_res = ""
        for x in result_pass:
            password_res = x
        if password_res == password:
            mycursor.execute("SELECT products.brand, products.name, sizes.value FROM users JOIN "
                             "user_products ON users.id = user_products.user_id JOIN products ON "
                             "user_products.product_id "
                             "= products.id JOIN sizes ON user_products.size_id = sizes.id WHERE users.username = "
                             "%s", (username,))
            result_user_order = mycursor.fetchall()
            for x in result_user_order:
                print(x)
            a = 1
            while b == 0:
                brand = input("brand：")
                name = input("product(name)：")
                size_target = input("size(want)：")
                size_ori = input("size(origin)：")
                # mycursor.execute("SELECT u.username, ua.latitude, ua.longitude FROM users u JOIN user_addresses ua ON "
                #                  "u.id = ua.user_id JOIN user_products up ON u.id = up.user_id JOIN products p ON "
                #                  "up.product_id = p.id JOIN sizes s1 ON up.size_id = s1.id JOIN sizes s2 ON p.name = "
                #                  "%s AND p.brand = %s AND s2.value = %s WHERE s1.value = %s AND "
                #                  "ua.user_id = 1 ORDER BY POWER(ua.latitude - (SELECT latitude FROM user_addresses "
                #                  "WHERE user_id = 1), 2)  + POWER(ua.longitude - (SELECT longitude FROM "
                #                  "user_addresses WHERE user_id = 1), 2) LIMIT 1", (name, brand, size_ori, size_target,))

                mycursor.execute("SELECT u.id, u.username, ua.latitude, ua.longitude, p.name AS product_name, "
                                 "s1.value AS size FROM users u JOIN user_addresses ua ON u.id = ua.user_id JOIN "
                                 "user_products up ON u.id = up.user_id JOIN products p ON up.product_id = p.id JOIN "
                                 "sizes s1 ON up.size_id = s1.id JOIN sizes s2 ON p.name = %s AND p.brand = "
                                 "%s AND s2.value = %s WHERE s1.value = %s AND p.name = %s AND p.brand "
                                 "= %s AND up.size_id = s2.id AND u.username <> %s ORDER BY POWER(ua.latitude - ("
                                 "SELECT "
                                 "latitude FROM user_addresses WHERE user_id = 1), 2) + POWER(ua.longitude - (SELECT "
                                 "longitude FROM user_addresses WHERE user_id = 1), 2) LIMIT 1", (name, brand, size_target, size_target, name, brand, username, ))
                result = mycursor.fetchall()
                if len(result) == 0:
                    print("No user can exchange clothes with you")
                else:
                    for x in result:
                        print(x)
                if_exit = input("Do you want to exit? 1(yes) 0(no): ")
                if int(if_exit) == 1:
                    break
        else:
            print("Username or password error!")
