import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#title
st.title("Analisis data E-Commerce")
with st.expander("ℹ️ Perhatikan Sebelum Menggunakan Dashboard Ini", expanded=True):
    st.markdown("""
    **Selamat datang di Dashboard Analisis E-Commerce!**
    - **Filter Tanggal** di sidebar hanya berlaku untuk analisis **"Total Order per Kota"** dan **"Total Order per Negara Bagian"**
    - Filter tanggal tidak berpengaruh pada analisis "Total Sales per Kategori"
    - Gunakan menu di sidebar untuk berpindah antar jenis analisis
    - Setiap analisis memiliki beberapa tab dengan visualisasi berbeda
    - ada keterbatasan data disini, hanya melampirkan data e-commerce dengan rentang waktu 2016 sampai 2018
    
    Selamat menggunaka :)
    """)

#menyiapkaan data yang akan ditampilkan
sales_df = pd.read_csv('https://raw.githubusercontent.com/miftahsuryan/Analisi_Data_E-Commerce/master/dashboard/combined_sales_kategori_df.csv')
city_df = pd.read_csv('https://raw.githubusercontent.com/miftahsuryan/Analisi_Data_E-Commerce/master/dashboard/order_per_city_df.csv')
state_df = pd.read_csv('https://raw.githubusercontent.com/miftahsuryan/Analisi_Data_E-Commerce/master/dashboard/order_per_state_df.csv')
time_df = pd.read_csv('https://raw.githubusercontent.com/miftahsuryan/Analisi_Data_E-Commerce/master/dashboard/time_location_per_order_df.csv')

# Menambahkan proses konversi kolom tanggal
time_df['order_purchase_timestamp'] = pd.to_datetime(time_df['order_purchase_timestamp'])

# sidebar
st.sidebar.title("Menu")
option = st.sidebar.radio(
    "Pilih Analisis", 
    ["Total Sales per Kategori", "Total Order per Kota", "Total Order per Negara Bagian"]
)

#slider untuk memilih jumlah data yang ditampilkan
number_of_rows = st.sidebar.slider("Jumlah data yang ditampilkan:", 5, 50, 10)

#menambahkan fitur interaktif tanggal
st.sidebar.header("Filter Tanggal")
min_date = time_df['order_purchase_timestamp'].min().date()
max_date = time_df['order_purchase_timestamp'].max().date()
start_date = st.sidebar.date_input("Tanggal Mulai", min_date)
end_date = st.sidebar.date_input("Tanggal Akhir", max_date)

start_datetime = datetime.datetime.combine(start_date, datetime.time.min)
end_datetime = datetime.datetime.combine(end_date, datetime.time.max)

# Filter data berdasarkan tanggal
filtered_time_df = time_df[(time_df['order_purchase_timestamp'] >= start_datetime) & 
                          (time_df['order_purchase_timestamp'] <= end_datetime)]
filtered_city_orders = filtered_time_df.groupby('customer_city').size().reset_index(name='jumlah_pesanan')
filtered_state_orders = filtered_time_df.groupby('customer_state').size().reset_index(name='jumlah_pesanan')

city_count_col = 'jumlah_pesanan'
state_count_col = 'jumlah_pesanan'

