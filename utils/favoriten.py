# utils/favoriten.py

import requests
import csv
import io
from requests.auth import HTTPBasicAuth
import streamlit as st

def get_remote_path(username):
    base_url = st.secrets["webdav"]["base_url"]
    user = st.secrets["webdav"]["username"]
    return f"{base_url}/files/{user}/trink_us/favoriten_{username}.csv"

def favoriten_laden(username):
    url = get_remote_path(username)
    auth = HTTPBasicAuth(st.secrets["webdav"]["username"], st.secrets["webdav"]["password"])
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            content = response.content.decode("utf-8")
            reader = csv.DictReader(io.StringIO(content))
            return list(reader)
        else:
            return []
    except Exception:
        return []

def favoriten_speichern(username, favoriten_liste):
    url = get_remote_path(username)
    auth = HTTPBasicAuth(st.secrets["webdav"]["username"], st.secrets["webdav"]["password"])
    output = io.StringIO()
    if favoriten_liste:
        writer = csv.DictWriter(output, fieldnames=favoriten_liste[0].keys())
        writer.writeheader()
        writer.writerows(favoriten_liste)
        data = output.getvalue()
        try:
            requests.put(url, data=data.encode("utf-8"), auth=auth)
        except Exception as e:
            st.error(f"Fehler beim Speichern der Favoriten: {e}")
