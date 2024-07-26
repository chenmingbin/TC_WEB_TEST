import mysql.connector
from datetime import datetime
import time

def generate_data(dev_id):
    """
    生成模拟数据。
    """
    rec_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cmd_data = bytes.fromhex('7e0200110034e80301000a0000191b000c003c0000181b000c004600001a1b000c00550000181b000c006900001a1c000c00870000181b000c0001EF7f')
    return rec_time, dev_id, cmd_data
    
def get_device_ids(conn):
    """
    从device表中获取设备ID列表。
    """
    cursor = conn.cursor()
    cursor.execute("SELECT DevId FROM device")
    device_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return device_ids

def get_user_ids(conn):
    """
    从user表中获取用户ID列表。
    """
    cursor = conn.cursor()
    cursor.execute("SELECT UserId FROM user")
    user_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return user_ids

def insert_data():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="123456",
            database="jammermonitor",
            port=3306,
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )

        # 获取设备ID列表
        dev_ids = get_device_ids(conn)
        if not dev_ids:
            print("No device IDs found in the 'device' table.")
            return

        # 获取用户ID列表
        user_ids = get_user_ids(conn)
        if not user_ids:
            print("No user IDs found in the 'user' table.")
            return

        dev_count = len(dev_ids)
        user_count = len(user_ids)
        dev_index = 0
        user_index = 0

        # 写入数据
        for _ in range(2592000):
            # 获取当前设备ID
            dev_id = dev_ids[dev_index]

            # 获取当前用户ID
            user_id = user_ids[user_index]

            # 生成数据
            rec_time, dev_id, cmd_data = generate_data(dev_id)
            print(cmd_data)

            # 插入设备数据
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pollingresponsecmd (RecTime, DevId, CmdData) VALUES (%s, %s, %s)", 
                          (rec_time, dev_id, cmd_data))
            conn.commit()
            cursor.close()

            # 插入用户日志数据
            opt_time = rec_time
            opt_desc = f"Inserted data for user {user_id}"
            cursor = conn.cursor()
            cursor.execute("INSERT INTO operationlog (OptTime, UserId, OptDesc) VALUES (%s, %s, %s)", 
                          (opt_time, user_id, opt_desc))
            conn.commit()
            cursor.close()

            print(f"Inserted: RecTime={rec_time}, DevId={dev_id}, CmdData={cmd_data.hex()}")
            print(f"Logged operation for UserId={user_id} at OptTime={opt_time} with description '{opt_desc}'")

            # 更新设备索引
            dev_index = (dev_index + 1) % dev_count

            # 更新用户索引
            user_index = (user_index + 1) % user_count

            # 休眠10毫秒
            # time.sleep(0.01)

        print(f"Data insertion completed.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            # 关闭数据库连接
            conn.close()

# 调用函数
insert_data()
