

global.crypto=require(  'crypto');
const express = require('express');
const mongoose = require('mongoose');
const methodOverride = require('method-override');
const path = require('path');
const { Student, Library, Fest } = require('./models');

const app = express()

// MongoDB Connection
mongoose.connect('mongodb://127.0.0.1:27017/campusDB')
    .then(() => console.log('Connected to MongoDB Context'))
    .catch(err => console.error('DB Connection Error:', err));

// Middleware
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.urlencoded({ extended: true }));
app.use(methodOverride('_method'));

// --- HOME ROUTE ---
app.get('/', (req, res) => res.render('index'));

// ==========================================
// 1. STUDENT CRUD ROUTES
// ==========================================
app.get('/students', async (req, res) => {
    const students = await Student.find({});
    res.render('students', { students });
});

app.post('/students', async (req, res) => {
    await Student.create(req.body);
    res.redirect('/students');
});

app.put('/students/:id', async (req, res) => {
    await Student.findByIdAndUpdate(req.id || req.params.id, req.body);
    res.redirect('/students');
});

app.delete('/students/:id', async (req, res) => {
    await Student.findByIdAndDelete(req.params.id);
    res.redirect('/students');
});

// ==========================================
// 2. LIBRARY CRUD ROUTES
// ==========================================
app.get('/library', async (req, res) => {
    const books = await Library.find({});
    res.render('library', { books });
});

app.post('/library', async (req, res) => {
    await Library.create(req.body);
    res.redirect('/library');
});

app.put('/library/:id', async (req, res) => {
    await Library.findByIdAndUpdate(req.params.id, req.body);
    res.redirect('/library');
});

app.delete('/library/:id', async (req, res) => {
    await Library.findByIdAndDelete(req.params.id);
    res.redirect('/library');
});

// ==========================================
// 3. FEST CRUD ROUTES
// ==========================================
app.get('/fest', async (req, res) => {
    const fests = await Fest.find({});
    res.render('fest', { fests });
});

app.post('/fest', async (req, res) => {
    await Fest.create(req.body);
    res.redirect('/fest');
});

app.put('/fest/:id', async (req, res) => {
    await Fest.findByIdAndUpdate(req.params.id, req.body);
    res.redirect('/fest');
});

app.delete('/fest/:id', async (req, res) => {
    await Fest.findByIdAndDelete(req.params.id);
    res.redirect('/fest');
});

// Start Server
app.listen(3000, () => console.log('Server running on http://localhost:3000'));
