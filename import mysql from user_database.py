import mysql.connector
from datetime import datetime
import time

def generate_data(UserId):
    """
    生成模拟数据。
    """
    OptTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    OptDesc = '进入首页。'
    return OptTime, UserId, OptDesc

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

        # 获取用户ID列表
        user_ids = get_user_ids(conn)
        if not user_ids:
            print("No device IDs found in the 'device' table.")
            return

        # 遍历每个设备ID
        for user_id in user_ids:
            print(f"Current user ID: {user_id}")
            
            # 写入500条记录
            for _ in range(500):
                # 生成数据
                OptTime, user_id, cmd_data = generate_data(user_id)

                # 插入数据
                cursor = conn.cursor()
                cursor.execute("INSERT INTO pollingresponsecmd (RecTime, DevId, CmdData) VALUES (%s, %s, %s)", 
                              (OptTime, user_id, cmd_data))
                
                # 提交更改
                conn.commit()
                cursor.close()

                print(f"Inserted: RecTime={OptTime}, DevId={user_id}, CmdData={cmd_data}")

                # 休眠300毫秒，避免频繁插入
                time.sleep(0.3)
            
            print(f"Data insertion completed for device ID {user_id}.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            # 关闭数据库连接
            conn.close()

# 调用函数
insert_data()
