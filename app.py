#import thư viện
from dash import Dash, html, dcc
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# TẢI DỮ LIỆU TỪ FIRESTORE

if not firebase_admin._apps:
    cred = credentials.Certificate("./iuh-20003021-firebase-adminsdk-zio7s-9302050963.json")
    app = firebase_admin.initialize_app(cred)
dbFIrestore = firestore.client()

QueryResult = list(dbFIrestore.collection("tbl-20003021").stream())
listQurey = list(map(lambda x : x.to_dict(), QueryResult))
df = pd.DataFrame(listQurey)
df = df.dropna(axis='columns')

#df = pd.read_csv('./orginal_sales_data_edit.csv')
#Đổi kiểu dữ liệu của year sang string
df["YEAR_ID"] = df["YEAR_ID"].astype("str")
df["QTR_ID"] = df["QTR_ID"].astype("str")

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)

server = app.server

app.title = "Finance Data Analysis"

#Biểu đồ doanh thu theo năm
bd1_value = df[['YEAR_ID','SALES']].groupby('YEAR_ID').sum()
listValueLoiNhan = list(bd1_value.to_dict().values())
year = listValueLoiNhan[0].keys()
values_loiNhan = listValueLoiNhan[0].values()
bd1 = pd.DataFrame({'YEAR': year,'DoanhThu': values_loiNhan})

figDoanhSoTheoNam = px.bar(bd1, x="YEAR", y="DoanhThu", title="Doanh Thu Theo Năm",
labels={'YEAR':'Năm',  'DoanhThu':'Doanh thu'})

#Biểu đồ doanh số theo mục và theo năm 
figTiLeDongGopDanhSoTheoTungDoanhMuc = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm', 'labels':'Quý','SALES':'Doanh số'},
title='TỈ LỆ ĐÓNG GÓP CỦA DOANH SỐ THEO DANH MỤC TRONG NĂM')



# Dữ liệu truy vấn 
tongDoanhSo = df['SALES'].sum().round(2)
doanhSoCaoNhat = df.groupby(['CATEGORY']).sum(numeric_only=True)['SALES'].max()

#Tinh loi nhuan
#1 Tính total sale
df['TOTAL_SALES'] = df['QUANTITYORDERED'] * df['PRICEEACH']
#2 Tính lợi nhuận
df['Profit'] = (df['SALES'] - df['TOTAL_SALES']).round(2)
tongLoiNhuan = df['Profit'].sum().round(2)
loiNhuanCaoNhat = df.groupby(['CATEGORY']).sum('Profit')['Profit'].max()

#Vẽ biểu đồ 3
figTiLeDongGopLoiNhanTheoTungDoanhMuc = px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='Profit',
color='Profit',
labels={'parent':'Năm', 'labels':'Quý','Profit':'Lợi nhuận'},
title='TỈ LỆ ĐÓNG GÓP CỦA LỢI NHUẬN THEO MỤC TRONG NĂM')

lnvalue = df[['YEAR_ID','Profit']].groupby('YEAR_ID').sum()
listValueLoiNhan = list(lnvalue.to_dict().values())
year = listValueLoiNhan[0].keys()
values_loiNhan = listValueLoiNhan[0].values()
bd2 = pd.DataFrame({'YEAR': year,'LoiNhuan': values_loiNhan})
figLoiNhanTheoNam = px.line(bd2, x="YEAR", y="LoiNhuan", title='LỢI NHUẬN BÁN HÀNG THEO NĂM', labels={'YEAR':'Năm',  'LoiNhuan':'Lợi nhuận'})

app.layout = html.Div(
    children=[
        html.Div(
             children=[
                html.H1(
                    children="XÂY DỰNG DOANH MỤC SẢN PHẨM TIỀM NĂNG", className="header-title-left"
                ),
                html.H1(
                    children="IUH-DHHHTT16C-20003021-Trần Hoài Duy", className="header-title-right"
                )
                ],className="header"
        ),
        html.Div(
            children=[
                html.Div(
                    children=[html.H4("DOANH SỐ SALE"),
                              html.P(tongDoanhSo)
                    ], className="under__header__item"),
                html.Div(
                    children=[html.H4("LỢI NHUẬN"),
                              html.P(tongLoiNhuan)
                    ], className="under__header__item"),
                html.Div(
                    children=[html.H4("TOP DOANH SỐ"),
                              html.P(doanhSoCaoNhat)
                    ], className="under__header__item"),
                html.Div(
                    children=[html.H4("TOP LỢI NHUẬN"),
                              html.P(loiNhuanCaoNhat)
                    ], className="under__header__item")
            ]
        ,className="under__header"),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                    id='soluong-graph',
                    figure=figDoanhSoTheoNam),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='doanhso-graph',
                    figure=figTiLeDongGopDanhSoTheoTungDoanhMuc),
                    className="card"
                )
            ], className="wrapper"),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                    id='luongdon-graph',
                    figure=figLoiNhanTheoNam),
                    className="card"
                ),
                html.Div(
                    children=dcc.Graph(
                    id='hihi-graph',
                    figure=figTiLeDongGopLoiNhanTheoTungDoanhMuc),
                    className="card"
                )
            ], className="wrapper")
    ])

'''
if __name__ == '__main__':
    app.run_server(debug=True, port=8090)
'''

if __name__ == '__main__':
    app.run_server(debug=True)