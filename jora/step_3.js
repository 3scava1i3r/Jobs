const fs = require('fs');
const path = require('path');
// const fetch = require('node-fetch');
const cheerio = require('cheerio');  // Import cheerio for HTML parsing.

const uniqueUrlsPath = path.join(__dirname, 'unique_urls.json');

function isFresherJob(jobTitle, jobDescription) {
    const fresherKeywords = [
        'fresh graduate', 'entry level', 'junior', 'trainee', 'graduate program', 'intern', 'no experience required'
    ];
    const experiencePattern = /\b(\d+)\+?\s?(years|yrs)?\s?experience\b/i;
    const advancedSkillsKeywords = ['advanced', 'expert', 'certification', 'proficient'];
    const educationKeywords = ['recent graduate', 'final-year student'];

    const hasFresherKeyword = fresherKeywords.some(keyword =>
        jobTitle.toLowerCase().includes(keyword) || jobDescription.toLowerCase().includes(keyword)
    );
    const hasExperienceRequirement = experiencePattern.test(jobDescription);
    const hasAdvancedSkillsRequirement = advancedSkillsKeywords.some(skill =>
        jobDescription.toLowerCase().includes(skill)
    );
    const hasEducationForFreshers = educationKeywords.some(keyword =>
        jobDescription.toLowerCase().includes(keyword)
    );

    return hasFresherKeyword || (!hasExperienceRequirement && !hasAdvancedSkillsRequirement && hasEducationForFreshers);
}

const fetchWithTimeout = (url, options = {}, timeout = 30000) => {
    return Promise.race([
        fetch(url, options),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Request timeout')), timeout)
        )
    ]);
};


const fetchWithRetry = async (url, options = {}, maxRetries = 3) => {
    for (let i = 0; i < maxRetries; i++) {
        try {
            return await fetchWithTimeout(url, options);
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, i) * 1000));
        }
    }
};


