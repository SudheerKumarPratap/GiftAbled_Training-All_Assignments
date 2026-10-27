const mongoose = require('mongoose');

// Student Schema
const StudentSchema = new mongoose.Schema({
    name: { type: String, required: true },
    rollNumber: { type: String, required: true, unique: true },
    email: { type: String, required: true },
    department: String
});

// Library Schema
const LibrarySchema = new mongoose.Schema({
    bookTitle: { type: String, required: true },
    author: { type: String, required: true },
    isbn: { type: String, required: true, unique: true },
    status: { type: String, enum: ['Available', 'Checked out'], default: 'Available' }
});

// Fest Schema
const FestSchema = new mongoose.Schema({
    eventName: { type: String, required: true },
    coordinator: { type: String, required: true },
    date: { type: Date, required: true },
    budget: Number
});

module.exports = {
    Student: mongoose.model('Student', StudentSchema),
    Library: mongoose.model('Library', LibrarySchema),
    Fest: mongoose.model('Fest', FestSchema)
};
