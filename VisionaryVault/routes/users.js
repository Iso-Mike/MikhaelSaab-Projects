const express = require('express');
const bcrypt = require('bcryptjs');
const User = require('../models/user');
const Artist = require('../models/artist');
const Artwork = require('../models/artwork');
const router = express.Router();

const requireLogin = (req, res, next) => {
  if (!req.session.userId) {
    return res.redirect('/login');
  }
  next();
};

router.get('/login', (req, res) => {
  if (req.session.userId) {
    return res.redirect('/');
  }
  res.render('login');
});

router.get('/register', (req, res) => {
  if (req.session.userId) {
    return res.redirect('/');
  }
  res.render('register');
});

router.post('/register', async (req, res) => {
  try {
    const { username, password, accountType } = req.body;
    if (!['patron', 'artist'].includes(accountType)) {
      return res.status(400).render('register', { error: 'Invalid account type' });
    }
    
    const existingUser = await User.findOne({ username });
    if (existingUser) {
      return res.render('register', { error: 'Username already exists.' });
    }

    const hashedPassword = await bcrypt.hash(password, 12);
    const newUser = new User({
      username,
      password: hashedPassword,
      accountType
    });

    await newUser.save();
    res.redirect('/users/login');
  } catch (error) {
    res.status(500).render('register', { error: 'Server error.' });
  }
});

router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (user && await bcrypt.compare(password, user.password)) {
      req.session.userId = user._id;
      req.session.username = user.username;
      res.redirect('/');
    } else {
      res.render('login', { error: 'Invalid credentials.' });
    }
  } catch (error) {
    res.status(500).render('login', { error: 'Server error.' });
  }
});

router.get('/logout', (req, res) => {
  req.session.destroy(() => {
    res.redirect('/');
  });
});

// Upgrade to artist account
router.post('/upgrade-to-artist', requireLogin, async (req, res) => {
  try {
    const user = await User.findById(req.session.userId);

    if (!user) {
      return res.status(404).send("User not found");
    }

    if (user.accountType === 'patron') {
      let artist = await Artist.findOne({ name: user.username });
      if (!artist) {
        artist = new Artist({ name: user.username });
        await artist.save();
      }

      res.redirect('/artworks/add');
    } else {
      res.status(400).send("Already an artist account");
    }
  } catch (error) {
    console.error("Error in upgrade to artist:", error);
    res.status(500).send("Internal server error");
  }
});

// User Profile Route
router.get('/profile', requireLogin, async (req, res) => {
  try {
    const user = await User.findById(req.session.userId)
      .populate('followedArtists');

    const likedArtworks = await Artwork.find({ likes: req.session.userId });

    const reviews = await Artwork.find({ 'reviews.author': req.session.userId })
      .populate({
        path: 'reviews.author',
        select: 'username' 
      });

    if (!user) {
      return res.status(404).send('User not found');
    }

    res.render('profile', { user, likedArtworks, reviews });
  } catch (error) {
    res.status(500).send(error.message);
  }
});

router.post('/downgrade-to-patron', requireLogin, async (req, res) => {
  const user = await User.findById(req.session.userId);
  if (user.accountType === 'artist') {
    user.accountType = 'patron';
    await user.save();
    res.redirect('/users/profile');
  } else {
    res.status(400).send("Already a patron account");
  }
});

router.post('/unfollow-artist/:artistId', requireLogin, async (req, res) => {
  const userId = req.session.userId;
  const artistId = req.params.artistId;
  await User.findByIdAndUpdate(userId, { $pull: { followedArtists: artistId } });
  res.redirect('/profile');
});

module.exports = router;
