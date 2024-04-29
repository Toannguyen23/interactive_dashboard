import mysql.connector as connector
import streamlit as st

#ket noi co so du lieu

connection = connector.connect(
    user='minhtoan',
    password='123456789',
    db='mydb'
)

cursor = connection.cursor(buffered=True)
#ham tong

def view_all_data():
    try:
        cursor.execute("select * from carsales")
        data = cursor.fetchall()
        return data

    except connector.errors.InternalError as e:
        st.error("Tìm kết quả thất bại: " + str(e))