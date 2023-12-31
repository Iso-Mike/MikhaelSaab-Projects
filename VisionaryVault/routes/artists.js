const express = require('express');
const Artist = require('../models/artist');
const Artwork = require('../models/artwork');
const User = require('../models/user');
const router = express.Router();

// Display all artists
router.get('/', async (req, res) => {
  try {
      const artists = await Artist.find();
      const user = req.session.userId ? await User.findById(req.session.userId) : null;
      res.render('artistList', { artists, user });
  } catch (error) {
      console.error("Error fetching artists:", error);
      res.status(500).render('errorPage', { error: "Error fetching artists" });
  }
});

// Display an artist's profile along with their artworks
router.get('/:artistId', async (req, res) => {
  try {
    const artistId = req.params.artistId;
    const artist = await Artist.findById(artistId);
    const artworks = await Artwork.find({ artist: artistId });
    const totalFollowers = await User.countDocuments({ followedArtists: artistId });

    const user = req.session.userId ? await User.findById(req.session.userId) : null;
    let isFollowing = false;
    if (user && user.followedArtists.includes(artistId)) {
      isFollowing = true;
    }

    if (!artist) {
      return res.status(404).send("Artist not found");
    }

    res.render('artistProfile', { artist, artworks, totalFollowers, isFollowing });
  } catch (error) {
    console.error("Error fetching artist details: ", error);
    res.status(500).send("Error fetching artist details");
  }
});

// Follow an artist
router.post('/:artistId/follow', async (req, res) => {
  try {
    const userId = req.session.userId;
    const artistId = req.params.artistId;
    await User.updateOne({ _id: userId }, { $addToSet: { followedArtists: artistId } });
    res.redirect('/artists');
  } catch (error) {
    res.status(500).send("Error following artist");
  }
});

// Unfollow an artist
router.post('/:artistId/unfollow', async (req, res) => {
  try {
    const userId = req.session.userId;
    const artistId = req.params.artistId;
    await User.updateOne({ _id: userId }, { $pull: { followedArtists: artistId } });
    res.redirect('/artists');
  } catch (error) {
    res.status(500).send("Error unfollowing artist");
  }
});

module.exports = router;