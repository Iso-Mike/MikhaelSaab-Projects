# Art Gallery Management System

## Author
Mikhael Saab

## Overview
The Art Gallery Management System is a comprehensive web application designed for efficient management of art galleries. It leverages modern web technologies and database management systems to streamline the handling of artworks, artists, and user interactions. Built with a focus on modular and maintainable code, the system is adaptable and scalable, catering to the evolving needs of art galleries.

## Features
- **Efficient Artwork Management:** Utilizes robust data handling for artworks, including listing, addition, and detailed views.
- **Artist Profiles and Management:** Manages artist data effectively, allowing for artist profile creation, editing, and viewing.
- **User Interaction:** Facilitates user functionalities such as registration, login, liking artworks, and adding reviews.
- **Dynamic Data Interaction:** Employs MongoDB for data storage, ensuring flexible and scalable data management.
- **Responsive Web Design:** Delivers a user-friendly interface compatible with various devices and screen sizes.
- **Robust Error Handling:** Rigorously handles user input errors and system faults to provide a stable and reliable experience.
- **File Upload Capability:** Integrates file handling for artwork images, supporting image uploads.

## Source Files
- `server.js`: Main server setup and configuration.
- `users.js`: Handles user-related routes and functionalities.
- `artworks.js`: Manages artwork-related routes and operations.
- `artists.js`: Responsible for artist-related routes and functionalities.
- `search.js`: Implements search functionalities for artworks and artists.

## Additional Files and Directories
- `models/`: Contains Mongoose models for data schema.
- `routes/`: Routing files for different modules.
- `views/`: Pug templates for rendering HTML.
- `public/`: Static files like stylesheets and client-side scripts.

## How to Compile and Run
- **Installation:** Run `npm install` & `node importArtworks.js` to install dependencies and initialize artworks.
- **Execution:** Start the server with `npm start` or `node server.js`.

## Usage Instructions
- **Starting the Server:** Run the server using `npm start` or `node server.js`.
- **Accessing the Application:** Open a web browser and go to `http://localhost:3000` (or the configured port).
- **Navigating the Website:** Use the website's navigation to explore artworks, artists, and user features.