#konten sesuai pilihan
if option == "Total Sales per Kategori":
    st.header("Total Sales per Kategori Produk")
    
    #tampilkan tabs untuk memilih tampilan data atau chart
    tab1, tab2, tab3 = st.tabs(["Data", "Visualisasi Kategori", "Top 10 Kategori"])
    
    with tab1:
        st.subheader("Data Penjualan per Kategori")
        st.dataframe(sales_df.head(number_of_rows))
        
        #download button
        csv = sales_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data CSV",
            data=csv,
            file_name="sales_per_kategori.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("Visualisasi Kategori")
        
        #seleksi kategori
        kategori = st.selectbox("Pilih kategori:", sales_df['product_category_name_english'].unique())
    
        #filter
        filtered_df = sales_df[sales_df['product_category_name_english'] == kategori]
        
        #bar
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(filtered_df['product_category_name_english'], filtered_df['total_sales'], color="skyblue")
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', rotation=0)
            
        ax.set_xlabel('Kategori')
        ax.set_ylabel('Total Penjualan($) x 10^6')
        ax.set_title(f'Total Penjualan untuk {kategori}')
        plt.xticks(rotation=90)
        
        st.pyplot(fig)
        st.metric(
            label=f"Total Penjualan {kategori}", 
            value=f"${filtered_df['total_sales'].sum():.2f}M",
            delta=f"{filtered_df['total_sales'].sum() / sales_df['total_sales'].sum() * 100:.1f}% dari total"
        )
    
    with tab3:
        st.subheader("Top 10 Kategori berdasarkan Penjualan")
        
        #top 10 categories
        top_sales = sales_df.sort_values(by='total_sales', ascending=False).head(10)
        
        #horizontal bar chart for top 10
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(top_sales['product_category_name_english'], top_sales['total_sales'], color="skyblue")
        
        #tambahkan nilai di dalam bar
        for bar in bars:
            width = bar.get_width()
            ax.text(width/2, bar.get_y() + bar.get_height()/2,
                    f'{width:.2f}',
                    ha='center', va='center', color='black', fontweight='bold')
            
        ax.set_xlabel('Total Penjualan($) x 10^6')
        ax.set_ylabel('Kategori')
        ax.set_title('10 Kategori Produk dengan Penjualan Tertinggi')
        ax.invert_yaxis()  
        
        st.pyplot(fig)

#pemesan per city
elif option == "Total Order per Kota":
    st.header("Total Order per Kota")
    st.info(f"Menampilkan data untuk periode: {start_date.strftime('%d %B %Y')} sampai {end_date.strftime('%d %B %Y')}")
    
    #tab
    tab1, tab2, tab3, tab4 = st.tabs(["Data", "Visualisasi Kota", "Top 10 Kota", "Peta Persebaran"])
    
    with tab1:
        st.subheader("Data Order per Kota")
        st.dataframe(filtered_city_orders.head(number_of_rows))
        
        #button untuk donwload
        csv = filtered_city_orders.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data CSV",
            data=csv,
            file_name="order_per_kota_filtered.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("Visualisasi Kota")
        
        kota = st.selectbox("Pilih kota:", filtered_city_orders['customer_city'].unique())
        
        #filter
        filtered_city = filtered_city_orders[filtered_city_orders['customer_city'] == kota]
        
        #bar
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(filtered_city['customer_city'], filtered_city[city_count_col], color="lightgreen")
        
        #tambahkan nilai di atas bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
            
        ax.set_xlabel('Kota')
        ax.set_ylabel('Jumlah Order')
        ax.set_title(f'Total Order untuk {kota} ({start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")})')
        
        st.pyplot(fig)
        st.metric(
            label=f"Jumlah Order di {kota}", 
            value=f"{filtered_city[city_count_col].sum()}",
            delta=f"{filtered_city[city_count_col].sum() / filtered_city_orders[city_count_col].sum() * 100:.1f}% dari total"
        )
    
    with tab3:
        st.subheader("Top 10 Kota berdasarkan Jumlah Order")
        
        #top 10 cities
        top_cities = filtered_city_orders.sort_values(by=city_count_col, ascending=False).head(10)
        
        #horizontal bar chart for top 10
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(top_cities['customer_city'], top_cities[city_count_col], color="lightgreen")
        
        #tambahkan nilai di dalam bar
        for bar in bars:
            width = bar.get_width()
            ax.text(width/2, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}',
                    ha='center', va='center', color='black', fontweight='bold')
            
        ax.set_xlabel('Jumlah Order')
        ax.set_ylabel('Kota')
        ax.set_title(f'10 Kota dengan Jumlah Order Tertinggi ({start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")})')
        ax.invert_yaxis()  
        
        st.pyplot(fig)
    
    with tab4:
        st.subheader("Peta Persebaran Order Customer")
        with open('geospatial_map.html', 'r', encoding='utf-8') as f:
            html_data = f.read()
        st.components.v1.html(html_data, height=600, scrolling=True)

