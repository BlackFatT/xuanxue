import sqlite3
from sqlite3 import Error


class SQLiteHandler:
    def __init__(self, db_name):
        """初始化数据库连接"""
        self.db_name = db_name
        self.connection = None
        self.connect()

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"数据库连接成功: {self.db_name}")
            return True
        except Error as e:
            print(f"连接失败: {e}")
            return False

    def create_table(self):
        """创建用户表"""
        if not self.connection:
            print("未建立数据库连接")
            return False

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            age INTEGER,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_sql)
            self.connection.commit()
            print("用户表创建成功")
            return True
        except Error as e:
            print(f"创建表失败: {e}")
            self.connection.rollback()
            return False

    def insert_user(self, username, email, age=None):
        """插入新用户"""
        if not self.connection:
            return False

        insert_sql = """
        INSERT INTO users (username, email, age)
        VALUES (?, ?, ?)
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_sql, (username, email, age))
            self.connection.commit()
            print(f"插入用户成功，ID: {cursor.lastrowid}")
            return cursor.lastrowid
        except Error as e:
            print(f"插入用户失败: {e}")
            self.connection.rollback()
            return False

    def get_users(self, condition=None):
        """查询用户，可带条件"""
        if not self.connection:
            return []

        query_sql = "SELECT * FROM users"
        if condition:
            query_sql += f" WHERE {condition}"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query_sql)
            # 获取列名用于格式化输出
            columns = [desc[0] for desc in cursor.description]
            users = [dict(zip(columns, row)) for row in cursor.fetchall()]
            print(f"查询到 {len(users)} 条用户记录")
            return users
        except Error as e:
            print(f"查询用户失败: {e}")
            return []

    def update_user(self, user_id, **kwargs):
        """更新用户信息"""
        if not self.connection or not kwargs:
            return False

        # 构建更新字段
        update_fields = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        update_sql = f"UPDATE users SET {update_fields} WHERE id = ?"

        # 准备参数
        params = list(kwargs.values()) + [user_id]

        try:
            cursor = self.connection.cursor()
            cursor.execute(update_sql, params)
            self.connection.commit()
            print(f"更新成功，影响行数: {cursor.rowcount}")
            return cursor.rowcount > 0
        except Error as e:
            print(f"更新用户失败: {e}")
            self.connection.rollback()
            return False

    def delete_user(self, user_id):
        """删除用户"""
        if not self.connection:
            return False

        delete_sql = "DELETE FROM users WHERE id = ?"

        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_sql, (user_id,))
            self.connection.commit()
            print(f"删除成功，影响行数: {cursor.rowcount}")
            return cursor.rowcount > 0
        except Error as e:
            print(f"删除用户失败: {e}")
            self.connection.rollback()
            return False

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")


def main():
    # 创建数据库处理器实例
    db_handler = SQLiteHandler("user_database.db")

    # 查询所有用户
    print("\n所有用户001:")
    all_users = db_handler.get_users()
    for user in all_users:
        print(user)

    # 创建用户表
    db_handler.create_table()

    # 插入测试数据
    db_handler.insert_user("张三", "zhangsan@example.com", 25)
    db_handler.insert_user("李四", "lisi@example.com", 30)
    db_handler.insert_user("王五", "wangwu@example.com")  # 年龄可选

    # 查询所有用户
    print("\n所有用户:")
    all_users = db_handler.get_users()
    for user in all_users:
        print(user)

    # 条件查询（年龄大于28的用户）
    print("\n年龄大于28的用户:")
    adult_users = db_handler.get_users("age > 28")
    for user in adult_users:
        print(user)

    # 更新用户信息（更新ID为1的用户年龄）
    print("\n更新用户信息:")
    db_handler.update_user(1, age=26, email="zhangsan_new@example.com")

    # 再次查询验证更新结果
    print("\n更新后的用户信息:")
    updated_user = db_handler.get_users("id = 1")
    print(updated_user)

    # 删除用户（删除ID为3的用户）
    print("\n删除用户:")
    db_handler.delete_user(3)

    # 最终用户列表
    print("\n最终用户列表:")
    final_users = db_handler.get_users()
    for user in final_users:
        print(user)

    # 关闭连接
    db_handler.close()


if __name__ == "__main__":
    main()
