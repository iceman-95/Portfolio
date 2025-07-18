let books = [];
let users = [];
let bookIdCounter = 1;

function initializeData() {
    // Sample books
    const sampleBooks = [
        { title: "The Great Gatsby", author: "F. Scott Fitzgerald", genre: "Classic", rating: 4.5, year: 1925 },
        { title: "To Kill a Mockingbird", author: "Harper Lee", genre: "Classic", rating: 4.8, year: 1960 },
        { title: "1984", author: "George Orwell", genre: "Dystopian", rating: 4.6, year: 1949 },
        { title: "Pride and Prejudice", author: "Jane Austen", genre: "Romance", rating: 4.4, year: 1813 },
        { title: "The Hobbit", author: "J.R.R. Tolkien", genre: "Fantasy", rating: 4.7, year: 1937 },
        { title: "The Catcher in the Rye", author: "J.D. Salinger", genre: "Coming-of-age", rating: 4.2, year: 1951 },
        { title: "Lord of the Flies", author: "William Golding", genre: "Allegory", rating: 4.3, year: 1954 },
        { title: "Animal Farm", author: "George Orwell", genre: "Allegory", rating: 4.5, year: 1945 },
        { title: "The Alchemist", author: "Paulo Coelho", genre: "Adventure", rating: 4.1, year: 1988 },
        { title: "Brave New World", author: "Aldous Huxley", genre: "Dystopian", rating: 4.4, year: 1932 },
        { title: "The Lord of the Rings", author: "J.R.R. Tolkien", genre: "Fantasy", rating: 4.9, year: 1954 },
        { title: "Jane Eyre", author: "Charlotte Brontë", genre: "Gothic", rating: 4.3, year: 1847 },
        { title: "Wuthering Heights", author: "Emily Brontë", genre: "Gothic", rating: 4.2, year: 1847 },
        { title: "The Picture of Dorian Gray", author: "Oscar Wilde", genre: "Gothic", rating: 4.4, year: 1890 },
        { title: "Frankenstein", author: "Mary Shelley", genre: "Gothic", rating: 4.3, year: 1818 }
    ];

    // Add books to the system
    sampleBooks.forEach(book => {
        addBook(book);
    });

    // Sample users
    const sampleUsers = [
        { userName: "Ana", penaltyPoints: 0 },
        { userName: "Beso", penaltyPoints: 2 },
        { userName: "Giorgi", penaltyPoints: 0 },
        { userName: "Dea", penaltyPoints: 1 },
        { userName: "Erekle", penaltyPoints: 0 }
    ];

    // Add users to the system
    sampleUsers.forEach(user => {
        users.push({ ...user, borrowingHistory: [], currentBorrows: [] });
    });
    console.log("Virtual Library System initialized with sample data!");
    console.log(`Total books: ${books.length}`);
    console.log(`Total users: ${users.length}`);
}

function addBook(book) {
    const newBook = {
        id: bookIdCounter++,
        title: book.title,
        author: book.author,
        genre: book.genre,
        rating: book.rating,
        year: book.year,
        borrowCount: 0,
        isAvailable: true,
        currentBorrower: null,
        dueDate: null
    };
    books.push(newBook);
    console.log(`Book "${newBook.title}" added to library with ID: ${newBook.id}`);
    return newBook.id;
}

function borrowBook(userName, bookId) {
    const user = users.find(u => u.userName === userName);
    if (!user) {
        console.log(`Error: User "${userName}" not found.`);
        return false;
    }

    // Find book
    const book = books.find(b => b.id === bookId);
    if (!book) {
        console.log(`Error: Book with ID ${bookId} not found.`);
        return false;
    }

    if (!book.isAvailable) {
        console.log(`Error: Book "${book.title}" is not available for borrowing.`);
        return false;
    }

    // Calculate due date (14 days from now)
    const borrowDate = new Date();
    const dueDate = new Date(borrowDate);
    dueDate.setDate(dueDate.getDate() + 14);

    // Update book status
    book.isAvailable = false;
    book.currentBorrower = userName;
    book.dueDate = dueDate;
    book.borrowCount++;

    // Update user's current borrows
    user.currentBorrows.push({
        bookId: bookId,
        bookTitle: book.title,
        borrowDate: borrowDate,
        dueDate: dueDate
    });

    console.log(`Book "${book.title}" successfully borrowed by ${userName}. Due date: ${dueDate.toDateString()}`);
    return true;
}

