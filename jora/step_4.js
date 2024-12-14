// segregate them acc to language
const fs = require('fs');


urlList = {
    'https://ar.jora.com': 'spanish',
    'https://au.jora.com': 'no',
    'https://us.jora.com': 'no',
    'https://th.jora.com': 'thai',
    'https://sg.jobsdb.com': 'no',
    'https://pt.jora.com': 'portugese',
    'https://ph.jora.com': 'no',
    'https://pe.jora.com': 'spanish',
    'https://nz.jora.com': 'no',
    'https://my.jora.com': 'no',
    'https://mx.jora.com': 'spanish',
    'https://in.jora.com': 'no',
    'https://ie.jora.com': 'no',
    'https://id.jora.com': 'Indonesian',
    'https://hk.jora.com': 'no',
    'https://uk.jora.com': 'no',
    'https://fr.jora.com': 'french',
    'https://es.jora.com': 'spanish',
    'https://ec.jora.com': 'spanish',
    'https://bd.jora.com': 'no',
    'https://br.jora.com': 'portugese',
    'https://ca.jora.com': 'no',
    'https://cl.jora.com': 'spanish',
    'https://co.jora.com': 'spanish',
}


// Read the job_data_100percent.json file
const jobData = JSON.parse(fs.readFileSync('job_data_100percent.json', 'utf8'));

// Create an object to store jobs by language
const jobsByLanguage = {};

// Iterate through each job in the jobData
jobData.forEach(job => {
    // console.log(job)
    const url = new URL(job.url).origin;
    // console.log('urls', url)
    const language = urlList[url] || 'unknown';

    if (!jobsByLanguage[language]) {
        jobsByLanguage[language] = [];
    }
    jobsByLanguage[language].push(job);
});

// Write separate JSON files for each language
for (const [language, jobs] of Object.entries(jobsByLanguage)) {
    const fileName = `jobs_${language}.json`;
    fs.writeFileSync(fileName, JSON.stringify(jobs, null, 2));
    console.log(`Created ${fileName} with ${jobs.length} jobs`);
}





// translate using ai








