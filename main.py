import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import streamlit as st

# Load the CSV file
data_file = 'dataset_tempat_wisata3.csv'  # Pastikan path sudah benar
data = pd.read_csv(data_file, on_bad_lines='warn')

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
        <a href="#">Home</a>
        <a href="/rekomendasi">Rekomendasi</a>
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

# Main Content Section
st.markdown(
    """
    <div class="container mt-4">
        <h2>Selamat Datang di Sistem Rekomendasi Wisata Mojokerto!</h2>
        <p>
            Sistem ini dirancang untuk membantu mahasiswa Lamongan dan sekitarnya menemukan tempat wisata yang menarik di Kabupaten Mojokerto.
            Gunakan menu di atas untuk menjelajahi berbagai fitur sistem kami.
        </p>
        <h3>Fitur Sistem:</h3>
        <ul>
            <li>Rekomendasi Tempat Wisata</li>
            <li>Informasi Tempat Wisata</li>
            <li>Intgrasi Dengan Maps dan Transportasi Umum <sup> Coming Soon</sup> </li>
        </ul>
        
       
    </div>
    """,
    unsafe_allow_html=True
)
# Button to download guide book
# Tombol 1: Download Panduan
st.markdown(
    """
    <a href="https://www.google.com" target="_blank">
        <button style="background-color:  #D81F26; color: white; width: 200px; border: none; padding: 10px 20px; text-align: center; font-size: 16px; border-radius: 5px; cursor: pointer;">
            Download Panduan
        </button>
    </a>
    """,
    unsafe_allow_html=True
)

# Tombol 2: Lihat Source Code
st.markdown(
    """
    <a href="https://www.google.com" target="_blank">
        <button style="background-color:  #D81F26; color: white; width: 200px; margin-top: 10px; border: none; padding: 10px 20px; text-align: center; font-size: 16px; border-radius: 5px; cursor: pointer;">
            Lihat Source Code
        </button>
    </a>
    """,
    unsafe_allow_html=True
)


# Tambahkan elemen H2 di dalam kotak full-width
st.markdown(
    """
    <style>
    .responsive-box {
        display: flex;
        justify-content: center; /* Posisi teks di tengah secara horizontal */
        align-items: center; /* Posisi teks di tengah secara vertikal */
        text-align: center;
        background-color: #D81F26; /* Warna merah Netflix */
        color: white; /* Warna teks putih */
        margin: 20px 0; /* Margin vertikal */
        width: 100%; /* Lebar penuh layar */
        height: auto; /* Tinggi kotak */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Tambahkan bayangan */
    }
    </style>
    <div class="responsive-box">
        <h4>Tempat Wisata yang Dapat Kamu Kunjungi</h4>
    </div>
    """,
    unsafe_allow_html=True
)


# Assuming the CSV has columns 'Nama_Tempat_Wisata', 'Jenis_Tempat_Wisata', 'Deskripsi', and 'url_gambar'
name_column = 'Nama_Tempat_Wisata'  # Change as needed
jenis_column = 'jenis_wisata'  # Change as needed
description_column = 'Deskripsi '  # Change as needed
image_url_column = 'url_gambar'  # Change as needed

# Loop through the rows to display data and images
for index, row in data.iterrows():
    image_url = row['url_gambar']

    # Card Container
    st.markdown(
        f"""
        <div class="card-container">
            <!-- Image Section -->
            <div class="card-img">
                <img src="{row[image_url_column]}" alt="{row[name_column]}">
            </div>
            <!-- Text Section -->
            <div class="card-text">
                <h3>{row[name_column]}</h3>
                <p><b>Jenis Wisata:</b> {row[jenis_column]}</p>
                <p>{row[description_column]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )


