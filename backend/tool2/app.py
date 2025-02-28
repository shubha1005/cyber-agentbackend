# from flask import Flask, request, jsonify, Blueprint
# import socket

# # Define the Blueprint for tool2
# tool2 = Blueprint('tool2', __name__)

# # Manually add CORS headers for tool2
# @tool2.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all domains (you can specify specific domains if needed)
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     return response

# def scan_ports(ip, ports):
#     results = {}
#     for port in ports:
#         results[port] = "Open" if scan_port(ip, port) else "Closed"
#     return results

# def scan_port(ip, port):
#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.settimeout(1)
#             s.connect((ip, port))
#             return True
#     except:
#         return False

# @tool2.route("/scan", methods=["POST"])
# def scan():
#     data = request.get_json()
#     ip = data.get("ip")
#     ports = data.get("ports", [])
#     try:
#         ports = list(map(int, ports))
#     except ValueError:
#         return jsonify({"error": "Invalid ports input"}), 400
#     results = scan_ports(ip, ports)
#     return jsonify(results)

# # Don't use `app.run` here in a blueprint; it's managed by the main app.
from flask import Flask, request, jsonify, Blueprint
import socket

# Define the Blueprint for tool2
tool2 = Blueprint('tool2', __name__)

# Manually add CORS headers for tool2
@tool2.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def scan_ports(ip, ports):
    results = {}
    for port in ports:
        results[port] = "Open" if scan_port(ip, port) else "Closed"
    return results

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            return True
    except:
        return False

def resolve_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

@tool2.route("/scan", methods=["POST"])
def scan():
    data = request.get_json()
    target = data.get("target")  # Can be IP or domain
    port_range = data.get("port_range", "")  # Expecting "20-80" format
    
    # Resolve domain to IP if needed
    ip = resolve_domain(target) if not target.replace('.', '').isdigit() else target
    if not ip:
        return jsonify({"error": "Invalid domain or IP"}), 400
    
    # Process port range
    try:
        start_port, end_port = map(int, port_range.split("-"))
        ports = list(range(start_port, end_port + 1))
    except ValueError:
        return jsonify({"error": "Invalid port range"}), 400
    
    results = scan_ports(ip, ports)
    return jsonify({"ip": ip, "results": results})
# from flask import Flask, request, jsonify, Blueprint
# import socket
# from flask_cors import CORS

# # Define the Blueprint for tool2
# tool2 = Blueprint('tool2', __name__)

# # Manually add CORS headers for tool2
# @tool2.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
#     return response

# def scan_ports(ip, ports):
#     results = {}
#     for port in ports:
#         results[port] = "Open" if scan_port(ip, port) else "Closed"
#     return results

# def scan_port(ip, port):
#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.settimeout(1)
#             s.connect((ip, port))
#             return True
#     except:
#         return False

# def resolve_domain(domain):
#     try:
#         return socket.gethostbyname(domain)
#     except socket.gaierror:
#         return None

# @tool2.route("/scan", methods=["POST"])
# def scan():
#     data = request.get_json()
#     target = data.get("target")  # Can be IP or domain
#     port_range = data.get("port_range", "")  # Expecting "20-80" format
#     selected_ports = data.get("selected_ports", [])  # List of specific ports
    
#     # Resolve domain to IP if needed
#     ip = resolve_domain(target) if not target.replace('.', '').isdigit() else target
#     if not ip:
#         return jsonify({"error": "Invalid domain or IP"}), 400
    
#     # Process port range
#     ports = set(selected_ports)  # Use a set to avoid duplicates
#     try:
#         if port_range:
#             start_port, end_port = map(int, port_range.split("-"))
#             ports.update(range(start_port, end_port + 1))
#     except ValueError:
#         return jsonify({"error": "Invalid port range"}), 400
    
#     results = scan_ports(ip, sorted(ports))
#     return jsonify({"ip": ip, "results": results})
# from flask import Flask, request, jsonify, Blueprint
# import socket
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend

# tool2 = Blueprint('tool2', __name__)

# def scan_ports(ip, ports):
#     results = {}
#     for port in ports:
#         results[port] = "Open" if scan_port(ip, port) else "Closed"
#     return results

# def scan_port(ip, port):
#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.settimeout(1)
#             s.connect((ip, port))
#             return True
#     except:
#         return False

# @tool2.route("/scan", methods=["POST"])
# def scan():
#     data = request.get_json()
#     target = data.get("ip")  # This can be an IP or domain
#     port_range = data.get("port_range")  # Example: "20-100"
#     selected_ports = data.get("selected_ports", [])  # Example: [22, 80, 443]

#     # Resolve domain to IP (if needed)
#     try:
#         ip = socket.gethostbyname(target)
#     except socket.gaierror:
#         return jsonify({"error": "Invalid domain or IP"}), 400

#     # Convert port range to list
#     ports = []
#     if port_range:
#         try:
#             start_port, end_port = map(int, port_range.split("-"))
#             ports = list(range(start_port, end_port + 1))
#         except ValueError:
#             return jsonify({"error": "Invalid port range format"}), 400

#     # Add selected ports (from checkboxes)
#     ports.extend(selected_ports)

#     if not ports:
#         return jsonify({"error": "No ports provided"}), 400

#     # Remove duplicates and sort
#     ports = sorted(set(ports))

#     # Scan and return results
#     results = scan_ports(ip, ports)
#     return jsonify({"ip": ip, "results": results})

# # Register blueprint
# app.register_blueprint(tool2, url_prefix='/tool2')

# if __name__ == "__main__":
#     app.run(debug=True)
