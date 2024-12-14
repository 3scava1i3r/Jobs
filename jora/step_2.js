// Html to json

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const url = require('url');

const scrapedDataDir = path.join(__dirname, 'scraped_data');
let fullUrlFinalArray = [];
function shouldExcludeUrl(url) {
    const excludeWords = ['senior', 'lead', 'manager', 'director', 'staff-', 'principal', 'SSR', 'SR'];
    return excludeWords.some(word => url.toLowerCase().includes(word));
}


// Function to remove 'fsv' query parameter from a URL
function normalizeUrl(urlStr) {
    const parsedUrl = new URL(urlStr);
    // console.log(parsedUrl.toString())
    parsedUrl.searchParams.delete('fsv'); // Remove 'fsv' query parameter
    // console.log(parsedUrl.toString()) uncomment later

    return parsedUrl.toString(); // Return the normalized URL
}


fs.readdir(scrapedDataDir, (err, files) => {
    if (err) {
        console.error('Error reading directory:', err);
        return;
    }

    let filesProcessed = 0;

    files.forEach(file => {
        if (path.extname(file) === '.html') {
            const filePath = path.join(scrapedDataDir, file);
            fs.readFile(filePath, 'utf8', (err, data) => {
                if (err) {
                    console.error(`Error reading file ${file}:`, err);
                    return;
                }

                const $ = cheerio.load(data);
                const jobLinks = $('.job-link');

                let startUrl = ''

                const appleLogin = $('.apple-login');
                if (appleLogin.length > 0) {
                    const redirectUri = appleLogin.attr('data-redirect-uri');
                    if (redirectUri) {
                        const trimmedUri = redirectUri.split('/sign_in_with_apple_sessions')[0];
                        // console.log('Base URL from apple-login:', trimmedUri);
                        startUrl = trimmedUri
                    }
                }


                // console.log(`Found ${jobLinks.length} job links in ${file}:`);
                jobLinks.each((index, element) => {
                    const href = $(element).attr('href');
                    const baseUrl = file.split('_')[0].replace(/_/g, '.') + '/';
                    const fullUrlFinal = url.resolve(baseUrl, href);
                    const finalUrl = url.resolve(startUrl, href);
                    // console.log("fullUrlFinal===========>", fullUrlFinal);
                    // fullUrlFinalArray.push(finalUrl);


                    const normalizedUrl = normalizeUrl(finalUrl); // Normalize the URL by removing 'fsv'

                    if (!shouldExcludeUrl(normalizedUrl)) {
                        fullUrlFinalArray.push(normalizedUrl);
                    }
                });


                filesProcessed++;
                if (filesProcessed === files.length) {
                    // All files have been processed
                    let uniqueUrlsSet = new Set(fullUrlFinalArray);
                    let uniqueUrlsArray = Array.from(uniqueUrlsSet);
                    // console.log("All unique full URLs:", uniqueUrlsArray); uncomment later

                    // Export uniqueUrlsArray to a file
                    const outputPath = path.join(__dirname, 'unique_urls.json');
                    fs.writeFile(outputPath, JSON.stringify(uniqueUrlsArray, null, 2), (err) => {
                        if (err) {
                            console.error('Error writing to file:', err);
                        } else {
                            console.log(`Unique URLs exported to ${outputPath}`);
                        }
                    });
                }
            });
        } else {
            filesProcessed++;
        }
    });
});