function returnBook(userName, bookId) {
    const user = users.find(u => u.userName === userName);
    if (!user) {
        console.log(`Error: User "${userName}" not found.`);
        return false;
    }

    // Find book
    const book = books.find(b => b.id === bookId);
    if (!book) { console.log(`Error: Book with ID ${bookId} not found.`); return false; }
    if (book.isAvailable) { console.log(`Error: Book "${book.title}" is already available.`); return false; }
    if (book.currentBorrower !== userName) { console.log(`Error: Book "${book.title}" is not borrowed by ${userName}.`); return false; }
    const returnDate = new Date();
    const isOverdue = returnDate > book.dueDate;
    let penaltyPoints = 0;
    if (isOverdue) {
        const daysOverdue = Math.ceil((returnDate - book.dueDate) / (1000 * 60 * 60 * 24));
        penaltyPoints = daysOverdue;
        user.penaltyPoints += penaltyPoints;
        console.log(`Book returned ${daysOverdue} days overdue. ${penaltyPoints} penalty points added to ${userName}.`);
    } else {
        console.log(`Thank you for returning "${book.title}" on time, ${userName}!`);
    }

    // Add to borrowing history
    user.borrowingHistory.push({
        bookId: bookId,
        bookTitle: book.title,
        borrowDate: book.dueDate.getTime() - (14 * 24 * 60 * 60 * 1000), // Calculate borrow date
        returnDate: returnDate,
        wasOverdue: isOverdue,
        penaltyPoints: penaltyPoints
    });

    // Remove from current borrows
    user.currentBorrows = user.currentBorrows.filter(borrow => borrow.bookId !== bookId);

    // Update book status
    book.isAvailable = true;
    book.currentBorrower = null;
    book.dueDate = null;
    return true;
}

function searchBooksBy(param, value) {
    let filteredBooks = [];
    switch (param.toLowerCase()) {
        case 'author':
            filteredBooks = books.filter(book => book.author.toLowerCase().includes(value.toLowerCase()));
            break;
        case 'genre':
            filteredBooks = books.filter(book => book.genre.toLowerCase().includes(value.toLowerCase()));
            break;
        case 'rating':
            const rating = parseFloat(value);
            if (isNaN(rating)) { console.log("Error: Invalid rating value."); return []; }
            filteredBooks = books.filter(book => book.rating >= rating);
            break;
        case 'year':
            const year = parseInt(value);
            if (isNaN(year)) { console.log("Error: Invalid year value."); return []; }
            filteredBooks = books.filter(book => book.year >= year);
            break;
        default:
            console.log("Error: Invalid search parameter. Use 'author', 'genre', 'rating', or 'year'.");
            return [];
    }
    console.log(`Found ${filteredBooks.length} books matching ${param}: ${value}`);
    filteredBooks.forEach(book => { console.log(`- "${book.title}" by ${book.author} (${book.year}) - Rating: ${book.rating}`); });
    return filteredBooks;
}

function getTopRatedBooks(limit) {
    const sortedBooks = [...books].sort((a, b) => b.rating - a.rating);
    const topBooks = sortedBooks.slice(0, limit);
    console.log(`Top ${limit} rated books:`);
    topBooks.forEach((book, index) => { console.log(`${index + 1}. "${book.title}" by ${book.author} - Rating: ${book.rating}`); });
    return topBooks;
}

