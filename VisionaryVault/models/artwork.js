const mongoose = require('mongoose');

const artworkSchema = new mongoose.Schema({
  title: { type: String, required: true, trim: true },
  artist: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Artist',
    required: true
  },
  year: {
    type: String,
    validate: {
      validator: function(v) {
        return /\d{4}/.test(v);
      },
      message: props => `${props.value} is not a valid year!`
    },
  },
  category: { type: String, trim: true },
  medium: { type: String, trim: true },
  description: { type: String, trim: true },
  imageUrl: {
    type: String,
    required: true,
    trim: true
  },
  likes: [{ type: mongoose.Schema.Types.ObjectId, ref: 'User' }],
  reviews: [{
    author: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    content: { type: String, required: true },
    rating: {
      type: Number,
      min: 1,
      max: 5
    },
    createdAt: { type: Date, default: Date.now }
  }]
}, {
  timestamps: true
});

module.exports = mongoose.model('Artwork', artworkSchema);
