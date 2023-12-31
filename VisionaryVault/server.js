const express = require('express');
const mongoose = require('mongoose');
const session = require('express-session');
const MongoStore = require('connect-mongo');
const userRoutes = require('./routes/users');
const artworkRoutes = require('./routes/artworks');
const homeRoutes = require('./routes/homeRoutes');
require('dotenv').config();
const artistRoutes = require('./routes/artists'); 
const searchRoutes = require('./routes/search'); 

const app = express();

const mongoDB = process.env.MONGODB_URI || 'mongodb://localhost:27017/gallery';
mongoose.connect(mongoDB)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('Could not connect to MongoDB', err));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));
app.set('view engine', 'pug');
app.set('views', './views');

const sessionStore = MongoStore.create({ mongoUrl: mongoDB });
app.use(session({
  secret: 'mysecret',
  resave: false,
  saveUninitialized: true,
  store: sessionStore,
  cookie: {
    maxAge: 24 * 60 * 60 * 1000
  }
}));

app.use((req, res, next) => {
  res.locals.user = req.session.userId ? { _id: req.session.userId, username: req.session.username } : null;
  next();
});

app.use('/users', userRoutes);
app.use('/artworks', artworkRoutes);
app.use('/', homeRoutes);
app.use('/artists', artistRoutes);
app.use('/search', searchRoutes);

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server started on port ${port}`));
