"""
Main application entry point for the WebRTC communication server.
"""
import os
import ssl
import asyncio
from pathlib import Path
from aiohttp import web
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

from .signaling import signaling_server
from .auth import register_user, login_user
from .rooms import room_manager


# Configuration
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", 8443))
STATIC_DIR = Path(__file__).parent.parent / "static"
CERTS_DIR = Path(__file__).parent.parent / "certs"


def generate_ssl_certs():
    """Generate self-signed SSL certificates for development."""
    CERTS_DIR.mkdir(exist_ok=True)
    
    key_path = CERTS_DIR / "key.pem"
    cert_path = CERTS_DIR / "cert.pem"
    
    if key_path.exists() and cert_path.exists():
        print("SSL certificates already exist.")
        return key_path, cert_path
    
    print("Generating self-signed SSL certificates...")
    
    # Generate private key
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Generate certificate
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "WebRTC App"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
            ]),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    
    # Write key
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Write certificate
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print(f"SSL certificates generated at {CERTS_DIR}")
    return key_path, cert_path


async def handle_register(request: web.Request) -> web.Response:
    """Handle user registration."""
    try:
        data = await request.json()
        username = data.get("username", "").strip()
        password = data.get("password", "")
        
        result = await register_user(username, password)
        
        if result["success"]:
            return web.json_response(result)
        else:
            return web.json_response(result, status=400)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


async def handle_login(request: web.Request) -> web.Response:
    """Handle user login."""
    try:
        data = await request.json()
        username = data.get("username", "").strip()
        password = data.get("password", "")
        
        result = await login_user(username, password)
        
        if result["success"]:
            return web.json_response(result)
        else:
            return web.json_response(result, status=401)
    except Exception as e:
        return web.json_response({"success": False, "error": str(e)}, status=500)


async def handle_stats(request: web.Request) -> web.Response:
    """Get server statistics."""
    stats = room_manager.get_stats()
    return web.json_response(stats)


async def handle_index(request: web.Request) -> web.Response:
    """Serve the main HTML page."""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return web.FileResponse(index_path)
    return web.Response(text="Index not found", status=404)


def create_app() -> web.Application:
    """Create and configure the aiohttp application."""
    app = web.Application()
    
    # API routes
    app.router.add_post("/api/register", handle_register)
    app.router.add_post("/api/login", handle_login)
    app.router.add_get("/api/stats", handle_stats)
    
    # WebSocket route
    app.router.add_get("/ws", signaling_server.handle_websocket)
    
    # Static files
    if STATIC_DIR.exists():
        app.router.add_static("/static/", STATIC_DIR, name="static")
        app.router.add_get("/", handle_index)
    
    return app


def main():
    """Run the server."""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║           WebRTC Communication App Server                 ║
║                                                           ║
║  🔒 Secure Audio/Video Calls & Text Messaging             ║
╚═══════════════════════════════════════════════════════════╝
""")
    
    # Generate SSL certificates
    key_path, cert_path = generate_ssl_certs()
    
    # Create SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(str(cert_path), str(key_path))
    
    # Create and run app
    app = create_app()
    
    print(f"🚀 Server starting on https://{HOST}:{PORT}")
    print(f"📁 Static files: {STATIC_DIR}")
    print(f"⚠️  Note: Accept the self-signed certificate warning in your browser")
    print()
    
    web.run_app(app, host=HOST, port=PORT, ssl_context=ssl_context)


if __name__ == "__main__":
    main()
