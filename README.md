# Climate Community Platform

A safe, calm, and inclusive online space for people around the world—especially those affected by climate change—to share experiences, emotions, and knowledge.

## Features

- **User Authentication**: Secure signup, login, and logout with password hashing
- **Community Forum**: Create posts, comment, and react to posts with categories:
  - Heatwaves
  - Flooding
  - Strong winds & storms
  - Emotional & mental health impacts
  - Daily life experiences
- **Seville Page**: Dedicated information about climate change impacts in Seville, Spain
- **Learn Page**: Verified external climate resources (IPCC, NASA, WHO)
- **Community Guidelines**: Clear guidelines for respectful participation
- **Content Reporting**: System for reporting inappropriate content
- **Healing Earth Section**: Reflective content on nature's value, human dignity, and ethical responsibility

## Design

- **Glassmorphism UI**: Inspired by Apple iOS 26 design with blurred, glassy interfaces
- **Nature Aesthetic**: Greens, blues, and earth tones with calm, peaceful design
- **Light & Dark Mode**: Toggle between light and dark themes
- **Mobile-First**: Responsive design that works on all devices
- **Accessible**: Built with accessibility in mind

## Technology Stack

- **Backend**: Python + Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5
- **Templates**: Jinja2

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
gec2/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── climate_community.db   # SQLite database (created on first run)
├── templates/            # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── forum.html
│   ├── create_post.html
│   ├── view_post.html
│   ├── seville.html
│   ├── learn.html
│   ├── guidelines.html
│   └── healing_earth.html
└── static/               # Static files
    ├── css/
    │   └── style.css    # Glassmorphism styles
    └── js/
        └── main.js      # JavaScript for interactions
```

## Database Schema

The application automatically creates the following tables on first run:

- **users**: User accounts with authentication
- **posts**: Forum posts with categories
- **comments**: Comments on posts
- **reactions**: Likes/support reactions on posts
- **reports**: Content reports for moderation

## Usage

1. **Sign Up**: Create an account to participate in the community
2. **Browse Forum**: View posts by category or all posts
3. **Create Posts**: Share your experiences and knowledge
4. **Engage**: Comment on posts and show support with reactions
5. **Learn**: Access verified climate resources
6. **Report**: Report inappropriate content to maintain community safety

## Security Notes

- **Production Deployment**: Change the `SECRET_KEY` in `app.py` before deploying to production
- **Password Security**: Passwords are hashed using Werkzeug's secure password hashing
- **Session Management**: Uses Flask sessions for user authentication
- **SQL Injection Protection**: Uses parameterized queries

## Community Values

- **Safety**: A safe space for everyone
- **Empathy**: Understanding and compassion
- **Respect**: Respectful dialogue always
- **Inclusion**: Everyone is welcome

## License

This project is created for educational and community purposes.

## Support

For questions or issues, please refer to the Community Guidelines page within the application.

---

**Remember**: You are not alone in this journey. This community is here to support you.