function getMostPopularBooks(limit) {
    const sortedBooks = [...books].sort((a, b) => b.borrowCount - a.borrowCount);
    const popularBooks = sortedBooks.slice(0, limit);
    console.log(`Top ${limit} most popular books:`);
    popularBooks.forEach((book, index) => { console.log(`${index + 1}. "${book.title}" by ${book.author} - Borrowed ${book.borrowCount} times`); });
    return popularBooks;
}

function checkOverdueUsers() {
    const overdueUsers = [];
    const currentDate = new Date();
    users.forEach(user => {
        const overdueBooks = user.currentBorrows.filter(borrow => { const dueDate = new Date(borrow.dueDate); return currentDate > dueDate; });
        if (overdueBooks.length > 0) {
            overdueUsers.push({ userName: user.userName, overdueBooks: overdueBooks.map(book => ({ bookTitle: book.bookTitle, daysOverdue: Math.ceil((currentDate - new Date(book.dueDate)) / (1000 * 60 * 60 * 24)) })) });
        }
    });
    if (overdueUsers.length === 0) { console.log("No users have overdue books."); return []; }
    console.log("Users with overdue books:");
    overdueUsers.forEach(user => {
        console.log(`\n${user.userName}:`);
        user.overdueBooks.forEach(book => { console.log(`  - "${book.bookTitle}" (${book.daysOverdue} days overdue)`); });
    });
    return overdueUsers;
}

function recommendBooks(userName) {
    const user = users.find(u => u.userName === userName);
    if (!user) { console.log(`Error: User "${userName}" not found.`); return []; }
    const genreCount = {};
    user.borrowingHistory.forEach(borrow => {
        const book = books.find(b => b.id === borrow.bookId);
        if (book) { genreCount[book.genre] = (genreCount[book.genre] || 0) + 1; }
    });

    // Get books user hasn't borrowed yet
    const borrowedBookIds = new Set(user.borrowingHistory.map(borrow => borrow.bookId));
    const availableBooks = books.filter(book => 
        book.isAvailable && !borrowedBookIds.has(book.id)
    );

    // Sort by user's preferred genres and then by rating
    const recommendedBooks = availableBooks.sort((a, b) => {
        const aGenreScore = genreCount[a.genre] || 0;
        const bGenreScore = genreCount[b.genre] || 0;
        if (aGenreScore !== bGenreScore) { return bGenreScore - aGenreScore; }
        return b.rating - a.rating;
    });
    console.log(`Book recommendations for ${userName}:`);
    recommendedBooks.slice(0, 5).forEach((book, index) => {
        const genreScore = genreCount[book.genre] || 0;
        console.log(`${index + 1}. "${book.title}" by ${book.author} (${book.genre}) - Rating: ${book.rating} - Genre preference: ${genreScore}`);
    });
    return recommendedBooks.slice(0, 5);
}

function removeBook(bookId) {
    const bookIndex = books.findIndex(b => b.id === bookId);
    if (bookIndex === -1) { console.log(`Error: Book with ID ${bookId} not found.`); return false; }
    const book = books[bookIndex];
    if (!book.isAvailable) { console.log(`Error: Cannot remove book "${book.title}" - it is currently borrowed by ${book.currentBorrower}.`); return false; }
    const removedBook = books.splice(bookIndex, 1)[0];
    console.log(`Book "${removedBook.title}" has been removed from the library.`);
    return true;
}

function printUserSummary(userName) {
    const user = users.find(u => u.userName === userName);
    if (!user) { console.log(`Error: User "${userName}" not found.`); return; }
    console.log(`\n=== User Summary for ${userName} ===`);
    console.log(`Total penalty points: ${user.penaltyPoints}`);
    if (user.currentBorrows.length === 0) { console.log("Currently borrowed books: None"); }
    else {
        console.log("Currently borrowed books:");
        user.currentBorrows.forEach(borrow => {
            const dueDate = new Date(borrow.dueDate);
            const currentDate = new Date();
            const daysUntilDue = Math.ceil((dueDate - currentDate) / (1000 * 60 * 60 * 24));
            if (daysUntilDue < 0) { console.log(`  - "${borrow.bookTitle}" (${Math.abs(daysUntilDue)} days overdue)`); }
            else { console.log(`  - "${borrow.bookTitle}" (due in ${daysUntilDue} days)`); }
        });
    }

    if (user.borrowingHistory.length === 0) {
        console.log("Borrowing history: None");
    } else {
        console.log(`Borrowing history: ${user.borrowingHistory.length} books borrowed`);
    }
}

