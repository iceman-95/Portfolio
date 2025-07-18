# Virtual Library System

A pure JavaScript, console-based virtual library. All logic is handled through function calls—no UI, no HTML, no CSS, and no dependencies. Everything is in a single file: `library.js`.

## Features
- Add, borrow, return, search, and remove books
- Track users, borrowing history, and penalty points
- 14-day borrowing period with overdue penalties
- Personalized book recommendations
- Top-rated and most popular books
- Overdue user tracking
- Predefined sample books and users (edit in `library.js`)

## Getting Started
1. **Make sure you have [Node.js](https://nodejs.org/) installed.**
2. **Place `library.js` in your project folder.**
3. **Run the script:**
   ```bash
   node library.js
   ```
   This will automatically run a demo showcasing all features.

## Usage
- All actions are performed by calling functions in `library.js`.
- You can comment out or remove the `runDemo();` line at the end if you want to use the library interactively.
- To use interactively:
  1. Start Node.js REPL: `node`
  2. Load the file: `.load library.js`
  3. Call any function, e.g. `borrowBook('Ana', 1)`

## Predefined User Names
- Ana
- Beso
- Giorgi
- Dea
- Erekle

## Main Functions
- `addBook(book)`
- `borrowBook(userName, bookId)`
- `returnBook(userName, bookId)`
- `searchBooksBy(param, value)`
- `getTopRatedBooks(limit)`
- `getMostPopularBooks(limit)`
- `checkOverdueUsers()`
- `recommendBooks(userName)`
- `removeBook(bookId)`
- `printUserSummary(userName)`
- `listAllBooks()`
- `listAllUsers()`
- `runDemo()`

## Example Usage
```js
borrowBook('Ana', 1);
returnBook('Ana', 1);
searchBooksBy('author', 'Orwell');
getTopRatedBooks(3);
recommendBooks('Dea');
printUserSummary('Beso');
```

## Customization
- To change users or books, edit the `sampleUsers` or `sampleBooks` arrays in the `initializeData` function in `library.js`.

## Do I need any other files?
**No.** Everything is self-contained in `library.js`. The README is for documentation only.
