# -*- coding:utf-8 -*-
import datetime
import platform
import re
import time
from functools import wraps
import warnings
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import os
import calendar
import get_myconf

warnings.filterwarnings('ignore')


class MysqlUpload:
    def __init__(self, username: str, password: str, host: str, port: int, charset: str = 'utf8mb4'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.config = {
            'host': self.host,
            'port': self.port,
            'user': self.username,
            'password': self.password,
            'charset': charset,  # utf8mb4 支持存储四字节的UTF-8字符集
            'cursorclass': pymysql.cursors.DictCursor,
        }
        self.conn = None

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    def _conn(self):
        self.config = {
            'host': self.host,
            'port': int(self.port),
            'user': self.username,
            'password': self.password,
            'charset': 'utf8mb4',  # utf8mb4 支持存储四字节的UTF-8字符集
            'cursorclass': pymysql.cursors.DictCursor,
        }
        try:
            self.conn = pymysql.connect(**self.config)  # 连接数据库
            return True
        except:
            return False

    @try_except
    def df_to_mysql(self, _table, _df, _db_name='远程数据源'):
        """
        将 _df 写入数据库, df 必须包含日期列
        _db_name: 数据库名称
        _table: 集合名称
        """
        cols = _df.columns.tolist()
        if '日期' in cols:
            _df['日期'] = _df['日期'].apply(lambda x: pd.to_datetime(x) if x else x)
        for col in cols:
            # 列名不能包含的特殊字符
            col_new = re.sub(r'[\',（)()/=<>+\-*^"’\[\]~#|&% ]', '_', col)
            _df.rename(columns={col: col_new}, inplace=True)

        connection = pymysql.connect(**self.config)  # 连接数据库
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{_db_name}'")  # 检查数据库是否存在
                database_exists = cursor.fetchone()
                if not database_exists:
                    # 如果数据库不存在，则新建
                    if '8.138.27' in str(self.host) or platform.system() == "Linux":  # 阿里云 mysql 低版本不支持 0900
                        cursor.execute(f"CREATE DATABASE {_db_name} COLLATE utf8mb4_unicode_ci")
                        self.config.update({'charset': 'utf8mb4_unicode_ci'})
                    else:
                        cursor.execute(f"CREATE DATABASE {_db_name} COLLATE utf8mb4_0900_ai_ci")
                    connection.commit()
                    print(f"创建Database: {_db_name}")
        except Exception as e:
            print(e)
            return
        finally:
            connection.close()  # 这里要断开连接

        self.config.update({'database': _db_name})  # 添加更新 config 字段
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        try:
            with connection.cursor() as cursor:
                _table = _table.replace('-', '_')
                # 1. 查询表, 不存在则创建一个空表
                cursor.execute(f"SHOW TABLES LIKE '{_table}'")
                if not cursor.fetchone():
                    sql = f'CREATE TABLE IF NOT EXISTS {_table} (id INT AUTO_INCREMENT PRIMARY KEY)'
                    cursor.execute(sql)
                    print(f'创建 mysql 表: {_table}')

                # 2. 检查列, 不存在则添加新列
                for col in _df.columns.tolist():
                    sql = ('SELECT 1 FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND '
                           'column_name = %s')
                    cursor.execute(sql, (_db_name, {_table}, col))
                    if cursor.fetchone() is None:  # 如果列不存在，添加新列
                        print(f"添加列: {col}")  # 添加列并指定数据类型
                        if col == '日期':
                            sql = f"ALTER TABLE {_table} ADD COLUMN {col} DATE default NULL;"
                        else:
                            sql = f"ALTER TABLE {_table} ADD COLUMN {col} mediumtext default NULL;"
                        cursor.execute(sql)

                    if col == '日期':
                        cursor.execute(f"SHOW INDEXES FROM `{_table}` WHERE Column_name = %s", ({col},))
                        result = cursor.fetchone()  # 检查索引是否存在
                        if not result:
                            # print(f'创建索引: {col}')
                            cursor.execute(f"CREATE INDEX index_name ON {_table}({col})")
                connection.commit()  # 提交事务

                # # 3. 移除指定日期范围内的数据, 避免重复插入
                # dates = _df['日期'].values.tolist()
                # start_date = pd.to_datetime(min(dates)).strftime('%Y-%m-%d')
                # end_date = (pd.to_datetime(max(dates)) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                # sql = f"DELETE FROM {_table} WHERE {'日期'} BETWEEN '%s' AND '%s'" % (start_date, end_date)
                # cursor.execute(sql)
                # connection.commit()

                # 4. 更新插入数据
                try:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")
                    print(f'{now}正在更新 mysql ({self.host}) 数据库: {_table}')
                    engine = create_engine(
                        f'mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{_db_name}'
                    )
                    _df.to_sql(_table, con=engine, if_exists='append', index=False)
                except Exception as e:  # 如果异常则回滚
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S: ")
                    print(f'{now}{_table}数据异常, 正在回滚: {e}')
                    connection.rollback()
        finally:
            connection.close()

    def upload_pandas(self, update_path, db_name, days=None):
        """
        专门用来上传 pandas数据源的全部文件
        db_name: 数据库名
        update_path: 上传更新文件所在路径
        days: 更新近期数据，单位: 天, 不设置则全部更新
        """
        if days:
            today = datetime.date.today()
            start_date = pd.to_datetime(today - datetime.timedelta(days=days))
        else:
            start_date = pd.to_datetime('2000-01-01')

        root_files = os.listdir(update_path)
        for root_file in root_files:
            if '其他数据' in root_file or '年.csv' in root_file or '京东数据集' in root_file:
                continue  # 跳过的文件夹
            f_path = os.path.join(update_path, root_file)

            if os.path.isdir(f_path):
                for root, dirs, files in os.walk(f_path, topdown=False):
                    for name in files:
                        if name.endswith('.csv') and 'baidu' not in name:
                            df = pd.read_csv(os.path.join(root, name), encoding='utf-8_sig', header=0, na_filter=False)
                            # if '日期' not in df.columns.tolist():
                            #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                            #     print(f'{now}{root_file} 缺少日期列, 不支持上传 mysql')
                            #     continue
                            if '日期' in df.columns.tolist():
                                df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x) if x else x)
                                df = df[df['日期'] >= start_date]
                            if len(df) == 0:
                                continue
                            self.df_to_mysql(_df=df, _db_name=db_name, _table=root_file)
            elif os.path.isfile(f_path):
                if f_path.endswith('.csv') and 'baidu' not in f_path:
                    df = pd.read_csv(f_path, encoding='utf-8_sig', header=0, na_filter=False)
                    # if '日期' not in df.columns.tolist():
                    #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                    #     print(f'{now}{root_file} 缺少日期列, 不支持上传 mysql')
                    #     continue
                    if '日期' not in df.columns.tolist():
                        df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x) if x else x)
                        df = df[df['日期'] >= start_date]
                    if len(df) == 0:
                        continue
                    table = f'{os.path.splitext(root_file)[0]}_f'  # 这里定义了文件表会加 _f 后缀
                    self.df_to_mysql(_df=df, _db_name=db_name, _table=table)

    # @try_except
    def read_mysql(self, _table, start_date, end_date, _db_name='远程数据源', ):
        start_date = pd.to_datetime(start_date).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(end_date).strftime('%Y-%m-%d')
        _df = pd.DataFrame()

        connection = pymysql.connect(**self.config)  # 连接数据库
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{_db_name}'")  # 检查数据库是否存在
                database_exists = cursor.fetchone()
                if not database_exists:
                    print(f"Database {_db_name} 数据库不存在")
                    return _df
                else:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                    print(f'{now}mysql 正在查询表: {_table}, 范围: {start_date}~{end_date}')
        except:
            return _df
        finally:
            connection.close()  # 断开连接

        before_time = time.time()
        # 读取数据
        self.config.update({'database': _db_name})
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        try:
            with connection.cursor() as cursor:
                # 获取指定日期范围的数据
                sql = f"SELECT * FROM {_db_name}.{_table} WHERE {'日期'} BETWEEN '%s' AND '%s'" % (start_date, end_date)
                cursor.execute(sql)
                rows = cursor.fetchall()  # 获取查询结果
                columns = [desc[0] for desc in cursor.description]
                _df = pd.DataFrame(rows, columns=columns)  # 转为 df
        except Exception as e:
            print(f'{e} {_db_name} -> {_table} 表不存在')
            return _df
        finally:
            connection.close()

        if len(_df) == 0:
            print(f'database: {_db_name}, table: {_table} 查询的数据为空')
        else:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            cost_time = int(time.time() - before_time)
            if cost_time < 1:
                cost_time = round(time.time() - before_time, 2)
            print(f'{now}mysql ({self.host}) 表: {_table} 获取数据长度: {len(_df)}, 用时: {cost_time} 秒')
        return _df