// Utility Functions

function listAllBooks() {
    console.log("\n=== All Books in Library ===");
    books.forEach(book => {
        const status = book.isAvailable ? "Available" : `Borrowed by ${book.currentBorrower}`;
        console.log(`ID: ${book.id} | "${book.title}" by ${book.author} | ${book.genre} | Rating: ${book.rating} | Status: ${status}`);
    });
}

function listAllUsers() {
    console.log("\n=== All Users ===");
    users.forEach(user => {
        console.log(`${user.userName} - Penalty points: ${user.penaltyPoints} - Current borrows: ${user.currentBorrows.length}`);
    });
}

// Demo function to showcase all features
function runDemo() {
    console.log("=== Virtual Library System Demo ===\n");
    console.log("1. Initial Library State:");
    listAllBooks();
    listAllUsers();
    console.log("\n2. Search Examples:");
    searchBooksBy('author', 'Orwell');
    searchBooksBy('genre', 'Fantasy');
    searchBooksBy('rating', '4.5');
    
    console.log("\n3. Top Books:");
    getTopRatedBooks(3);
    getMostPopularBooks(3);
    
    console.log("\n4. Borrowing Books:");
    borrowBook('Ana', 1);
    borrowBook('Beso', 3);
    borrowBook('Giorgi', 5);
    console.log("\n4. Top Books:");
    getTopRatedBooks(3);
    getMostPopularBooks(3);
    console.log("\n5. After Borrowing:");
    listAllBooks();
    console.log("\n6. User Summaries:");
    printUserSummary('Ana');
    printUserSummary('Beso');
    console.log("\n7. Returning Books:");
    returnBook('Ana', 1);
    returnBook('Beso', 3);
    console.log("\n8. Overdue Users Check:");
    checkOverdueUsers();
    console.log("\n9. Book Recommendations:");
    recommendBooks('Ana');
    recommendBooks('Beso');
    console.log("\n10. Adding New Book:");
    addBook({ title: "The Martian", author: "Andy Weir", genre: "Science Fiction", rating: 4.3, year: 2011 });
    console.log("\n11. Removing Book:");
    removeBook(16);
    console.log("\n12. Final Library State:");
    listAllBooks();
    listAllUsers();
    console.log("\n=== Demo Complete ===");
    console.log("All functions have been demonstrated successfully!");
}

// Initialize the system
initializeData();

// Show initial state
console.log("\n" + "=".repeat(50));
console.log("VIRTUAL LIBRARY SYSTEM - READY");
console.log("=".repeat(50));
console.log("\nAvailable functions:");
console.log("- addBook(book)");
console.log("- borrowBook(userName, bookId)");
console.log("- returnBook(userName, bookId)");
console.log("- searchBooksBy(param, value)");
console.log("- getTopRatedBooks(limit)");
console.log("- getMostPopularBooks(limit)");
console.log("- checkOverdueUsers()");
console.log("- recommendBooks(userName)");
console.log("- removeBook(bookId)");
console.log("- printUserSummary(userName)");
console.log("- listAllBooks()");
console.log("- listAllUsers()");
console.log("- runDemo()");
console.log("\nRun 'runDemo()' to see all functions in action!");

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        addBook,
        borrowBook,
        returnBook,
        searchBooksBy,
        getTopRatedBooks,
        getMostPopularBooks,
        checkOverdueUsers,
        recommendBooks,
        removeBook,
        printUserSummary,
        listAllBooks,
        listAllUsers,
        runDemo,
        books,
        users
    };
}

runDemo(); 
