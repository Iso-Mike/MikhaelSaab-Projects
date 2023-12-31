const express = require('express');
const Artwork = require('../models/artwork');
const router = express.Router();

function escapeRegex(text) {
  return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
}

router.get('/', async (req, res) => {
  const ITEMS_PER_PAGE = 5;
  const page = parseInt(req.query.page) || 1;
  const query = req.query.query;

  if (!query) {
    return res.redirect('/');
  }

  try {
    const regex = new RegExp(escapeRegex(query), 'i'); // Case-insensitive search

    // Optimized aggregation pipeline
    const matchStage = {
      $match: {
        $or: [
          { title: regex },
          { category: regex },
          { 'artistData.name': regex }
        ]
      }
    };
    const countStage = { $count: 'total' };
    const skipStage = { $skip: (page - 1) * ITEMS_PER_PAGE };
    const limitStage = { $limit: ITEMS_PER_PAGE };

    // Execute two separate pipelines for counting and fetching results
    const totalArtworks = await Artwork.aggregate([matchStage, countStage]);
    const artworks = await Artwork.aggregate([
      { $lookup: { from: 'artists', localField: 'artist', foreignField: '_id', as: 'artistData' } },
      { $unwind: '$artistData' },
      matchStage,
      skipStage,
      limitStage
    ]);

    res.render('searchResults', {
      artworks,
      query,
      currentPage: page,
      totalPages: Math.ceil((totalArtworks[0]?.total || 0) / ITEMS_PER_PAGE)
    });
  } catch (error) {
    console.error("Error in search:", error);
    res.status(500).send("Search functionality is currently unavailable. Please try again later.");
  }
});

module.exports = router;
