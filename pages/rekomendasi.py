import pandas as pd
import sklearn 
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .navbar {
        background-color: #D81F26; /* Darker background */
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .navbar a {
        color: white;
        text-decoration: none;
        margin: 0 15px;
        font-size: 18px;
        font-weight: bold;
    }
    .navbar a:hover {
        text-decoration: none;
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #D81F26;
        min-width: 160px;
        box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
        z-index: 1;
    }
    .dropdown-content a {
        color: white;
        padding: 8px 16px;
        text-decoration: none;
        display: block;
    }
    .dropdown-content a:hover {
        background-color: #D81F26;
        text-decoration: none;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }
    .header {
        text-align: center;
        margin: 20px 0;
    }
    .header img {
        max-width: 160px;
        height: auto;
        margin: 0 20px;
    }
    .header h1 {
        font-size: 32px;
        color: #fff;
        margin-top: 10px;
    }
    .header h3 {
        font-size: 20px;
        color: #aaa;
    }
    

    /* CSS for Card Styling */
    .card-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        background-color: #1f1f1f;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        transition: border-color 0.3s ease;
        border: 2px solid transparent; /* Initial border color */
    }

    .card-container:hover {
        border-color: #D81F26; /* Change border color to red */
    }

    .card-img {
        flex: 1;
        text-align: center;
    }

    .card-img img {
        width: 200px;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
    }

    .card-text {
        flex: 3;
        padding-left: 20px;
    }

    .card-text h3 {
        color: #E50914;
        margin-bottom: 10px;
    }

    .card-text h2 {
        color: #E50914;
        
    }

    .card-text p {
        color: #ccc;
    }

    </style>

    <!-- Header Section -->
    <div class="header">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UTM_DIKBUDRISTEK.png/2048px-UTM_DIKBUDRISTEK.png" alt="Logo Universitas">
        <h1>Sistem Rekomendasi Wisata Mojokerto</h1>
        <h3>Untuk Mahasiswa Lamongan dan Sekitarnya</h3>
    </div>

    <!-- Navbar Section -->
    <div class="navbar">
        <a href="main.py">Home</a>
        <a href="rekomendasi.py">Rekomendasi</a>
        <div class="dropdown">
            <a href="#">Contact</a>
            <div class="dropdown-content">
                <a href="#email">Email</a>
                <a href="#phone">Phone</a>
                <a href="#address">Address</a>
            </div>
        </div>
        <a href="#">About</a>
    </div>
    """,
    unsafe_allow_html=True
)

# load dataset
data_user = pd.read_csv('dataset_user_aka_responden_lolos_filterfixx.csv')
data_rating = pd.read_csv('dataset_rating_per_user.csv')
data_tempat_wisata = pd.read_csv('dataset_tempat_wisata3.csv')

st.markdown(
    """
    <style>
    .centered-title {
        text-align: center; /* Memusatkan teks */
        color: white; /* Opsional: mengatur warna teks */
        margin-top: 20px; /* Opsional: spasi atas */
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown('<h2 class="centered-title">Isi Data Diri Anda Untuk Mendapatkan Rekomendasi Wisata</h2>', unsafe_allow_html=True)
# Input pengguna
asal = st.selectbox("Pilih asal Anda:", ["Lamongan", "Non Lamongan"])

# Logika untuk User Profile Filtering
if asal == "Lamongan":
    usia = st.number_input("Masukkan usia Anda:", min_value=18, max_value=26)
    
    if usia == 20:
        st.write("Anda berada dalam usia 20 tahun.")
        jenis_kelamin = st.selectbox("Pilih jenis kelamin Anda:", ["Pilih Jenis Kelamin", "Laki-Laki", "Perempuan"])
        
        if jenis_kelamin == "Laki-Laki":
            # Profil dominan cocok (usia 20 tahun, laki-laki)
            st.write("Profil Anda cocok dengan pengguna dominan.")
            st.write("Mencari rekomendasi berbasis profil dan rating pengguna...")
            
            # Item-Based Collaborative Filtering
            rating_matrix = data_rating.pivot_table(
                index="id_user", 
                columns="id_tempat_wisata", 
                values="rating"
            ).fillna(0)

            similarity_matrix = cosine_similarity(rating_matrix.T)
            similarity_df = pd.DataFrame(
                similarity_matrix, 
                index=rating_matrix.columns, 
                columns=rating_matrix.columns
            )


            if st.button("Lihat Hasil Rekomendasi"):
   
                # Ambil rata-rata rating setiap tempat wisata
                rating_rata_rata = data_rating.groupby("id_tempat_wisata")["rating"].mean()

                #st.subheader("Perhitungan Selisih Kuadrat, Akar, dan Perkalian Matriks Berpasangan:")
                
                # Tambahkan kolom baru untuk menyimpan selisih (rating - rata-rata) dan hasil kuadratnya
                data_rating["rating_minus_mean"] = data_rating.apply(
                    lambda row: row["rating"] - rating_rata_rata[row["id_tempat_wisata"]],
                    axis=1
                )
                data_rating["squared_diff"] = data_rating["rating_minus_mean"] ** 2  # Kuadratkan selisihnya

                # Totalkan selisih kuadrat
                total_squared_diff = data_rating["squared_diff"].sum()
                
                # Akarkan total selisih kuadrat (RMS - Root Mean Square)
                rms = total_squared_diff ** 0.5

                # Proses Rating Matrix
                rating_matrix = data_rating.pivot_table(
                    index="id_user", 
                    columns="id_tempat_wisata", 
                    values="rating"
                ).fillna(0)

                # Hitung Similarity Matrix
                similarity_matrix = cosine_similarity(rating_matrix.T)
                similarity_df = pd.DataFrame(
                    similarity_matrix, 
                    index=rating_matrix.columns, 
                    columns=rating_matrix.columns
                )

                # Perkalian Matriks Berpasangan
                multiplied_matrix = similarity_matrix * rms  # Perkalian matriks similarity dengan RMS
                multiplied_df = pd.DataFrame(
                    multiplied_matrix, 
                    index=rating_matrix.columns, 
                    columns=rating_matrix.columns
                )

                # Hitung Similarity dari Hasil Perkalian Matriks
                #st.subheader("Similarity dari Hasil Perkalian Matriks:")
                similarity_from_multiplied_matrix = cosine_similarity(multiplied_df)
                similarity_multiplied_df = pd.DataFrame(
                    similarity_from_multiplied_matrix, 
                    index=rating_matrix.columns, 
                    columns=rating_matrix.columns
                )

                # Tampilkan matriks similarity dari hasil perkalian
                #st.write("Matrix Similarity dari Hasil Perkalian Matriks:")
                #st.dataframe(similarity_multiplied_df)

                if 'similarity_multiplied_df' not in locals():
                    st.warning("Matriks similarity belum dihitung. Hitung matriks similarity terlebih dahulu!")
                else:
                    #st.subheader("Prediksi Rating Menggunakan Weighted Average of Deviation")

                    # Dictionary untuk menyimpan hasil prediksi rating
                    predicted_ratings = {}

                    # Loop melalui semua tempat wisata untuk menghitung prediksi rating
                    for item_id in similarity_multiplied_df.index:
                        numerator = 0  # Pembilang
                        denominator = 0  # Penyebut

                        # Ambil similaritas dengan tempat wisata lainnya
                        similarity_scores = similarity_multiplied_df[item_id]

                        # Iterasi melalui semua tempat wisata yang dirating oleh user
                        for rated_item_id in data_rating["id_tempat_wisata"].unique():
                            # Ambil similarity score dengan tempat wisata lainnya
                            similarity = similarity_scores[rated_item_id]

                            # Cek apakah tempat wisata memiliki rating
                            rated_item_ratings = data_rating[data_rating["id_tempat_wisata"] == rated_item_id]

                            if not rated_item_ratings.empty:
                                # Ambil rata-rata rating user
                                mean_user_ratings = rated_item_ratings.groupby("id_user")["rating"].mean().to_dict()

                                # Loop untuk semua user yang sudah merating tempat wisata ini
                                for user_id, rating in rated_item_ratings[["id_user", "rating"]].values:
                                    deviation = rating - mean_user_ratings[user_id]  # Selisih dari rata-rata user
                                    numerator += similarity * deviation
                                    denominator += abs(similarity)

                        # Hitung prediksi rating jika penyebut tidak nol
                        if denominator != 0:
                            predicted_rating = rating_rata_rata[item_id] + (numerator / denominator)
                            predicted_ratings[item_id] = predicted_rating

                    # Tampilkan hasil prediksi rating
                    #st.subheader("Top Prediksi Rating:")
                    top_predictions = sorted(predicted_ratings.items(), key=lambda x: x[1], reverse=True)[:5]

                   # Tampilkan rekomendasi dengan prediksi rating
                    st.subheader("Rekomendasi Tempat Untukmu:")

                    for place_id, pred_rating in top_predictions:
                        # Ambil data tempat wisata
                        place_row = data_tempat_wisata[data_tempat_wisata["id_tempat_wisata"] == place_id].iloc[0]

                        # Alasan rekomendasi
                        reason = f"Prediksi rating untuk tempat wisata ini adalah {pred_rating:.2f}, yang menunjukkan kemungkinan tinggi untuk disukai oleh pengguna seperti Anda."

                        # Render dalam format kartu HTML
                        st.markdown(
                            f"""
                            <div class="card-container">
                                <!-- Image Section -->
                                <div class="card-img">
                                    <img src="{place_row['url_gambar']}" alt="{place_row['Nama_Tempat_Wisata']}">
                                </div>
                                <!-- Text Section -->
                                <div class="card-text">
                                    <h3>{place_row['Nama_Tempat_Wisata']}</h3>
                                    <p><b>Jenis Wisata:</b> {place_row['jenis_wisata']}</p>
                                    <p>{place_row['Deskripsi ']}</p>
                                    <p class="reason">{reason}</p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )



        else:
            if st.button("Lihat Hasil Rekomendasi"):
                # Fallback untuk jenis kelamin berbeda
                st.write("Profil Anda tidak sesuai dengan pengguna dominan. Menampilkan rekomendasi berdasarkan rating rata-rata.")
                
                # Hitung rata-rata rating untuk setiap tempat wisata
                avg_rating = data_rating.groupby("id_tempat_wisata")["rating"].mean().sort_values(ascending=False)
                st.subheader("Rekomendasi Berdasarkan Rating Rata-Rata:")

                # Loop untuk menampilkan top 3 tempat wisata dengan styling seperti contoh
                for place_id in avg_rating.head(3).index:
                    # Ambil data tempat wisata dari dataset
                    place_row = data_tempat_wisata[data_tempat_wisata["id_tempat_wisata"] == place_id].iloc[0]
                    rating_avg = avg_rating[place_id]  # Rata-rata rating
                    
                    # Alasan kenapa masuk top rekomendasi
                    reason = f"Tempat wisata ini memiliki rating rata-rata tertinggi sebesar {rating_avg:.1f} dibandingkan tempat wisata lainnya."
                    
                    # Render HTML untuk setiap rekomendasi
                    st.markdown(
                        f"""
                        <div class="card-container">
                            <!-- Image Section -->
                            <div class="card-img">
                                <img src="{place_row['url_gambar']}" alt="{place_row['Nama_Tempat_Wisata']}">
                            </div>
                            <!-- Text Section -->
                            <div class="card-text">
                                <h3>{place_row['Nama_Tempat_Wisata']}</h3>
                                <p><b>Jenis Wisata:</b> {place_row['jenis_wisata']}</p>
                                <p>{place_row['Deskripsi ']}</p>
                                <p style="color: #555; font-style: italic;">{reason}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    else:
       # Fallback untuk usia di luar 20 tahun
        st.write("Anda berada di luar usia 20 tahun.")
        selected_category = st.selectbox("Pilih Kategori Wisata:", data_tempat_wisata["jenis_wisata"].unique())

        if st.button("Lihat Hasil Rekomendasi"):
            st.write("Menampilkan rekomendasi berdasarkan kategori wisata...")

            # Jika pengguna memilih kategori, gunakan kategori tersebut
            if selected_category:
                st.write(f"Kategori yang dipilih: {selected_category}")
                
                # Ambil tempat wisata berdasarkan kategori yang dipilih pengguna
                top_places = data_tempat_wisata[data_tempat_wisata["jenis_wisata"] == selected_category]
            else:
                # Fallback: Jika tidak ada pilihan, gunakan kategori dengan rating rata-rata tertinggi
                st.write("Tidak ada kategori yang dipilih, menampilkan kategori populer...")
                avg_rating_by_category = data_rating.merge(data_tempat_wisata, on="id_tempat_wisata")
                category_recommendation = avg_rating_by_category.groupby("jenis_wisata")["rating"].mean().sort_values(ascending=False).index[0]
                st.write(f"Kategori Wisata Populer: {category_recommendation}")

                # Ambil tempat wisata dari kategori populer
                top_places = data_tempat_wisata[data_tempat_wisata["jenis_wisata"] == category_recommendation]

            # Tampilkan rekomendasi berdasarkan kategori
            st.subheader("Rekomendasi Tempat Wisata:")
            if not top_places.empty:
                for _, place_row in top_places.iterrows():
                    # Alasan untuk kategori wisata
                    reason = f"Tempat wisata ini termasuk dalam kategori '{place_row['jenis_wisata']}' yang paling sesuai dengan preferensi Anda."

                    # Render setiap tempat wisata dengan styling seperti contoh
                    st.markdown(
                        f"""
                        <div class="card-container">
                            <!-- Image Section -->
                            <div class="card-img">
                                <img src="{place_row['url_gambar']}" alt="{place_row['Nama_Tempat_Wisata']}">
                            </div>
                            <!-- Text Section -->
                            <div class="card-text">
                                <h3>{place_row['Nama_Tempat_Wisata']}</h3>
                                <p><b>Jenis Wisata:</b> {place_row['jenis_wisata']}</p>
                                <p>{place_row['Deskripsi ']}</p>
                                <p style="color: #555; font-style: italic;">{reason}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.write("Maaf, tidak ada tempat wisata yang sesuai dengan kategori ini.")
else:
    if asal == "Non Lamongan":
        st.write("Anda berasal dari luar Lamongan.")
    
        # Input preferensi jenis wisata
        jenis_wisata_preferensi = st.selectbox(
            "Pilih jenis wisata favorit Anda:",
            options=["Pilih Jenis Wisata", "Alam", "Budaya", "Hiburan"]
        )

        if st.button("Lihat Hasil Rekomendasi"):
            if jenis_wisata_preferensi != "Pilih Jenis Wisata":
                # Filter tempat wisata berdasarkan jenis wisata
                tempat_wisata_preferensi = data_tempat_wisata[data_tempat_wisata["jenis_wisata"] == jenis_wisata_preferensi]

                # Ambil tempat dengan rating rata-rata tertinggi dalam kategori
                avg_rating = data_rating.groupby("id_tempat_wisata")["rating"].mean().sort_values(ascending=False)
                rekomendasi_terfilter = avg_rating[avg_rating.index.isin(tempat_wisata_preferensi["id_tempat_wisata"])]

                # Tampilkan rekomendasi
                st.subheader(f"Rekomendasi Berdasarkan Jenis Wisata '{jenis_wisata_preferensi}':")
                for place_id in rekomendasi_terfilter.head(3).index:
                    place_row = data_tempat_wisata[data_tempat_wisata["id_tempat_wisata"] == place_id].iloc[0]
                    rating_avg = rekomendasi_terfilter[place_id]  # Rata-rata rating

                    # Alasan rekomendasi
                    reason = f"Tempat wisata ini memiliki rating rata-rata {rating_avg:.1f} dalam kategori '{jenis_wisata_preferensi}', menjadikannya salah satu pilihan terbaik."

                    # Render rekomendasi dalam format HTML dengan styling
                    st.markdown(
                        f"""
                        <div class="card-container">
                            <!-- Image Section -->
                            <div class="card-img">
                                <img src="{place_row['url_gambar']}" alt="{place_row['Nama_Tempat_Wisata']}">
                            </div>
                            <!-- Text Section -->
                            <div class="card-text">
                                <h3>{place_row['Nama_Tempat_Wisata']}</h3>
                                <p><b>Jenis Wisata:</b> {place_row['jenis_wisata']}</p>
                                <p>{place_row['Deskripsi ']}</p>
                                <p style="color: #555; font-style: italic;">{reason}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                # Fallback ke rekomendasi berbasis rating rata-rata
                st.write("Anda belum memilih preferensi. Menampilkan rekomendasi berdasarkan rating rata-rata tertinggi.")
                avg_rating = data_rating.groupby("id_tempat_wisata")["rating"].mean().sort_values(ascending=False)

                st.subheader("Rekomendasi Berdasarkan Rating Tertinggi:")
                for place_id in avg_rating.head(3).index:
                    place_row = data_tempat_wisata[data_tempat_wisata["id_tempat_wisata"] == place_id].iloc[0]
                    rating_avg = avg_rating[place_id]  # Rata-rata rating

                    # Alasan rekomendasi fallback
                    reason = f"Tempat wisata ini memiliki rating rata-rata tertinggi sebesar {rating_avg:.1f}, menjadikannya rekomendasi terbaik secara keseluruhan."

                    # Render fallback rekomendasi dalam format HTML dengan styling
                    st.markdown(
                        f"""
                        <div class="card-container">
                            <!-- Image Section -->
                            <div class="card-img">
                                <img src="{place_row['url_gambar']}" alt="{place_row['Nama_Tempat_Wisata']}">
                            </div>
                            <!-- Text Section -->
                            <div class="card-text">
                                <h3>{place_row['Nama_Tempat_Wisata']}</h3>
                                <p><b>Jenis Wisata:</b> {place_row['jenis_wisata']}</p>
                                <p>{place_row['Deskripsi ']}</p>
                                <p style="color: #555; font-style: italic;">{reason}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
