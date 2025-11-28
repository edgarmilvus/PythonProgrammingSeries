
#
# These sources are part of the "PyThon Programming Series" by Edgar Milvus, 
# you can find it on Amazon: https://www.amazon.com/dp/B0FTTQNXKG or
# https://tinyurl.com/PythonProgrammingSeries 
# New books info: https://linktr.ee/edgarmilvus 
#
# MIT License
# Copyright (c) 2025 Edgar Milvus
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Source File: solution_exercise_5.py
# Description: Solution for Exercise 5
# ==========================================

# (Assuming the Flask app and basic setup from above are present)

# --- 5. Dynamic Versioning Implementation ---

def get_file_mtime(filename):
    """
    Calculates the last modification timestamp for a static file.
    Returns the timestamp as an integer string for use as a version parameter.
    """
    try:
        # Construct the full filesystem path
        filepath = os.path.join(current_app.static_folder, filename)
        
        # Check if the file exists
        if os.path.exists(filepath):
            # Get modification time (mtime) and convert to integer for URL
            mtime = int(os.path.getmtime(filepath))
            return str(mtime)
        return None
    except Exception:
        # Fallback if file access fails
        return 'fallback'

# Register the function as a global Jinja utility
app.jinja_env.globals['static_mtime'] = get_file_mtime

@app.route('/dynamic_version')
def dynamic_version_index():
    # Renders the template that uses the dynamic version
    return render_template('dynamic_index.html')


# --- JINJA TEMPLATE (templates/dynamic_index.html) ---

DYNAMIC_VERSION_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dynamic Versioned Assets</title>
    
    <!-- DYNAMIC LINK (Using the custom function 'static_mtime'): -->
    <link rel="stylesheet" 
          href="{{ url_for('static', 
                          filename='main.css', 
                          v=static_mtime('main.css')) }}">
</head>
<body>
    <h1>Testing Dynamic Cache Busting</h1>
    <p>The 'v' parameter should now be a timestamp (e.g., v=1678886400).</p>
</body>
</html>
"""

if __name__ == '__main__':
    # Example usage:
    # To run this, you would need to ensure the template files are saved 
    # with the content defined above and the static file 'main.css' exists.
    # print(f"Static URL (Static Version): {url_for('static_version_index', _external=True)}")
    # print(f"Static URL (Dynamic Version): {url_for('dynamic_version_index', _external=True)}")
    # app.run(debug=True)
    pass
