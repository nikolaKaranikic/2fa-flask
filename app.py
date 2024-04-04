from flask import Flask, request, render_template_string
import pyotp

app = Flask(__name__)

# Generate a secret for a user (this should be stored securely and associated with the user account)
user_secret = pyotp.random_base32()

@app.route('/')
def index():
    # Generate a TOTP URI for the QR Code
    totp_uri = pyotp.totp.TOTP(user_secret).provisioning_uri(name="user@example.com", issuer_name="YourApp")
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?data={totp_uri}&size=200x200"
    # Simple form for testing OTP verification
    form_html = '''
        <div>
            <img src="{{ qr_code_url }}" alt="Scan with your authenticator app"/>
            <form action="/verify" method="post">
                <input type="text" name="otp" placeholder="Enter OTP" required>
                <input type="submit" value="Verify OTP">
            </form>
        </div>
    '''
    return render_template_string(form_html, qr_code_url=qr_code_url)

@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form['otp']
    totp = pyotp.TOTP(user_secret)
    if totp.verify(otp):
        return "OTP is valid!"
    else:
        return "Invalid OTP."

if __name__ == '__main__':
    app.run(debug=True)
