const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser'); // Explicitly require body-parser
const app = express();
const port = 3030;

app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json()); // Enable JSON parsing for request bodies

// Read JSON data
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

// Connect to MongoDB with error handling
mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' })
  .then(() => console.log("MongoDB connected"))
  .catch(err => console.error("MongoDB connection error:", err));

const Reviews = require('./review');
const Dealerships = require('./dealership');

// Initialize Database: Delete existing data and insert new data
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data.reviews); // Changed bracket notation to dot notation
    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealerships_data.dealerships); // Changed bracket notation to dot notation
    console.log('Data insertion completed successfully.');
  } catch (error) {
    console.error('Error during data insertion:', error);
  }
})();

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({ dealership: req.params.id }); // Changed bracket notation to dot notation if applicable
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/state/:state', async (req, res) => {
  try {
    const documents = await Dealerships.find({ state: req.params.state }); // Changed bracket notation to dot notation if applicable
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const document = await Dealerships.findById(req.params.id);
    if (!document) {
      return res.status(404).json({ error: 'Dealer not found' });
    }
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

// Express route to insert review
app.post('/insert_review', async (req, res) => { // Removed express.raw middleware as express.json() is already used
  try {
    const data = req.body; // Changed to use parsed JSON directly
    const documents = await Reviews.find().sort({ id: -1 });
    let new_id = documents[0] ? documents[0].id + 1 : 1; // Changed bracket notation to dot notation

    const review = new Reviews({
      id: new_id, // Changed to dot notation
      name: data.name, // Changed to dot notation
      dealership: data.dealership, // Changed to dot notation
      review: data.review, // Changed to dot notation
      purchase: data.purchase, // Changed to dot notation
      purchase_date: data.purchase_date, // Changed to dot notation
      car_make: data.car_make, // Changed to dot notation
      car_model: data.car_model, // Changed to dot notation
      car_year: data.car_year, // Changed to dot notation
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Express route to update a review
app.put('/update_review/:id', async (req, res) => {
  try {
    const data = req.body;

    // Basic validation
    if (!data.name || !data.dealership || !data.review) { // Changed bracket notation to dot notation if applicable
      return res.status(400).json({ error: 'Missing required fields: name, dealership, review' });
    }

    const updatedReview = await Reviews.findByIdAndUpdate(req.params.id, data, { new: true });
    if (!updatedReview) {
      return res.status(404).json({ error: 'Review not found' });
    }
    res.json(updatedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error updating review' });
  }
});

// Express route to delete a review
app.delete('/delete_review/:id', async (req, res) => {
  try {
    const deletedReview = await Reviews.findByIdAndDelete(req.params.id);
    if (!deletedReview) {
      return res.status(404).json({ error: 'Review not found' });
    }
    res.json({ message: 'Review deleted successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error deleting review' });
  }
});

// Express route to update a dealership
app.put('/update_dealer/:id', async (req, res) => {
  try {
    const data = req.body;

    const updatedDealer = await Dealerships.findByIdAndUpdate(req.params.id, data, { new: true });
    if (!updatedDealer) {
      return res.status(404).json({ error: 'Dealer not found' });
    }
    res.json(updatedDealer);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error updating dealer' });
  }
});

// Express route to delete a dealership
app.delete('/delete_dealer/:id', async (req, res) => {
  try {
    const deletedDealer = await Dealerships.findByIdAndDelete(req.params.id);
    if (!deletedDealer) {
      return res.status(404).json({ error: 'Dealer not found' });
    }
    res.json({ message: 'Dealer deleted successfully' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error deleting dealer' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
