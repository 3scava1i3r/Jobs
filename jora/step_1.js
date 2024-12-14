// Get all Jobs

const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const writeFileAsync = promisify(fs.writeFile);

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
urlList = [
    'https://ar.jora.com/',
    'https://au.jora.com/'
    , 'https://us.jora.com/', 'https://th.jora.com/', 'https://sg.jobsdb.com'
    , 'https://pt.jora.com/', 'https://ph.jora.com/', 'https://pe.jora.com/'
    , 'https://nz.jora.com/', 'https://my.jora.com/'

    , 'https://mx.jora.com/'
    , 'https://in.jora.com/'

    , 'https://ie.jora.com/', 'https://id.jora.com/'

    , 'https://hk.jora.com/', 'https://uk.jora.com/', 'https://fr.jora.com/', 'https://es.jora.com/', 'https://ec.jora.com/', 'https://bd.jora.com/', 'https://br.jora.com/', 'https://ca.jora.com/', 'https://cl.jora.com/', 'https://co.jora.com/'

]
keyword_list = ['backend', 'developer', 'software']


async function fetchWithRetry(url, options, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(url, options);
            return await response.text();
        } catch (error) {
            if (i === retries - 1) throw error;
            await delay(1000 * (i + 1)); // Exponential backoff
        }
    }
}



async function processUrl(baseUrl, keyword, page) {


    const url = `${baseUrl}j?l=&nofollow=true&p=${page}&q=${keyword}&sp=homepage&surl=0&trigger_source=homepage`;


    // const url = `${baseUrl}j?l=&nofollow=true&p=${page}&q=${keyword}&sp=search&surl=0&tk=erN69pcQqxsBGoxImEJm-uPST43sluMBpjWDg2jMc&trigger_source=serp`;
    try {
        const data = await fetchWithRetry(url, {
            "headers": {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en-US,en;q=0.9",
                "priority": "u=0, i",
                "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "cookie": "sol_id=23be07be-41b4-4f2b-ab3b-0eb414901358; qd=eyJxIjoiYmFja2VuZCIsImwiOiJJbmRpYSIsImxpZCI6bnVsbH0; jsu=---%0A%3Aid%3A+dd690297-377d-48ab-bdc1-3e85a323eeb5%0A%3Alr%3A+1727426458%0A%3Alv%3A+%0A%3Acv%3A+1727426458%0A%3Asi%3A+in%0A%3Aemail%3A+%0A; rs=---%0A-+q%3A+backend%0A++l%3A+India%0A++trigger_source%3A+serp%0A++sp%3A+search%0A++p%3A+5%0A++surl%3A+false%0A++controller%3A+search%0A++action%3A+index%0A++tk%3A+erN69pcQqxsBGoxImEJm-LnC5z3XtoMdbKmSiv1_Z%0A++a%3A+%0A-+q%3A+It%0A++l%3A+%27%27%0A++a%3A+%0A++sp%3A+browse%0A; sc=3; _cfuvid=gdSk_Dwh_rz4ifEKTN6h0MiFHjBGDwJ3JZMC9qOIv_4-1727426458580-0.0.1.1-604800000; dads=1; _jobengine_session=RUZWOXBiNjVZZ0JwTTk4ODZBUndsVUlzaGJncWdMZTIrZU9BemRrWU1pYU92VEJuSVlsd0ZDOFZDS2JQZkpIejlKTmczcG9qajMyT3dtWm9PQU10VU04VkhVaFdoZzRHYk5tUkdHa0pjZ21TQnhlZlJUNmR2WHpUOGFiMFZ3Z01wUlpaSlF5MGdrOUwwS2p0WnJNS1hGTVVqL2o5ejFxOHdvNEdxQVZLMEVjdU01aDNIY0wzOUV3TFB1U3hzNjY5WUtueDZDcEh0bnVBK3VtRUZNclhHcWtjMkpmNXZFa1FjYjFodklUV3BkcTdabFNuMENzOWpMY3MrQUNXMzNyKzBDZjR0Uy9PeHJWYUFyTFdKdTBtRkZaaURaWnc3dVJtZWlWb0hmbnUvMUxQNS9LWkwvdmtaWTZ6M1lMT3JpTFItLW5Ma3ZHaGxUMTZmeUowR25ML3MxS2c9PQ%3D%3D--a78f8a8a8058b6b3dc6987909530f93933696c58",
                "Referer": "https://in.jora.com/j?l=India&nofollow=true&p=5&q=backend&sp=search&surl=0&tk=erN69pcQqxsBGoxImEJm-LnC5z3XtoMdbKmSiv1_Z&trigger_source=serp",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            },
            "body": null,
            "method": "GET"
        });

        const fileName = `${baseUrl.replace(/[^a-z0-9]/gi, '_')}_${keyword}_page${page}.html`;
        const dirPath = path.join(__dirname, 'scraped_data');
        const filePath = path.join(dirPath, fileName);

        if (!fs.existsSync(dirPath)) {
            fs.mkdirSync(dirPath, { recursive: true });
        }

        await writeFileAsync(filePath, data);
        console.log(`Saved ${fileName}`);
    } catch (error) {
        console.error(`Error processing ${url}:`, error);
    }
}

async function main() {
    for (const baseUrl of urlList) {
        for (const keyword of keyword_list) {
            for (let page = 1; page <= 1; page++) {
                await processUrl(baseUrl, keyword, page);
                await delay(1000); // Rate limiting: 1 request per second
            }
        }
    }
}

main().catch(console.error);
