Group members: Nand Patel, Amitoj Uppal, and Rahman Mohamad

# Movie Watchlist Application
This project is a movie watchlist application that allows users to add, view, and manage movies they want to watch. They can simply add a movie to wishlist that they want to watch. It also provides functionalities for user management, including adding and deleting users.

## Live Link
Enjoy fast and seemless experience. Cheers.

You can access the live version of this application [here](https://nand.pythonanywhere.com/).

## Features

- User authentication: Users can register, login, and logout securely.
- Watchlist management: Users can add movies to their watchlist, view their watchlist, and remove movies from their watchlist.
- Movie search: Users can search for movies using the integrated movie database API.
- User deletion: Users can delete their account, removing all associated data including the watchlist.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/BTP405/project-2-group_13naa.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`.

## Usage

1. Register an account or login with existing credentials.
2. Search for movies using the search bar.
3. Add movies to your watchlist by clicking the "Add to Watchlist" button on movie details page (Only for logged in users).
4. View your watchlist by clicking the "Watchlist" link in the navigation bar.
5. Remove movies from your watchlist by clicking the "Remove" button next to each movie.
6. Logout securely when done.

## Testing

Run unit tests using:

```bash
python manage.py test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Feel free to customize the content to match your project's specifics, such as features, installation instructions, usage guidelines, and contribution guidelines.
