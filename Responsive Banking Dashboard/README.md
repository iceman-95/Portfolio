# 🏦 Global Trust Bank - Responsive Banking Dashboard

A modern, responsive banking dashboard built with pure HTML and CSS. This project demonstrates a professional banking interface with real transaction data, spending analytics, and a fully responsive design that works across all devices.

## ✨ Features

### 🎨 **Modern Design**
- Clean, professional banking interface
- Dark/Light theme toggle
- Smooth animations and hover effects
- Professional color scheme and typography
- Card-based layout with subtle shadows

### 📱 **Fully Responsive**
- **Desktop**: Full navigation with multi-column layouts
- **Tablet**: Adaptive grid layouts
- **Mobile**: Stacked layouts with simplified navigation
- Responsive breakpoints at 700px for optimal mobile experience

### 🏦 **Banking Features**
- **Account Overview**: Multiple account types (Total Available, Savings)
- **Transaction History**: Detailed transaction list with categories
- **Spending Analytics**: Real-time spending progress and insights
- **Quick Actions**: Send Money, Pay Bills, Transfer, Download
- **Notifications**: Real-time banking alerts
- **Advanced Filtering**: Filter transactions by date, category, and amount
- **User Profile**: Security settings and account management

### 💰 **Real Transaction Data**
- Connected to actual transaction history
- Real spending calculations (₾1,212.30 total expenses)
- Category-based spending analysis
- Budget tracking with progress bars
- Smart spending insights

## 🚀 Getting Started

### Prerequisites
- Any modern web browser
- No additional dependencies required

### Installation
1. Clone or download the project files
2. Open `dashboard.html` in your web browser
3. Navigate between Dashboard and Transactions pages

### File Structure
```
Banking Dashboard/
├── dashboard.html          # Main dashboard page
├── transactions.html       # Transaction history page
├── style.css              # Shared stylesheet
├── pngegg.png            # Bank logo
├── acc_p.png             # User profile picture
└── README.md             # This file
```

## 📋 Pages Overview

### 🏠 Dashboard Page (`dashboard.html`)
- **Account Cards**: Display account balances and status
- **Money Spent Section**: Real-time spending analytics with progress bar
- **Quick Actions**: Common banking functions
- **Notifications**: Real-time alerts modal
- **Theme Toggle**: Switch between light and dark modes

### 📊 Transactions Page (`transactions.html`)
- **Transaction List**: Detailed transaction history with categories
- **Filter System**: Advanced filtering by date, category, and amount
- **Summary Cards**: Total income, expenses, and net balance
- **Spending Chart**: Category-based spending visualization
- **Export Functionality**: Download transaction data

## 🎯 Key Features

### 💳 **Account Management**
- Multiple account types (Total Available, Savings)
- Real-time balance display
- Account status indicators
- Masked account numbers for security

### 📈 **Spending Analytics**
- Real transaction data integration
- Progress bar showing budget usage
- Category-based spending breakdown
- Smart insights and recommendations
- Monthly budget tracking

### 🔍 **Advanced Filtering**
- Date range filtering (Today, Week, Month, etc.)
- Category-based filtering
- Amount range filtering
- Real-time filter application

### 🌙 **Theme System**
- Light/Dark theme toggle
- Consistent theming across all components
- Smooth theme transitions
- Professional color schemes

## 🛠️ Technical Details

### **Pure HTML & CSS**
- No JavaScript frameworks used
- No CSS frameworks (Bootstrap, Tailwind, etc.)
- Vanilla JavaScript for minimal interactivity
- Semantic HTML5 structure

### **Responsive Design**
```css
@media (max-width: 700px) {
    /* Mobile-specific styles */
    .accounts-list { flex-direction: column; }
    .navbar { flex-direction: column; }
    .transaction-row { flex-direction: column; }
}
```

### **Design System**
- **Colors**: Professional blue theme (#1a237e, #3949ab)
- **Typography**: Segoe UI font family
- **Spacing**: Consistent padding and margins
- **Components**: Reusable card, button, and modal styles

## 📊 Transaction Data

### **Real Spending Breakdown**
- **Total Expenses**: ₾1,212.30
- **Categories**: Groceries, Restaurant, Utilities, Transport, Shopping, Income
- **Top Category**: Shopping (₾435.28)
- **Budget**: ₾3,000 monthly budget
- **Progress**: 40.4% spent (healthy spending)

### **Transaction Categories**
- 🛒 **Groceries**: ₾192.12
- 🍽️ **Restaurant**: ₾260.60
- ⚡ **Utilities**: ₾189.81
- 🚗 **Transport**: ₾65.50
- 🛍️ **Shopping**: ₾435.28
- 💸 **Income**: ₾2,450.00

## 🎨 Design Features

### **Professional UI Elements**
- Modern card-based layout
- Subtle shadows and borders
- Smooth hover animations
- Professional iconography (Font Awesome)
- Consistent spacing and typography

### **Interactive Components**
- Clickable account cards
- Hover effects on buttons
- Modal dialogs for notifications
- Dropdown menus for user profile
- Theme toggle switch

### **Accessibility**
- Semantic HTML structure
- Proper alt text for images
- Keyboard navigation support
- High contrast color schemes
- Responsive text sizing

## 🔧 Customization

### **Changing Bank Name**
Edit the `<h1>` tag in both HTML files:
```html
<h1>Your Bank Name</h1>
```

### **Updating Logo**
Replace `pngegg.png` with your logo file and update the src attribute:
```html
<img src="your-logo.png" alt="Your Bank Logo" class="logo">
```

### **Modifying Colors**
Update the CSS variables in `style.css`:
```css
:root {
    --primary-color: #1a237e;
    --secondary-color: #3949ab;
    --accent-color: #00bcd4;
}
```

## 📱 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers

## 🚀 Deployment

### **Local Development**
1. Download all project files
2. Open `dashboard.html` in your browser
3. Navigate between pages using the navigation bar

### **Web Server Deployment**
1. Upload all files to your web server
2. Ensure `style.css` is in the same directory
3. Access via `dashboard.html`

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test across different devices
5. Submit a pull request

## 📞 Support

For questions or support, please open an issue in the repository.