#pemesanan per state
else:
    st.header("Total Order per Negara Bagian")
    st.info(f"Menampilkan data untuk periode: {start_date.strftime('%d %B %Y')} sampai {end_date.strftime('%d %B %Y')}")
    
    #tab
    tab1, tab2, tab3, tab4 = st.tabs(["Data", "Visualisasi Negara Bagian", "Top 10 Negara Bagian", "Peta Persebaran"])
    
    with tab1:
        st.subheader("Data Order per Negara Bagian")
        st.dataframe(filtered_state_orders.head(number_of_rows))
        
        #button untuk download
        csv = filtered_state_orders.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data CSV",
            data=csv,
            file_name="order_per_state_filtered.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("Visualisasi Negara Bagian")
        
        #dapat memilih visualisasi
        chart_type = st.radio("Jenis visualisasi:", ["Bar Chart", "Pie Chart"])
        
        state = st.selectbox("Pilih negara bagian:", filtered_state_orders['customer_state'].unique())
        
        #filter
        filtered_state = filtered_state_orders[filtered_state_orders['customer_state'] == state]
        
        if chart_type == "Bar Chart":
            # bar
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(filtered_state['customer_state'], filtered_state[state_count_col], color="coral")
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom')
                
            ax.set_xlabel('Negara Bagian')
            ax.set_ylabel('Jumlah Order')
            ax.set_title(f'Total Order untuk {state} ({start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")})')
        else:
            #menggunakan visualisasi data pie chart
            fig, ax = plt.subplots(figsize=(10, 6))
            top_states = filtered_state_orders.sort_values(by=state_count_col, ascending=False).head(5)
            others = pd.DataFrame({
                'customer_state': ['Others'],
                state_count_col: [filtered_state_orders[state_count_col].sum() - top_states[state_count_col].sum()]
            })
            plot_data = pd.concat([top_states, others])
            explode = [0.1 if s == state else 0 for s in plot_data['customer_state']]
            
            ax.pie(plot_data[state_count_col], labels=plot_data['customer_state'], 
                   autopct='%1.1f%%', startangle=90, explode=explode,
                   colors=['coral', 'skyblue', 'lightgreen', 'violet', 'gold', 'gray'])
            ax.axis('equal')
            ax.set_title(f'Distribusi Order per Negara Bagian ({start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")})')
            
        st.pyplot(fig)
        st.metric(
            label=f"Jumlah Order di {state}", 
            value=f"{filtered_state[state_count_col].sum()}",
            delta=f"{filtered_state[state_count_col].sum() / filtered_state_orders[state_count_col].sum() * 100:.1f}% dari total"
        )
    
    with tab3:
        st.subheader("Top 10 Negara Bagian berdasarkan Jumlah Order")
        
        #top 10 states
        top_states = filtered_state_orders.sort_values(by=state_count_col, ascending=False).head(10)
        
        #horizontal bar chart for top 10
        fig, ax = plt.subplots(figsize=(10, 8))
        bars = ax.barh(top_states['customer_state'], top_states[state_count_col], color="coral")
        
        #tambahkan nilai di dalam bar
        for bar in bars:
            width = bar.get_width()
            ax.text(width/2, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}',
                    ha='center', va='center', color='black', fontweight='bold')
            
        ax.set_xlabel('Jumlah Order')
        ax.set_ylabel('Negara Bagian')
        ax.set_title(f'10 Negara Bagian dengan Jumlah Order Tertinggi ({start_date.strftime("%d %B %Y")} - {end_date.strftime("%d %B %Y")})')
        ax.invert_yaxis()  
        
        st.pyplot(fig)
    
    with tab4:
        st.subheader("Peta Persebaran Order Customer")
        with open('geospatial_map.html', 'r', encoding='utf-8') as f:
            html_data = f.read()
        st.components.v1.html(html_data, height=600, scrolling=True)



#footer
st.markdown("---")
st.markdown("Dashboard E-commerce")