class OptimizeDatas:
    """ 数据维护 删除 mysql 的重复数据"""
    def __init__(self, username: str, password: str, host: str, port: int, charset: str = 'utf8mb4'):
        self.username = username
        self.password = password
        self.host = host
        self.port = port  # 默认端口, 此后可能更新，不作为必传参数
        self.charset = charset
        self.config = {
            'host': self.host,
            'port': self.port,
            'user': self.username,
            'password': self.password,
            'charset': self.charset,  # utf8mb4 支持存储四字节的UTF-8字符集
            'cursorclass': pymysql.cursors.DictCursor,
        }
        self.db_name_lists: list = []  # 更新多个数据库 删除重复数据
        self.db_name = None
        self.days: int = 60  # 对近 N 天的数据进行排重

    @staticmethod
    def try_except(func):  # 在类内部定义一个异常处理方法
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f'{func.__name__}, {e}')  # 将异常信息返回

        return wrapper

    def optimize_list(self):
        """
        更新多个数据库 移除冗余数据
        需要设置 self.db_name_lists
        """
        if not self.db_name_lists:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            print(f'{now}尚未设置参数: self.db_name_lists')
            return
        for db_name in self.db_name_lists:
            self.db_name = db_name
            self.optimize()

    def optimize(self):
        """ 更新一个数据库 移除冗余数据 """
        if not self.db_name:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            print(f'{now}尚未设置参数: self.db_name')
            return
        tables = self.table_list(db_name=self.db_name)
        if not tables:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            print(f'{now}{self.db_name} -> 数据表不存在')
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        print(f'{now}mysql({self.host}: {self.port}) 数据库优化中(日期长度: {self.days} 天)...')
        self.optimize_main(tables=tables)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
        print(f'{now}mysql({self.host}: {self.port}) 数据库优化完成!')

    @try_except
    def optimize_main(self, tables):
        """
        因为有时会断联, 单独设置这个函数, 避免全局宕机
        """
        for table_dict in tables:
            for key, table_name in table_dict.items():
                # if '人群洞察' not in table_name:
                #     continue
                if '京东数据集' in table_name:
                    print(f'跳过的文件: {table_name}')
                    continue
                begin_time = time.time()
                datas = self.table_datas(db_name=self.db_name, table_name=str(table_name), days=self.days)
                if not datas:
                    continue

                duplicate_id = []  # 出现重复的 id
                all_datas = []  # 迭代器
                for data in datas:
                    delete_id = data['id']
                    del data['id']
                    if str(data) in all_datas:  # 数据出现重复时
                        duplicate_id.append(delete_id)  # 添加 id 到 duplicate_id
                        continue
                    all_datas.append(str(data))  # 数据没有重复
                del all_datas

                if not duplicate_id:  # 如果没有重复数据，则跳过该数据表
                    continue
                try:
                    connection = pymysql.connect(**self.config)
                except Exception as e:
                    print(f'{self.db_name}/{table_name}, {e}')
                    time.sleep(60)  # 连接如果断开，重试一次
                    connection = pymysql.connect(**self.config)

                try:
                    with connection.cursor() as cursor:
                        placeholders = ', '.join(['%s'] * len(duplicate_id))
                        # 移除冗余数据
                        sql = f"DELETE FROM {table_name} WHERE id IN ({placeholders})"
                        cursor.execute(sql, duplicate_id)
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                        cost_time = round(time.time() - begin_time, 2)
                        print(f"{now}{self.db_name}/{table_name} -> 原数据: {len(datas)}, "
                              f"删除重复数据: {cursor.rowcount}, 用时: {cost_time}")

                        # 5. 重置自增列 (id 列)
                        try:
                            cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE 'id'")
                            result = cursor.fetchone()
                            if result:
                                cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN id;")  # 删除 id  列
                            cursor.execute(
                                f"ALTER TABLE {table_name} ADD column id INT AUTO_INCREMENT PRIMARY KEY FIRST;")
                            cursor.execute(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1")  # 设置自增从 1 开始
                        except Exception as e:
                            print(f'{e}')
                            connection.rollback()

                    connection.commit()  # 提交事务
                except Exception as e:
                    print(f'{self.db_name}/{table_name}, {e}')
                    connection.rollback()  # 异常则回滚
                finally:
                    connection.close()

    def database_list(self):
        """ 获取所有数据库 """
        connection = pymysql.connect(**self.config)  # 连接数据库
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()  # 获取所有数据库的结果
        connection.close()
        return databases

    def table_list(self, db_name):
        """ 获取指定数据库的所有数据表 """
        connection = pymysql.connect(**self.config)  # 连接数据库
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")  # 检查数据库是否存在
                database_exists = cursor.fetchone()
                if not database_exists:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
                    print(f'{now}{db_name}: 数据表不存在!')
                    return
        except Exception as e:
            print(f'002 {e}')
            return
        finally:
            connection.close()  # 断开连接

        self.config.update({'database': db_name})  # 添加更新 config 字段
        connection = pymysql.connect(**self.config)  # 重新连接数据库
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()  # 获取所有数据表
        connection.close()
        return tables

    def table_datas(self, db_name, table_name, days: int):
        """
        获取指定数据表的数据
        days: 返回近 N 天数据
        返回： [dict, dict, ...]
        """
        end_date = datetime.date.today()
        start_date = pd.to_datetime(end_date - datetime.timedelta(days=days))
        self.config.update({'database': db_name})  # 添加更新 config 字段
        connection = pymysql.connect(**self.config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"SHOW FULL COLUMNS FROM {table_name}")  # 查询数据表的列信息
                columns = cursor.fetchall()
                for col in columns:  # 遍历列信息，检查是否存在类型为日期的列
                    if col['Field'] == '日期' and col['Type'] == 'date' or col['Type'].startswith('datetime'):
                        sql = f"SELECT * FROM {table_name} WHERE {'日期'} BETWEEN '%s' AND '%s'" % (start_date, end_date)
                        break
                else:
                    sql = f"SELECT * FROM {table_name}"  # 如果不包含日期列，则获取全部数据
                cursor.execute(sql)
                results = cursor.fetchall()
        except Exception as e:
            print(f'001 {e}')
        finally:
            connection.close()
        return results


def year_month_day(start_date, end_date):
    """
    使用date_range函数和DataFrame来获取从start_date至end_date之间的所有年月日
    calendar.monthrange： 获取当月第一个工作日的星期值(0,6) 以及当月天数
    """
    # 替换年月日中的日, 以便即使传入当月日期也有返回值
    try:
        start_date = f'{pd.to_datetime(start_date).year}-{pd.to_datetime(start_date).month}-01'
    except Exception as e:
        print(e)
        return []
    # 使用pandas的date_range创建一个日期范围，频率为'MS'代表每月开始
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')
    # 转换格式
    year_months = date_range.strftime('%Y-%m').drop_duplicates().sort_values()

    results = []
    for year_month in year_months:
        year = re.findall(r'(\d{4})', year_month)[0]
        month = re.findall(r'\d{4}-(\d{2})', year_month)[0]
        s, d = calendar.monthrange(int(year), int(month))
        results.append({'起始日期': f'{year_month}-01', '结束日期': f'{year_month}-{d}'})

    return results  # start_date至end_date之间的所有年月日


def download_datas(_table, save_path, start_date):
    username, password, host, port = get_myconf.select_config_values(target_service='home_lx', database='mysql')
    m = MysqlUpload(username=username, password=password, host=host, port=port)
    m.port = port
    results = year_month_day(start_date=start_date, end_date='today')
    # print(results)
    for result in results:
        start_date = result['起始日期']
        end_date = result['结束日期']
        # print(start_date, end_date)
        df = m.read_mysql(_db_name='pandas数据源', _table=_table, start_date=start_date, end_date=end_date)
        if len(df) == 0:
            continue
        path = os.path.join(save_path, f'{_table}_{str(start_date)}_{str(end_date)}.csv')
        df['日期'] = df['日期'].apply(lambda x: re.sub(' .*', '', str(x)))
        df.to_csv(path, index=False, encoding='utf-8_sig', header=True)


if __name__ == '__main__':
    username, password, host, port = get_myconf.select_config_values(target_service='aliyun', database='mysql')
    print(username, password, host, port)
    # o = OptimizeDatas(username=username, password=password, host=host, port=port)
    # o.db_name = 'pandas数据源'
    # o.days = 6
    # o.optimize()
