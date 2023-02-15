Database Structure

Status
	Name
  Color
  
Cart
	Store (Which User)
  Order # (User #)
  Internal Order ID (UUID)
  Client Address
  Client Address 2
  Client City
  Client Zip
  Client State
  Client Email
  Client Phone
  Current Status (CartStatus)
  Invoice (ForeignKey)
  
CartItem
	Product
  ProductSize
  Qty
  Image 
  
CartStatus
	Status (ForeignKey)
  Cart (ForeignKey)
  Current (Boolean)
  Date Started
  Date Completed

Product
	Name
  Cut File (File)
  Belongs_to (Users)
  
ProductSize
	Product
  Width MM
  Height MM
  

Invoice (CSVUpload)
	File (CSV)
  Date Approved
  Date Paid
  
UserPaymentMethod 
	Stripe Credit/Card Token
	PayPal Token
  