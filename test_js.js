const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('sohyeon_sillok.html', 'utf8');
try {
    const dom = new JSDOM(html, { runScripts: "dangerously" });
    console.log("No syntax errors found on load.");
} catch (e) {
    console.error("Syntax error:", e);
}
