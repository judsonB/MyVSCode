import qrcode

def generate_qr_code():
  # Take URL input from the user
  url = input("Enter the URL to generate a QR Code: ")
  
  # Generate QR Code
  qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
  )
  qr.add_data(url)
  qr.make(fit=True)

  # Create an image of the QR Code
  img = qr.make_image(fill_color="black", back_color="white")
  
  # Save the QR Code image
  img.save("qrcode.png")
  print("QR Code generated and saved as 'qrcode.png'.")

if __name__ == "__main__":
  generate_qr_code()