import mysql.connector
from datetime import datetime
import time

def generate_data(dev_id):
    """
    生成模拟数据。
    """
    rec_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cmd_data = bytes.fromhex('7e0100110034e80301000a0000191b000c003c0000181b000c004600001a1b000c00550000181b000c006900001a1c000c00870000181b000c000f5f7f')
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

        # 遍历每个设备ID
        for dev_id in dev_ids:
            print(f"Current device ID: {dev_id}")
            
            # 写入500条记录
            for _ in range(500):
                # 生成数据
                rec_time, dev_id, cmd_data = generate_data(dev_id)

                # 插入数据
                cursor = conn.cursor()
                cursor.execute("INSERT INTO pollingresponsecmd (RecTime, DevId, CmdData) VALUES (%s, %s, %s)", 
                              (rec_time, dev_id, cmd_data))
                
                # 提交更改
                conn.commit()
                cursor.close()

                print(f"Inserted: RecTime={rec_time}, DevId={dev_id}, CmdData={cmd_data.hex()}")

                # 休眠300毫秒，避免频繁插入
                time.sleep(0.3)
            
            print(f"Data insertion completed for device ID {dev_id}.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            # 关闭数据库连接
            conn.close()

# 调用函数
insert_data()