// Read the unique_urls.json file
fs.readFile(uniqueUrlsPath, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading unique_urls.json:', err);
        return;
    }

    const urls = JSON.parse(data);

    // Function to fetch HTML content
    async function fetchHtml(url) {
        try {
            const response = await fetch(url);
            // console.log(response) uncomment later
            const html = await response.text();
            return html;
        } catch (error) {
            console.error(`Error fetching ${url}:`, error);
            return null;
        }
    }

    // Process each URL
    urls.forEach(async (url, index) => {


        fetchWithRetry(url, {
            "headers": {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "priority": "u=0, i",
                "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "cookie": "sol_id=23be07be-41b4-4f2b-ab3b-0eb414901358; _cfuvid=wJEm5s59j5x2uQGyQsK4WQJFABIuW_.OWOBrGjoZFL4-1727454284137-0.0.1.1-604800000; jsu=---%0A%3Aid%3A+dad00ea4-a677-4402-8894-f9eb116d2655%0A%3Alr%3A+1727470556%0A%3Alv%3A+%0A%3Acv%3A+1727470556%0A%3Asi%3A+ca%0A%3Aemail%3A+%0A; qd=eyJxIjoiZGV2ZWxvcGVyIiwibCI6IktpdGNoZW5lciwgT250YXJpbyIsImxpZCI6bnVsbH0; _jobengine_session=MndtZ2dlamZOWjlrMDBtZkR2WjhQUWZVbnpqL1RVc2V1My90MzhJMEt4NURvQzgvQ2ZiZ3d1empvdmhxSWx1RExmbFA1ZU9Rd3BoN2FRcXRDSE81MlR5YVRCV0oxOGttbmZ4emxJRmNreFNxZHF0akFad3gxU09xYkNBZ2NkcXZQU3R6YWh4cldBdUEwVUdQNHpHL0JpdTlTMmJYeGRvVlBqRXJPN2crUENEcW5Od1hwVVJqd3V4dzVLN0NoMlZFVDhtdHNJNE9BZUEvZEJpTEZMZXRIOTkwaHFCRHJiK1RKTFFnYVgwSUpyOWZhQm9wblNubnFFUTNieGRuTldBVnNMNjVjc3ZONTVjeE96dVl4OWxKbkQ5NkViRlJ0SGdhSVByZnhxMWVRTkowM2dac0pRWThlVk00OE0ySHVNSUItLTQvckpxK1ppUnc2bEh3dUZJZGdUYUE9PQ%3D%3D--bcb973054336d6d992c15e6d6a7088a4333dce00"
            },
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": null,
            "method": "GET"
        }).then(response => response.text())
            .then(html => {
                // console.log(html); uncomment later
                // const fileName = `${baseUrl.replace(/[^a-z0-9]/gi, '_')}_${keyword}_page${page}.html`;
                // const filePath = path.join(__dirname, 'scraped_data', fileName);
                // fs.writeFileSync(filePath, data);
                // console.log(`Saved ${fileName}`);
                const $ = cheerio.load(html);

                // Extract job description, job info, and job link
                const jobDescription = $('#job-description-container').text().trim();
                const jobInfo = $('#job-info-container').text().trim();
                const jobLink = $('.job-view-actions-container.bottom-actions-container a').attr('href');

                // Log the extracted information
                // console.log('url', url); uncomment later
                // console.log("Job Description:", jobDescription); uncomment later
                // console.log("Job Info:", jobInfo); uncomment later
                // console.log("Job Link:", jobLink); uncomment later

            })
            .catch(error => {
                console.error("Fetch error:", error);
            });


        // const html = await fetchHtml(url);
        // if (html) {
        //     console.log(html, "html")

        //     fetch(url,
        //         {
        //             "headers": {
        //                 "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        //                 "accept-language": "en-US,en;q=0.9",
        //                 "cache-control": "max-age=0",
        //                 "priority": "u=0, i",
        //                 "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        //                 "sec-ch-ua-mobile": "?0",
        //                 "sec-ch-ua-platform": "\"macOS\"",
        //                 "sec-fetch-dest": "document",
        //                 "sec-fetch-mode": "navigate",
        //                 "sec-fetch-site": "none",
        //                 "sec-fetch-user": "?1",
        //                 "upgrade-insecure-requests": "1",
        //                 "cookie": "sol_id=23be07be-41b4-4f2b-ab3b-0eb414901358; _cfuvid=wJEm5s59j5x2uQGyQsK4WQJFABIuW_.OWOBrGjoZFL4-1727454284137-0.0.1.1-604800000; jsu=---%0A%3Aid%3A+dad00ea4-a677-4402-8894-f9eb116d2655%0A%3Alr%3A+1727470556%0A%3Alv%3A+%0A%3Acv%3A+1727470556%0A%3Asi%3A+ca%0A%3Aemail%3A+%0A; qd=eyJxIjoiZGV2ZWxvcGVyIiwibCI6IktpdGNoZW5lciwgT250YXJpbyIsImxpZCI6bnVsbH0; _jobengine_session=MndtZ2dlamZOWjlrMDBtZkR2WjhQUWZVbnpqL1RVc2V1My90MzhJMEt4NURvQzgvQ2ZiZ3d1empvdmhxSWx1RExmbFA1ZU9Rd3BoN2FRcXRDSE81MlR5YVRCV0oxOGttbmZ4emxJRmNreFNxZHF0akFad3gxU09xYkNBZ2NkcXZQU3R6YWh4cldBdUEwVUdQNHpHL0JpdTlTMmJYeGRvVlBqRXJPN2crUENEcW5Od1hwVVJqd3V4dzVLN0NoMlZFVDhtdHNJNE9BZUEvZEJpTEZMZXRIOTkwaHFCRHJiK1RKTFFnYVgwSUpyOWZhQm9wblNubnFFUTNieGRuTldBVnNMNjVjc3ZONTVjeE96dVl4OWxKbkQ5NkViRlJ0SGdhSVByZnhxMWVRTkowM2dac0pRWThlVk00OE0ySHVNSUItLTQvckpxK1ppUnc2bEh3dUZJZGdUYUE9PQ%3D%3D--bcb973054336d6d992c15e6d6a7088a4333dce00"
        //             },
        //             "referrerPolicy": "strict-origin-when-cross-origin",
        //             "body": null,
        //             "method": "GET"
        //         }
        //     )
        //         .then(response => response.text())
        //         .then(html => {
        //             console.log(html);
        //             // const fileName = `${baseUrl.replace(/[^a-z0-9]/gi, '_')}_${keyword}_page${page}.html`;
        //             // const filePath = path.join(__dirname, 'scraped_data', fileName);
        //             // fs.writeFileSync(filePath, data);
        //             // console.log(`Saved ${fileName}`);
        //             const $ = cheerio.load(html);

        //             // Extract job description, job info, and job link
        //             const jobDescription = $('#job-description-container').text().trim();
        //             const jobInfo = $('#job-info-container').text().trim();
        //             const jobLink = $('.job-view-actions-container.bottom-actions-container a').attr('href');

        //             if (isFresherJob(jobTitle, jobDescription)) {
        //                 console.log("This job is likely for freshers.");
        //             } else {
        //                 console.log("This job may require more experience.");
        //             }

        //             // Log the extracted information
        //             console.log('url', url);
        //             console.log("Job Description:", jobDescription);
        //             console.log("Job Info:", jobInfo);
        //             console.log("Job Link:", jobLink);

        //         })
        //         .catch(error => {
        //             console.error("Fetch error:", error);
        //         });


        //     // if (isFresherJob(jobTitle, jobDescription)) {
        //     //     console.log("This job is likely for freshers.");
        //     // } else {
        //     //     console.log("This job may require more experience.");
        //     // }

        //     // const fileName = `job_${index + 1}.html`;
        //     // const filePath = path.join(__dirname, 'job_htmls', fileName);

        //     // // Ensure the directory exists
        //     // fs.mkdirSync(path.dirname(filePath), { recursive: true });

        //     // // Write the HTML content to a file
        //     // fs.writeFile(filePath, html, (err) => {
        //     //     if (err) {
        //     //         console.error(`Error writing ${fileName}:`, err);
        //     //     } else {
        //     //         console.log(`Saved ${fileName}`);
        //     //     }
        //     // });
        // }
    });
});
