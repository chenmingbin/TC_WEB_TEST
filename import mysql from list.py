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

def insert_data():
    conn = mysql.connector.connect(
        host="127.0.0.1",  # 确保这里与 MySQL 服务器配置一致
        user="root",
        password="123456",
        database="jammermonitor",
        port=3306,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    c = conn.cursor()

    # 设备ID范围
    dev_ids = [41] + list(range(68, 81))

    # 每个设备ID写入500条记录
    for dev_id in dev_ids:
        for _ in range(500):
            # 生成数据
            rec_time, dev_id, cmd_data = generate_data(dev_id)

            # 插入数据
            c.execute("INSERT INTO pollingresponsecmd (RecTime, DevId, CmdData) VALUES (%s, %s, %s)", 
                      (rec_time, dev_id, cmd_data))
            
            # 提交更改
            conn.commit()

            print(f"Inserted: RecTime={rec_time}, DevId={dev_id}, CmdData={cmd_data.hex()}")

            # 休眠500毫秒，避免频繁插入
            time.sleep(0.5)
    
    print("Data insertion completed for all device IDs.")
    
    # 关闭数据库连接
    conn.close()

# 调用函数
insert_data()
