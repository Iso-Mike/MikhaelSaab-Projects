const express = require('express');
const Artwork = require('../models/artwork');
const router = express.Router();
const User = require('../models/user');
const Artist = require('../models/artist');
const mongoose = require('mongoose');

const multer = require('multer');
const upload = multer({ dest: 'uploads/' }); 

// Pagination settings
const ITEMS_PER_PAGE = 5;

const storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, 'public/images')
  },
  filename: function(req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname))
  }
});

const requireLogin = (req, res, next) => {
  if (!req.session || !req.session.userId) {
    return res.redirect('/login');
  }
  next();
};

// Helper function to calculate pagination
function calculatePagination(totalItems, currentPage) {
  return {
    currentPage,
    totalPages: Math.ceil(totalItems / ITEMS_PER_PAGE),
  };
}

// Helper function to escape regex characters
function escapeRegex(text) {
  return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
}

// Display all artworks with pagination
router.get('/', async (req, res) => {
  const page = parseInt(req.query.page) || 1;
  const sort = req.query.sort || 'title';
  const skip = (page - 1) * ITEMS_PER_PAGE;

  let sortOptions = {};
  let aggregateOptions = [];

  switch (sort) {
    case 'mostLiked':
      aggregateOptions.push({ $addFields: { likesCount: { $size: "$likes" } } });
      sortOptions = { likesCount: -1 };
      break;
    case 'mostCommented':
      aggregateOptions.push({ $addFields: { reviewsCount: { $size: "$reviews" } } });
      sortOptions = { reviewsCount: -1 };
      break;
    case 'title':
    default:
      sortOptions = { title: 1 }; 
      break;
  }

  try {
    const totalArtworks = await Artwork.countDocuments();

    aggregateOptions.push(
      { $sort: sortOptions },
      { $skip: skip },
      { $limit: ITEMS_PER_PAGE },
      { $lookup: {
          from: 'artists',
          localField: 'artist',
          foreignField: '_id',
          as: 'artist'
        }
      },
      { $unwind: '$artist' }
    );

    const artworks = await Artwork.aggregate(aggregateOptions);

    const pagination = calculatePagination(totalArtworks, page);

    res.render('artworkGallery', { artworks, ...pagination, sort: req.query.sort || 'title' });
  } catch (error) {
    res.status(500).send("Error fetching artworks: " + error.message);
  }
});

router.get('/add', requireLogin, (req, res) => {
  res.render('addArtwork');
});

// Like an artwork
router.post('/:artworkId/like', async (req, res) => {
  try {
    const artworkId = req.params.artworkId;
    const artwork = await Artwork.findById(artworkId).populate('artist');
    const userId = req.session.userId;

    // Check if the user is the artist of the artwork
    if (artwork.artist._id.toString() === userId) {
      return res.status(403).send("You cannot like your own artwork.");
    }

    if (artwork.likes.includes(userId)) {
      artwork.likes.pull(userId);
    } else {
      artwork.likes.push(userId);
    }

    await artwork.save();
    res.redirect(`/artworks/${artworkId}`);
  } catch (error) {
    console.error("Error updating artwork like:", error);
    res.status(500).send("Error updating artwork like");
  }
});

// Add review to an artwork
router.post('/:artworkId/addReview', async (req, res) => {
  try {
    const artworkId = req.params.artworkId;
    const userId = req.session.userId;
    const { content } = req.body;

    if (!content) {
      return res.status(400).send("Review content is required.");
    }

    const artwork = await Artwork.findById(artworkId).populate('artist');
    if (!artwork) {
      return res.status(404).send("Artwork not found.");
    }

    // Check if the user is the artist of the artwork
    if (artwork.artist._id.toString() === userId) {
      return res.status(403).send("You cannot review your own artwork.");
    }

    artwork.reviews.push({ author: userId, content });
    await artwork.save();

    res.redirect(`/artworks/${artworkId}`);
  } catch (error) {
    console.error("Error adding review:", error);
    res.status(500).send("Error adding review");
  }
});

// Delete a review from an artwork
router.post('/:artworkId/deleteReview/:reviewIndex', requireLogin, async (req, res) => {
  try {
    const { artworkId, reviewIndex } = req.params;
    const userId = req.session.userId;

    const artwork = await Artwork.findById(artworkId);
    if (!artwork) {
      return res.status(404).send("Artwork not found.");
    }

    // Check if the review was made by the logged-in user
    if (artwork.reviews[reviewIndex].author.toString() !== userId) {
      return res.status(403).send("You can only delete your own reviews.");
    }

    // Remove the review
    artwork.reviews.splice(reviewIndex, 1);
    await artwork.save();

    res.redirect(`/artworks/${artworkId}`);
  } catch (error) {
    console.error("Error deleting review:", error);
    res.status(500).send("Error deleting review");
  }
});

router.get('/:artworkId', async (req, res) => {
  try {
    const artworkId = req.params.artworkId;
    const artwork = await Artwork.findById(artworkId)
      .populate('artist')
      .populate({
        path: 'reviews.author',
        model: 'User',
        select: 'username'
      });

    if (!artwork) {
      return res.status(404).send("Artwork not found");
    }

    // Convert reviews to a format that can be safely accessed in the Pug template
    artwork.reviews = artwork.reviews.map(review => {
      return {
        ...review.toObject(),
        author: review.author ? review.author : { username: 'Unknown' },
        createdAt: review.createdAt ? review.createdAt.toLocaleDateString() : 'Unknown date'
      };
    });

    // Fetch related artworks
    const relatedArtworks = await Artwork.find({
      artist: artwork.artist._id,
      _id: { $ne: artworkId }
    }).limit(5);

    res.render('artworkDetail', { artwork, relatedArtworks });
  } catch (error) {
    console.error("Error fetching artwork details: ", error);
    res.status(500).send("Error fetching artwork details");
  }
});

router.post('/add', requireLogin, upload.single('image'), async (req, res) => {
  try {
    const userId = req.session.userId;
    const user = await User.findById(userId);
    const { title, description, year, category, medium } = req.body;
    const image = req.file;

    if (!image) {
      return res.status(400).send("Image file is required.");
    }

    const imageUrl = `/uploads/${image.filename}`;

    let artist = await Artist.findOne({ name: user.username });
    if (!artist) {
      artist = new Artist({ name: user.username });
      await artist.save();
    }

    const newArtwork = new Artwork({
      title,
      description,
      year,
      category,
      medium,
      artist: artist._id,
      imageUrl
    });

    await newArtwork.save();

    // Update user to artist if they are still a patron
    if (user.accountType === 'patron') {
      user.accountType = 'artist';
      await user.save();
    }

    res.redirect('/users/profile'); // Redirect to the user's profile
  } catch (error) {
    console.error("Error adding new artwork:", error);
    res.status(500).send("Error adding new artwork");
  }
});

module.exports = router;