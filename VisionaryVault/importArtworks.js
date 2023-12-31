const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const Artwork = require('./models/artwork');
const Artist = require('./models/artist');

require('dotenv').config();

const connectToDatabase = async () => {
  const dbURI = process.env.MONGODB_URI || 'mongodb://localhost:27017/gallery';
  try {
    await mongoose.connect(dbURI);
    console.log('Connected to MongoDB');
  } catch (err) {
    console.error('Failed to connect to MongoDB:', err);
    throw err;
  }
};

const findOrCreateArtist = async (artistName) => {
  try {
    let artist = await Artist.findOne({ name: artistName });
    if (!artist) {
      artist = new Artist({ name: artistName });
      await artist.save();
    }
    return artist;
  } catch (err) {
    console.error(`Error finding or creating artist: ${artistName}`, err);
    throw err;
  }
};

const importArtworks = async (jsonData) => {
  try {
    await Artwork.deleteMany({});
    for (const item of jsonData) {
      if (!item.Title || !item.Artist) {
        console.warn('Skipping invalid item:', item);
        continue;
      }

      const artist = await findOrCreateArtist(item.Artist);
      const artwork = new Artwork({
        title: item.Title,
        artist: artist._id,
        year: item.Year,
        category: item.Category,
        medium: item.Medium,
        description: item.Description,
        imageUrl: item.Poster,
      });

      await artwork.save();
      console.log(`Imported artwork: ${artwork.title}`);
    }
    console.log('Artworks imported successfully');
  } catch (err) {
    console.error('Failed to import artworks:', err);
    throw err;
  }
};

const main = async () => {
  try {
    await connectToDatabase();

    const jsonPath = path.join(__dirname, 'data', 'gallery.json');
    if (!fs.existsSync(jsonPath)) {
      throw new Error('JSON data file not found');
    }
    const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

    await importArtworks(jsonData);
  } catch (err) {
    console.error(err.message);
  } finally {
    mongoose.disconnect();
    console.log('MongoDB connection closed');
  }
};

if (require.main === module) {
  main();
}
