# Học thêm tại: https://dash.plotly.com/

# Run this app with `python app.py` and

# visit http://127.0.0.1:8050/ in your web browser.

# BẤM CTRL '+' C ĐỂ TẮT APP ĐANG CHẠY

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# TẢI DỮ LIỆU TỪ FIRESTORE
cred = credentials.Certificate("./iuh-20003021-firebase-adminsdk-zio7s-9302050963.json")
appLoadData = firebase_admin.initialize_app(cred)

dbFireStore = firestore.client()

queryResults = list(dbFireStore.collection(u'tbl-20003021').where(u'DEALSIZE', u'==', 'Large').stream())
listQueryResult = list(map(lambda x: x.to_dict(), queryResults))

df = pd.DataFrame(listQueryResult)

# TRỰC QUAN HÓA DỮ LIỆU WEB APP
app = Dash(__name__)
server = app.server

app.title = "Xây Dựng Danh Mục Sản Phẩm Tiềm Năng"

doanhSo = sum(df['SALES'])
answerdoanhSo = str(round(doanhSo, 2))

loiNhuan = sum(df['SALES']) - sum(df['QUANTITYORDERED']*df['PRICEEACH'])
answerLoiNhuan = str(round(loiNhuan, 2))

DoanhSo = df.groupby(['CATEGORY']).sum(numeric_only=True)
topDoanhSo = DoanhSo['SALES'].max()
answertopDoanhSo = str(round(topDoanhSo, 2))

df["PROFIT"]=df['SALES']-df["QUANTITYORDERED"]*df["PRICEEACH"]
ln = df.groupby(['CATEGORY']).sum('PROFIT')
topLoiNhuan = ln['PROFIT'].max()

answertopLoiNhuan = str(round(topLoiNhuan, 2))

df["YEAR_ID"] = df["YEAR_ID"].astype("str")
h1 = px.histogram(df, x="YEAR_ID", y="SALES", title='Doanh số bán hàng theo năm',
labels={'YEAR_ID': 'Năm','SALES':'Doanh Số'})


hk3 = df[df['YEAR_ID']=='2003']
ln3 = sum(hk3['SALES']) - sum(hk3['QUANTITYORDERED']*hk3['PRICEEACH'])
hk4 = df[df['YEAR_ID']=='2004']
ln4= sum(hk4['SALES']) - sum(hk4['QUANTITYORDERED']*hk4['PRICEEACH'])
hk5 = df[df['YEAR_ID']=='2005']
ln5= sum(hk5['SALES']) - sum(hk5['QUANTITYORDERED']*hk5['PRICEEACH'])
d = pd.DataFrame({
    'YEAR_ID':[2003,2004,2005],
    'PROFIT':[ln3,ln4,ln5]
})
d["YEAR_ID"] = d["YEAR_ID"].astype("str")
h2 = px.line(d, x='YEAR_ID', y='PROFIT', markers=True, labels={'YEAR_ID':'Năm','PROFIT':'Lợi Nhuận'},
title='Lợi nhuận bán hàng theo năm')


h3=px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='SALES',
color='SALES',
labels={'parent':'Năm', 'labels':'Danh Mục','SALES':'Doanh Số'},
title='Tỉ lệ doanh số theo danh mục trong từng năm')

df["PROFIT"]=df['SALES']-df["QUANTITYORDERED"]*df["PRICEEACH"]
h4=px.sunburst(df, path=['YEAR_ID', 'CATEGORY'], values='PROFIT',
color='PROFIT',
labels={'parent':'Năm', 'labels':'Danh Mục','PROFIT':'Lợi Nhuận'},
title='Tỉ lệ lợi nhuận theo danh mục trong từng năm')

sp = df.groupby(['CATEGORY']).sum('SALES').sort_values(by="SALES", ascending=False).reset_index().head(1)['CATEGORY'][0]

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H3(
                    "Xây Dựng Danh Mục Sản Phẩm Tiềm Năng", className="header-title"
                ),html.P('IUH_DHHTTT16C_20003021_Trần Hoài Duy',className='info')
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                children=html.Div(
                    children=[
                        html.P("DOANH SỐ SALE",className="title"),
                        html.P(answerdoanhSo)
                    ],
                    className="label"
                    ),className="card c1"
                ),
                html.Div(
                children=html.Div(
                    children=[
                        html.P("LỢI NHUẬN",className="title"),
                        html.P(answerLoiNhuan)
                    ],
                    className="label"
                    ),className="card c1"
                ),
                html.Div(
                children=html.Div(
                    children=[
                        html.P("TOP DOANH SỐ",className="title"),
                        html.P(sp+', '+answertopDoanhSo)
                    ],
                    className="label"
                    ),className="card c1"
                ),
                html.Div(
                children=html.Div(
                    children=[
                        html.P("TOP LỢI NHUẬN",className="title"),
                        html.P(sp+', '+answertopLoiNhuan)
                    ],
                    className="label"
                    ),className="card c1"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=h1,
                    className="hist"
                    ),className="card c2"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=h3,
                    className="hist"
                    ),className="card c2"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=h2,
                    className="hist"
                    ),className="card c2"
                ),
                html.Div(
                children=dcc.Graph(
                    figure=h4,
                    className="hist"
                    ),className="card c2"
                )
            ],className="wrapper"
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=8090)
            