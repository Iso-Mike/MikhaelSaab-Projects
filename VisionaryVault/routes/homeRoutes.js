const express = require('express');
const router = express.Router();
const Artwork = require('../models/artwork');

// Home route to display featured artworks
router.get('/', async (req, res) => {
  try {
    const featuredArtworks = await Artwork.find().sort({ likes: -1 }).limit(6);

    res.render('index', { featuredArtworks });
  } catch (error) {
    console.error(error);
    res.status(500).send('Internal Server Error');
  }
});

module.exports = router;