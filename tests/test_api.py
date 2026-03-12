import pytest
from api import app

@pytest.fixture
def client():
    # This sets up a "virtual" version of your website to test against
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    """Verify the home page returns a 200 OK status."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"EchoSplit AI" in response.data

def test_allowed_file_logic():
    """Verify our file extension guard works."""
    from api import allowed_file
    assert allowed_file("song.mp3") is True
    assert allowed_file("data.pdf") is False
    assert allowed_file("beat.WAV") is True  # Tests case sensitivity

def test_upload_no_file(client):
    """Verify the API handles empty uploads gracefully."""
    response = client.post('/upload')
    assert response.status_code == 200 # Flask returns 200 even for custom error messages
    assert b"No file part" in response.data

def test_allowed_file_no_extension():
    """Verify files without extensions are rejected."""
    from api import allowed_file
    assert allowed_file("no_extension_file") is False

def test_allowed_file_multiple_dots():
    """Verify security against double-extension attacks (e.g., song.exe.mp3)."""
    from api import allowed_file
    # This should be True because the actual extension is .mp3
    assert allowed_file("malicious.exe.mp3") is True
    # This should be False because the actual extension is .exe
    assert allowed_file("fake_song.mp3.exe") is False

def test_upload_invalid_extension(client):
    """Verify the server returns a 400 error for bad file types."""
    data = {
        'file': (open(__file__, 'rb'), 'test.txt') # Uploading this script as a .txt
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b"File type not supported" in response.data

def test_download_all_404(client):
    """Verify the zip route returns 404 if the song folder doesn't exist."""
    response = client.get('/download_all/non_existent_song')
    assert response.status_code == 404