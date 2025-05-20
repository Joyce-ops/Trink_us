# utils/favoriten.py

import requests
import io
import csv
from requests.auth import HTTPBasicAuth
import streamlit as st

def get_favoriten_url(username: str):
    base_url = st.secrets["webdav"]["base_url"]
    webdav_user = st.secrets["webdav"]["username"]
    password = st.secrets["webdav"]["password"]

    remote_path = f"{base_url}/files/{webdav_user}/trink_us/user_data_{username}/favoriten.csv"
    auth = HTTPBasicAuth(webdav_user, password)
    return remote_path, auth

def favoriten_laden(username: str):
    url, auth = get_favoriten_url(username)
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            csvfile = io.StringIO(response.text)
            reader = csv.DictReader(csvfile)
            return list(reader)
        else:
            return []
    except Exception as e:
        st.error(f"Fehler beim Laden der Favoriten: {e}")
        return []

def favoriten_speichern(username: str, favoriten_liste):
    url, auth = get_favoriten_url(username)
    try:
        if not favoriten_liste:
            csv_content = ""
        else:
            output = io.StringIO()
            fieldnames = favoriten_liste[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for fav in favoriten_liste:
                writer.writerow(fav)
            csv_content = output.getvalue()
        response = requests.put(
            url,
            data=csv_content.encode("utf-8"),
            headers={'Content-Type': 'text/csv'},
            auth=auth
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Fehler beim Speichern der Favoriten: {response.status_code}")
    except Exception as e:
        st.error(f"Fehler beim Speichern der Favoriten: {e}")
