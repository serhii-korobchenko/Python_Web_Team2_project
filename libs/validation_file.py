ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'mp4', 'xlsx', 'doxc', 'xls', 'avi', 'MPEG', 'WEBM'}
PICTURE = {'png', 'jpg', 'jpeg', 'gif'}
VIDEO = {'mp4', 'avi', 'MPEG', 'WEBM'}
DOCUMENT = {'xlsx','docx', 'xls', 'pdf', 'txt', 'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in VIDEO

def picture(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in PICTURE

def doc(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in DOCUMENT
