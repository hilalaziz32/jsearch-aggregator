# Job Search Frontend

A simple, modern web interface for the Job Search API.

## Features

- **Clean Search Interface**: Simple search bar with prominent search button
- **Advanced Settings**: Collapsible advanced search options
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Results**: Displays job listings with collapsible details
- **Export Functionality**: Download search results as Excel files
- **Keyboard Shortcuts**: 
  - `Ctrl/Cmd + Enter`: Quick search submission
  - `Escape`: Clear search field

## Setup

1. Ensure the backend API is running on `http://localhost:8000`
2. Open `frontend/index.html` in a web browser
3. Start searching for jobs!

## File Structure

```
frontend/
├── index.html          # Main HTML interface
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## Usage

### Basic Search
1. Enter job keywords in the search bar
2. Click "Search Jobs" or press `Ctrl/Cmd + Enter`
3. View results with collapsible job cards

### Advanced Search
1. Click "⚙️ Advanced Settings" to expand additional options
2. Configure parameters like:
   - Number of pages to search
   - Country code
   - Date posted filter
   - Employment types
   - Work from home options
   - And more...

### Results Features
- **Collapsible Job Cards**: Click to expand/collapse job details
- **Single Expansion**: Only one job card can be expanded at a time
- **Export to Excel**: Download search results as XLSX files
- **Responsive Layout**: Optimized for all screen sizes

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- **POST /search**: Submit job search queries
- **GET /export/xlsx/{request_id}**: Download Excel exports

## Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Troubleshooting

### Common Issues

1. **"Unable to connect to API"**
   - Ensure backend server is running on port 8000
   - Check browser console for CORS errors

2. **Search not working**
   - Verify internet connection
   - Check if API key is configured in backend

3. **Export links not working**
   - Ensure backend is running and can generate XLSX files
   - Check browser download settings

### Development Tips

- Open browser developer tools to debug API calls
- Check network tab for request/response details
- Console logs provide helpful debugging information

## Customization

### Styling
Modify `styles.css` to change the appearance:
- Colors and gradients
- Layout and spacing
- Responsive breakpoints

### Functionality
Extend `script.js` to add features:
- Additional form validation
- Search history
- Favorite jobs
- Custom filters
